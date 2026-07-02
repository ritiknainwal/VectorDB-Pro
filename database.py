import os

from dotenv import load_dotenv
import json
from models import Embedding

from sqlalchemy import (
    create_engine,
    text
)

from sqlalchemy.orm import sessionmaker


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def test_connection():

    with engine.connect() as conn:

        result = conn.execute(
            text("SELECT version();")
        )

        print(result.fetchone()[0])

from models import Base


def init_db():

    Base.metadata.create_all(bind=engine)  

from sqlalchemy.orm import Session
from models import Document, Chunk


def save_document(title, filename):
    db = Session(engine)

    doc = Document(
        title=title,
        filename=filename
    )

    db.add(doc)
    db.commit()
    db.refresh(doc)
    db.close()

    return doc.id


def save_chunk(document_id, chunk_number, text_data):

    db = SessionLocal()

    chunk = Chunk(
        document_id=document_id,
        chunk_number=chunk_number,
        text=text_data
    )

    db.add(chunk)

    db.commit()

    db.refresh(chunk)

    chunk_id = chunk.id

    db.close()

    return chunk_id

from models import ChatHistory


def save_chat(question, answer):

    db = SessionLocal()

    chat = ChatHistory(
        question=question,
        answer=answer
    )

    db.add(chat)

    db.commit()

    db.close()


def load_history():

    db = SessionLocal()

    chats = (
        db.query(ChatHistory)
        .order_by(ChatHistory.id.desc())
        .all()
    )

    db.close()

    return chats

from models import Chunk

def load_all_chunks():

    db = SessionLocal()

    chunks = (
        db.query(Chunk)
        .order_by(Chunk.document_id, Chunk.chunk_number)
        .all()
    )

    db.close()

    return chunks

from models import Document


def load_documents():

    db = SessionLocal()

    docs = (
        db.query(Document)
        .order_by(Document.id.desc())
        .all()
    )

    db.close()

    return docs

def save_embedding(chunk_id, embedding):

    db = SessionLocal()

    row = Embedding(
        chunk_id=chunk_id,
        vector=json.dumps(embedding)
    )

    db.add(row)

    db.commit()

    db.close()

def load_all_embeddings():

    db = SessionLocal()

    embeddings = db.query(Embedding).all()

    db.close()

    return embeddings

def document_exists(filename):

    db = SessionLocal()

    exists = (
        db.query(Document)
        .filter(Document.filename == filename)
        .first()
    )

    db.close()

    return exists

from models import Document, Chunk, Embedding

def delete_document(filename):

    db = SessionLocal()

    # Find the document
    document = db.query(Document).filter(
        Document.filename == filename
    ).first()

    if not document:
        db.close()
        return

    # Find all chunks belonging to the document
    chunks = db.query(Chunk).filter(
        Chunk.document_id == document.id
    ).all()

    # Delete embeddings of each chunk
    for chunk in chunks:

        db.query(Embedding).filter(
            Embedding.chunk_id == chunk.id
        ).delete()

    # Delete all chunks
    db.query(Chunk).filter(
        Chunk.document_id == document.id
    ).delete()

    # Delete document
    db.delete(document)

    db.commit()

    db.close()