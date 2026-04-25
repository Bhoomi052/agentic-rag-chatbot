from fastapi import FastAPI
from backend.app.routes import router

# 👇 add these imports
from backend.app.models import Base
from backend.app.db import engine

app = FastAPI()

# 👇 AUTO CREATE TABLE (IMPORTANT)
Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def home():
    return {"message": "RAG API running 🚀"}