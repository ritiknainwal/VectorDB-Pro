from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from rag import generate_answer 
from vector_store import index_pdf
from fastapi import UploadFile, File
from database import *

import shutil
import os

from vector_store import (
    add_document,
    search_documents,
    total_vectors,
    all_vectors,
    get_documents,
    index_pdf,
    rebuild_index
)

class AskRequest(BaseModel):
    question: str
    k: int = 3

app = FastAPI(title="VectorDB Pro")

init_db()
rebuild_index()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


# ---------------- Models ---------------- #

class Document(BaseModel):
    title: str
    text: str


class SearchRequest(BaseModel):
    query: str
    k: int = 3


# ---------------- Routes ---------------- #

@app.get("/")
def home():
    return {
        "message": "VectorDB Pro Backend Running 🚀"
    }


@app.get("/ui")
def ui():
    return FileResponse("templates/index.html")


@app.get("/status")
def status():
    return {
        "vectors": total_vectors(),
        "dimensions": 768,
        "model": "nomic-embed-text"
    }


@app.get("/vectors")
def vectors():
    return all_vectors()


@app.post("/insert")
def insert(doc: Document):

    add_document(
        doc.title,
        doc.text
    )

    return {
        "success": True,
        "total_vectors": total_vectors()
    }

@app.get("/list")
def list_documents():

    docs = get_documents()

    result = []

    for i, doc in enumerate(docs):

        result.append({

            "id": i,

            "title": doc["title"],

            "text": doc["filename"]

        })

    return result

@app.post("/search")
def search(req: SearchRequest):

    results = search_documents(
        req.query,
        req.k
    )

    return results

@app.get("/points")
def get_points():

    points = []

    vectors = all_vectors()

    for i, item in enumerate(vectors):

        vector = item["vector"]

        # Temporary projection using first two dimensions
        x = float(vector[0]) * 150
        y = float(vector[1]) * 150

        points.append({
            "id": i,
            "title": item["metadata"]["title"],
            "x": x,
            "y": y
        })

    return points

@app.post("/ask")
def ask(req: AskRequest):

    results = search_documents(
        req.question,
        req.k
    )

    context = ""

    sources = []

    for r in results:

        context += r["metadata"]["text"] + "\n\n"

        sources.append({

            "title": r["metadata"]["title"],

            "score": round((1-r["score"])*100,2)

        })

    answer = generate_answer(
        req.question,
        context
    )

    # ⭐ Save conversation
    save_chat(
        req.question,
        answer
    )

    return {

        "answer": answer,

        "sources": sources

    }

@app.get("/history")
def history():

    rows = load_history()

    history = []

    for q, a, t in rows:

        history.append({

            "question": q,

            "answer": a,

            "time": t

        })

    return history

@app.post("/upload_pdf")
def upload_pdf(file: UploadFile = File(...)):

    # Create uploads folder if it doesn't exist
    os.makedirs("uploads", exist_ok=True)

    save_path = os.path.join("uploads", file.filename)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    total_chunks = index_pdf(save_path)

    return {
        "success": True,
        "filename": file.filename,
        "chunks": total_chunks
    }