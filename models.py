from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from sqlalchemy.orm import declarative_base

from sqlalchemy.sql import func


Base = declarative_base()


class Document(Base):

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255))

    filename = Column(String(255))

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class Chunk(Base):

    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id")
    )

    chunk_number = Column(Integer)

    text = Column(Text)


class ChatHistory(Base):

    __tablename__ = "chat_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    question = Column(
        Text,
        nullable=False
    )

    answer = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class Embedding(Base):

    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True)

    chunk_id = Column(
        Integer,
        ForeignKey("chunks.id")
    )

    vector = Column(Text)

    chunk = relationship("Chunk")