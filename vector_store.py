import os
import json 

from embeddings import get_embedding
from hnsw_engine import HNSWVectorDB
from pdf_loader import load_pdf
from chunking import chunk_text

from database import (
    save_document,
    save_chunk,
    save_embedding,
    load_documents,
    load_all_chunks,
    load_all_embeddings,
    document_exists
)

# Create one global HNSW database
db = HNSWVectorDB(dim=768)


def add_document(title: str, text: str):

    embedding = get_embedding(text)

    metadata = {
        "title": title,
        "text": text
    }

    db.insert(
        embedding,
        metadata
    )


def search_documents(query: str, k=3):
    """
    Search similar documents.
    """

    query_embedding = get_embedding(query)

    return db.search(
        query_embedding,
        k
    )


def total_vectors():
    return db.size()


def all_vectors():
    return db.get_all_items()

def get_documents():

    docs = load_documents()

    result = []

    for doc in docs:

        result.append({

            "title": doc.title,

            "filename": doc.filename

        })

    return result


def index_pdf(pdf_path: str):

    filename = os.path.basename(pdf_path)
    
    if document_exists(filename):
        return -1

    text = load_pdf(pdf_path)

    chunks = chunk_text(text)

    filename = pdf_path.split("\\")[-1]

    document_id = save_document(
        filename,
        filename
    )
    for i, chunk in enumerate(chunks):
        chunk_id = save_chunk(document_id,i + 1,chunk)
        embedding = get_embedding(chunk)
        save_embedding(chunk_id,embedding)
        metadata = {
            "title": f"{filename} - Chunk {i+1}",
            "text": chunk
            }
        db.insert(
        embedding,
        metadata
        )
    return len(chunks)

def rebuild_index():

    global db

    # Create a fresh empty HNSW index
    db = HNSWVectorDB(dim=768)

    chunks = load_all_chunks()
    embeddings = load_all_embeddings()

    print(f"Chunks: {len(chunks)}")
    print(f"Embeddings: {len(embeddings)}")

    print(f"Loading {len(chunks)} chunks from PostgreSQL...")

    embedding_map = {}

    for emb in embeddings:
        embedding_map[emb.chunk_id] = json.loads(emb.vector)

    for chunk in chunks:

        if chunk.id not in embedding_map:
            continue

        metadata = {
            "title": f"Document {chunk.document_id} - Chunk {chunk.chunk_number}",
            "text": chunk.text
        }

        db.insert(
            embedding_map[chunk.id],
            metadata
        )

    print("HNSW Index rebuilt from stored embeddings!")