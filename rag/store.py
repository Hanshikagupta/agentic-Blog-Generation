from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document


DEFAULT_PERSIST_DIR = Path("chroma_db")
DEFAULT_COLLECTION = "blog_knowledge_base"


@dataclass
class RetrievedChunk:
    content: str
    source: str
    title: str
    score: float


class KnowledgeBase:
    """ChromaDB-backed vector store for domain knowledge retrieval."""

    def __init__(
        self,
        persist_dir: Path | str = DEFAULT_PERSIST_DIR,
        collection_name: str = DEFAULT_COLLECTION,
    ):
        self.persist_dir = Path(persist_dir)
        self.collection_name = collection_name
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self._store: Optional[Chroma] = None

    @property
    def exists(self) -> bool:
        return self.persist_dir.exists() and any(self.persist_dir.iterdir())

    def _get_store(self) -> Chroma:
        if self._store is None:
            self.persist_dir.mkdir(parents=True, exist_ok=True)
            self._store = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=str(self.persist_dir),
            )
        return self._store

    def add_documents(self, documents: List[Document]) -> int:
        if not documents:
            return 0
        store = self._get_store()
        store.add_documents(documents)
        return len(documents)

    def retrieve(self, query: str, k: int = 8) -> List[RetrievedChunk]:
        if not self.exists:
            return []
        if not os.getenv("OPENAI_API_KEY"):
            return []

        store = self._get_store()
        results = store.similarity_search_with_relevance_scores(query, k=k)

        chunks: List[RetrievedChunk] = []
        for doc, score in results:
            source = doc.metadata.get("source", "unknown")
            title = doc.metadata.get("title") or Path(source).stem
            chunks.append(
                RetrievedChunk(
                    content=doc.page_content,
                    source=source,
                    title=title,
                    score=float(score),
                )
            )
        return chunks

    def count(self) -> int:
        if not self.exists:
            return 0
        try:
            store = self._get_store()
            return store._collection.count()  # type: ignore[attr-defined]
        except Exception:
            return 0
