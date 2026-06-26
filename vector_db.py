import numpy as np

class VectorDB:

    def __init__(self):
        self.items = []

    def cosine_similarity(self, a, b):

        a = np.array(a)
        b = np.array(b)

        return np.dot(a, b) / (
            np.linalg.norm(a) * np.linalg.norm(b)
        )

    def insert(self, vector, metadata):

        self.items.append({
            "vector": np.array(vector),
            "metadata": metadata
        })

    def search(self, query, k=3):

        query = np.array(query)

        results = []

        for item in self.items:

            score = self.cosine_similarity(
                query,
                item["vector"]
            )

            results.append({
                "score": float(score),
                "metadata": item["metadata"]
            })

        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results[:k]