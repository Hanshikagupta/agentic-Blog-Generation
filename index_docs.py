#!/usr/bin/env python3
"""CLI to index documents into the RAG knowledge base."""

from __future__ import annotations

import argparse
from pathlib import Path

from dotenv import load_dotenv

from rag.ingest import index_directory

load_dotenv()


def main() -> None:
    parser = argparse.ArgumentParser(description="Index documents into the blog agent knowledge base.")
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("knowledge_base"),
        help="Directory containing .md/.txt files (default: knowledge_base/)",
    )
    parser.add_argument(
        "--persist",
        type=Path,
        default=Path("chroma_db"),
        help="ChromaDB persist directory (default: chroma_db/)",
    )
    parser.add_argument("--chunk-size", type=int, default=800)
    parser.add_argument("--chunk-overlap", type=int, default=120)
    args = parser.parse_args()

    result = index_directory(
        source_dir=args.source,
        persist_dir=args.persist,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
    )
    print(result["message"])
    print(f"  Files indexed: {result.get('files', 0)}")
    print(f"  Chunks added:  {result.get('chunks', 0)}")
    print(f"  Total in store: {result.get('total_in_store', 0)}")


if __name__ == "__main__":
    main()
