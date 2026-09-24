"""FastAPI server for the Blog Writing Agent."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

load_dotenv()

from bog import app as graph_app, build_initial_state  # noqa: E402
from rag.ingest import index_directory  # noqa: E402
from rag.store import KnowledgeBase  # noqa: E402

api = FastAPI(
    title="Blog Writing Agent API",
    description="Generate technical blog posts with RAG, web research, and image generation.",
    version="2.0.0",
)


class GenerateRequest(BaseModel):
    topic: str = Field(..., min_length=3, description="Blog topic or prompt")
    as_of: Optional[str] = Field(default=None, description="As-of date (YYYY-MM-DD)")
    use_rag: bool = Field(default=True, description="Retrieve from knowledge base if available")


class GenerateResponse(BaseModel):
    title: str
    content: str
    filename: str
    mode: str
    kb_chunks_used: int
    web_evidence_count: int
    quality_score: Optional[float] = None
    quality_notes: Optional[str] = None


class IndexRequest(BaseModel):
    source_dir: str = Field(default="knowledge_base")
    chunk_size: int = 800
    chunk_overlap: int = 120


class IndexResponse(BaseModel):
    files: int
    chunks: int
    total_in_store: int
    message: str


class HealthResponse(BaseModel):
    status: str
    kb_documents: int
    kb_available: bool


@api.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    kb = KnowledgeBase()
    count = kb.count()
    return HealthResponse(status="ok", kb_documents=count, kb_available=kb.exists)


@api.post("/index", response_model=IndexResponse)
def index_docs(req: IndexRequest) -> IndexResponse:
    source = Path(req.source_dir)
    if not source.exists():
        raise HTTPException(status_code=404, detail=f"Source directory not found: {source}")

    result = index_directory(
        source_dir=source,
        chunk_size=req.chunk_size,
        chunk_overlap=req.chunk_overlap,
    )
    return IndexResponse(
        files=result.get("files", 0),
        chunks=result.get("chunks", 0),
        total_in_store=result.get("total_in_store", 0),
        message=result.get("message", "Done"),
    )


@api.post("/generate", response_model=GenerateResponse)
def generate_blog(req: GenerateRequest) -> GenerateResponse:
    as_of = req.as_of or date.today().isoformat()
    inputs = build_initial_state(topic=req.topic, as_of=as_of, use_rag=req.use_rag)

    try:
        result = graph_app.invoke(inputs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

    plan = result.get("plan")
    title = plan.blog_title if plan else "blog"
    content = result.get("final") or result.get("merged_md") or ""
    filename = f"{title.replace(' ', '_').lower()}.md"

    quality = result.get("quality_report")
    return GenerateResponse(
        title=title,
        content=content,
        filename=filename,
        mode=result.get("mode", "unknown"),
        kb_chunks_used=len(result.get("kb_evidence", [])),
        web_evidence_count=len(result.get("evidence", [])),
        quality_score=quality.score if quality else None,
        quality_notes=quality.notes if quality else None,
    )


@api.get("/")
def root() -> dict:
    return {
        "service": "Blog Writing Agent",
        "docs": "/docs",
        "endpoints": ["/health", "/index", "/generate"],
    }
