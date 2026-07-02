from sentence_transformers import SentenceTransformer

print("Loading embedding model...")

model = SentenceTransformer("BAAI/bge-base-en-v1.5")

print("Embedding model loaded!")


def get_embedding(text: str):

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()