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


def chunk_text(text, chunk_size=500, overlap=50):
    # split by sentences first
    import re
    sentences = re.split(r'(?<=[.!?\n]) +', text.strip())

    chunks = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) <= chunk_size:
            current += " " + sentence
        else:
            if current.strip():
                chunks.append(current.strip())
            # overlap: carry last `overlap` chars into next chunk
            current = current[-overlap:] + " " + sentence

    if current.strip():
        chunks.append(current.strip())

    return chunks


def get_embedding(text):
    return model.encode(text).tolist()


def store_chunks(chunks):
    # clear old data first
    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])

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
