from fastapi import APIRouter, UploadFile, File
import shutil
import os

from backend.app.rag_pipeline import process_and_store, query_chunks

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