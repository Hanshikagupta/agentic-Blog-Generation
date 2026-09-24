from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.store import KnowledgeBase

SUPPORTED_EXTENSIONS = {".md", ".txt", ".markdown"}


def load_documents(source_dir: Path) -> List[Document]:
    """Load markdown/text files from a directory."""
    documents: List[Document] = []
    if not source_dir.exists():
        return documents

    for path in sorted(source_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").strip()
        if not text:
            continue
        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": str(path),
                    "title": _title_from_content(path, text),
                },
            )
        )
    return documents


def _title_from_content(path: Path, text: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("_", " ").replace("-", " ").title()


def chunk_documents(
    documents: Iterable[Document],
    chunk_size: int = 800,
    chunk_overlap: int = 120,
) -> List[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "],
    )
    return splitter.split_documents(list(documents))


def index_directory(
    source_dir: Path,
    persist_dir: Path | None = None,
    chunk_size: int = 800,
    chunk_overlap: int = 120,
) -> dict:
    """Index all supported documents from source_dir into the knowledge base."""
    kb = KnowledgeBase(persist_dir=persist_dir or Path("chroma_db"))
    raw_docs = load_documents(source_dir)
    if not raw_docs:
        return {"files": 0, "chunks": 0, "message": f"No documents found in {source_dir}"}

    chunks = chunk_documents(raw_docs, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    added = kb.add_documents(chunks)
    return {
        "files": len(raw_docs),
        "chunks": added,
        "total_in_store": kb.count(),
        "message": f"Indexed {len(raw_docs)} file(s) into {added} chunk(s).",
    }
