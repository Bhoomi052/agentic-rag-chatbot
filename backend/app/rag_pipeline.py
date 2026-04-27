from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from backend.app.db import collection

model = SentenceTransformer("all-MiniLM-L6-v2")


def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def get_embedding(text):
    return model.encode(text).tolist()


def store_chunks(chunks):
    embeddings = [get_embedding(chunk) for chunk in chunks]
    ids = [str(i) for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids)


def query_chunks(query, k=3):
    query_embedding = get_embedding(query)
    results = collection.query(query_embeddings=[query_embedding], n_results=k)
    return results["documents"][0]


def process_and_store(file_path):
    text = load_pdf(file_path)
    chunks = chunk_text(text)
    store_chunks(chunks)
    return len(chunks)
