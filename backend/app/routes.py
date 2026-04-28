from fastapi import APIRouter, UploadFile, File
import shutil
import os

from backend.app.rag_pipeline import process_and_store, query_chunks
from backend.app.db import collection

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    os.makedirs("data", exist_ok=True)

    file_path = f"data/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    count = process_and_store(file_path)

    return {"message": f"{count} chunks stored 🔥"}


@router.get("/query")
def query(q: str):
    results = query_chunks(q)
    return {"results": results}


@router.get("/inspect")
def inspect_db(limit: int = 5):
    results = collection.get(limit=limit, include=["documents", "embeddings"])
    data = []
    for i, doc in enumerate(results["documents"]):
        data.append({
            "id": results["ids"][i],
            "text_preview": doc[:200],
            "vector_preview": results["embeddings"][i][:5]
        })
    return {"total": collection.count(), "chunks": data}