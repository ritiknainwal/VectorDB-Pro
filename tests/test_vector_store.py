import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

from vector_store import (
    add_document,
    search_documents,
    total_vectors
)


add_document(
    "Python",
    "Python is a programming language."
)

add_document(
    "Machine Learning",
    "Machine learning is a branch of Artificial Intelligence."
)

print("Vectors:", total_vectors())

print()

results = search_documents(
    "What is AI?"
)

for r in results:

    print(r["metadata"]["title"])
    print(r["score"])
    print()