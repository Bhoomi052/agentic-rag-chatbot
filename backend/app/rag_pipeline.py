from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from sqlalchemy import text
from backend.app.db import SessionLocal

# load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# ---------------------------
# 1. LOAD PDF
# ---------------------------
def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


# ---------------------------
# 2. CHUNK TEXT
# ---------------------------
def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


# ---------------------------
# 3. EMBEDDING
# ---------------------------
def get_embedding(text):
    return model.encode(text).tolist()


# ---------------------------
# 4. STORE IN POSTGRES (SQLAlchemy)
# ---------------------------
def store_chunks(chunks):
    db = SessionLocal()

    for chunk in chunks:
        embedding = get_embedding(chunk)

        db.execute(
            text("INSERT INTO documents (content, embedding) VALUES (:content, :embedding)"),
            {"content": chunk, "embedding": embedding}
        )

    db.commit()
    db.close()


# ---------------------------
# 5. QUERY (SIMILARITY SEARCH)
# ---------------------------
def query_chunks(query, k=3):
    db = SessionLocal()

    query_embedding = get_embedding(query)

    results = db.execute(
        text("""
        SELECT content
        FROM documents
        ORDER BY embedding <-> :embedding
        LIMIT :k
        """),
        {"embedding": query_embedding, "k": k}
    ).fetchall()

    db.close()

    return [r[0] for r in results]


# ---------------------------
# 6. FULL PIPELINE
# ---------------------------
def process_and_store(file_path):
    text = load_pdf(file_path)
    chunks = chunk_text(text)
    store_chunks(chunks)

    return len(chunks)