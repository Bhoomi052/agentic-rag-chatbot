# Agentic RAG Chatbot 🤖

An AI-powered RAG (Retrieval Augmented Generation) chatbot that lets you upload a PDF and ask questions about it.

## What This Does
- Upload any PDF
- Automatically chunks, embeds, and stores it in ChromaDB
- Ask questions → get relevant answers from the PDF content

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI |
| Frontend | HTML + CSS + JS (served via FastAPI) |
| Vector DB | ChromaDB (local, persistent) |
| Embeddings | SentenceTransformers (`all-MiniLM-L6-v2`) |
| PDF Parsing | pypdf |

---

## Project Structure

```
agentic-rag-chatbot/
├── backend/
│   ├── __init__.py
│   └── app/
│       ├── main.py          # FastAPI app + CORS + static files
│       ├── db.py            # ChromaDB client setup
│       ├── rag_pipeline.py  # PDF load, chunk, embed, store, query
│       ├── routes.py        # API endpoints
│       └── models.py        # Not used (ChromaDB handles storage)
├── frontend/
│   └── index.html           # UI — upload PDF + chat interface
├── chroma_store/            # Auto-created — vector data stored here
├── data/                    # Uploaded PDFs saved here
├── inspect_db.py            # Script to inspect stored chunks
├── example.env              # Environment variable template
└── requirements.txt
```

---

## Changes Made

### 1. Migrated from PostgreSQL → ChromaDB
- Removed `psycopg2-binary`, SQLAlchemy, pgvector setup
- `db.py` now uses `chromadb.PersistentClient` — no DB server needed
- `models.py` cleared — ChromaDB handles its own storage
- `main.py` cleaned — removed `Base.metadata.create_all()`

### 2. Fixed Chunking (Sentence-aware)
- Old: character-based chunking — words were cut in the middle
- New: sentence-aware chunking using `re.split()` on `.` `!` `?` `\n`
- Words and sentences are never split across chunks now

### 3. Fixed Duplicate Chunks
- `store_chunks()` now clears old data before storing new PDF
- Re-uploading same PDF won't create duplicate entries

### 4. Added Frontend
- Dark themed UI built with HTML/CSS/JS
- PDF upload section with status feedback
- Chat-style query interface
- Served directly from FastAPI at `http://127.0.0.1:8000`

### 5. Added CORS + Static Files
- `CORSMiddleware` added so frontend can call backend APIs
- `StaticFiles` mounted at `/static` to serve frontend
- `aiofiles` added to requirements (needed by StaticFiles)

### 6. Added `/inspect` Endpoint
- `GET /inspect?limit=5` — view stored chunks and vector previews
- Useful for debugging what's stored in ChromaDB

---

## Setup & Run

```bash
# 1. Clone and go to project folder
cd agentic-rag-chatbot

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy env file
copy example.env .env        # Windows
cp example.env .env          # Mac/Linux

# 5. Run server
PYTHONPATH=. uvicorn backend.app.main:app --reload
```

Open browser: `http://127.0.0.1:8000`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serves frontend UI |
| POST | `/upload` | Upload and process PDF |
| GET | `/query?q=your question` | Query the PDF |
| GET | `/inspect?limit=5` | View stored chunks in ChromaDB |

---

## Environment Variables (`example.env`)

```
APP_ENV=development
CHROMA_PERSIST_PATH=./chroma_store
CHROMA_COLLECTION_NAME=documents
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

---

## Inspect Stored Data

```bash
# Terminal se
PYTHONPATH=. python inspect_db.py

# Browser se
http://127.0.0.1:8000/inspect
```

---

## Team
- Bhoomi (Backend + AI)
- Krrish (Backend + AI + Frontend)
