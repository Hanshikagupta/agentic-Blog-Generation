# Blog Writing Agent

An AI-powered blog writing agent that generates technical blog posts using **LangGraph orchestration**, **RAG (Retrieval-Augmented Generation)**, **web research**, and **image generation**. Built to demonstrate production-grade agent patterns for portfolio/resume use.

## Highlights (Resume-Ready)

| Feature | Technology | What It Demonstrates |
|---------|-----------|---------------------|
| **Multi-agent orchestration** | LangGraph | Router → RAG → Research → Plan → Parallel Workers → Reducer |
| **RAG pipeline** | ChromaDB + OpenAI Embeddings | Document ingestion, chunking, semantic retrieval |
| **Hybrid retrieval** | ChromaDB + Tavily | Internal knowledge + live web evidence |
| **Structured outputs** | Pydantic + LangChain | Typed routing, planning, and evaluation |
| **Parallel generation** | LangGraph `Send` API | Fan-out section writers, map-reduce pattern |
| **Quality evaluation** | LLM-as-judge | Automated post-generation scoring |
| **REST API** | FastAPI | Programmatic access with OpenAPI docs |
| **Image generation** | Google Gemini | Diagram planning + generation with graceful fallback |

## Architecture

```
START
  ↓
ROUTER          → closed_book | hybrid | open_book
  ↓
RAG RETRIEVE    → ChromaDB semantic search (knowledge base)
  ↓
RESEARCH?       → Tavily web search (optional)
  ↓
ORCHESTRATOR    → structured blog plan (5–9 sections)
  ↓
WORKERS × N     → parallel section writing
  ↓
REDUCER         → merge → plan images → generate images
  ↓
EVALUATE        → quality score + notes
  ↓
END
```

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here      # optional — web research
GOOGLE_API_KEY=your_google_api_key_here      # optional — image generation
```

### 3. Index your knowledge base (RAG)

Add `.md` or `.txt` files to `knowledge_base/`, then:

```bash
python index_docs.py
```

A sample LangGraph guide is included in `knowledge_base/langgraph_guide.md`.

### 4. Generate a blog

**CLI:**

```bash
python bog.py
```

**REST API:**

```bash
uvicorn api:api --reload
```

Then open http://localhost:8000/docs for interactive API documentation.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Service status + KB document count |
| `POST` | `/index` | Index documents from a directory |
| `POST` | `/generate` | Generate a blog post |

### Example: Generate via API

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "How to use LangGraph for AI workflows", "use_rag": true}'
```

Response includes `content`, `quality_score`, `kb_chunks_used`, and `web_evidence_count`.

## Project Structure

```
blog/
├── bog.py                  # Main LangGraph agent (CLI entry point)
├── api.py                  # FastAPI REST server
├── index_docs.py           # Knowledge base indexing CLI
├── rag/
│   ├── store.py            # ChromaDB vector store
│   └── ingest.py           # Document loading + chunking
├── knowledge_base/         # Source documents for RAG
├── chroma_db/              # Persisted vector store (generated)
├── requirements.txt
└── README.md
```

## Modes

- **closed_book** — Evergreen concepts; RAG provides domain grounding
- **hybrid** — RAG + web research for up-to-date examples
- **open_book** — News/event-driven; web research with recency filtering

## Blog Kinds

- `explainer` — Conceptual explanations
- `tutorial` — Step-by-step guides
- `news_roundup` — Weekly/topical roundup
- `comparison` — Technology comparisons
- `system_design` — Architecture deep-dives

## Extending the Agent

1. **Add documents** — Drop files into `knowledge_base/` and run `python index_docs.py`
2. **Add nodes** — Define a function and wire it into the graph in `bog.py`
3. **Change models** — Edit the `llm` instance in `bog.py` (default: `gpt-4o-mini`)
4. **Adjust RAG** — Tune `chunk_size`, `k`, or embedding model in `rag/`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `OPENAI_API_KEY is not set` | Add key to `.env` |
| RAG returns 0 chunks | Run `python index_docs.py` first |
| Research skipped | Add `TAVILY_API_KEY` to `.env` |
| No images | Add `GOOGLE_API_KEY`; blog still generates without them |

## Documentation

For a complete deep-dive into code logic, theory, and interview preparation, see **[docs/BOOK.md](docs/BOOK.md)**.

Topics covered:
- System architecture and data flow
- Node-by-node code walkthrough
- RAG pipeline theory and implementation
- Design patterns and production considerations
- 36 interview questions with detailed answers

## License

MIT License
