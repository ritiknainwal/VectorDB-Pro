import hnswlib
import numpy as np


class HNSWVectorDB:

    def __init__(self, dim=768, max_elements=10000):

        self.dim = dim
        self.count = 0

        self.index = hnswlib.Index(
            space="cosine",
            dim=dim
        )

        self.index.init_index(
            max_elements=max_elements,
            ef_construction=200,
            M=16
        )

        self.index.set_ef(50)

        self.items = []


    def insert(self, vector, metadata):

        vector = np.asarray(vector, dtype=np.float32)

        self.index.add_items(
            vector.reshape(1, -1),
            np.array([self.count])
        )

        self.items.append({
            "id": self.count,
            "vector": vector.tolist(),
            "metadata": metadata
        })

        self.count += 1


    def search(self, query, k=3):

        if self.count == 0:
            return []

        query = np.asarray(
            query,
            dtype=np.float32
        )

        k = min(k, self.count)

        labels, distances = self.index.knn_query(
            query.reshape(1, -1),
            k=k
        )

        results = []

        for label, distance in zip(
            labels[0],
            distances[0]
        ):

            item = self.items[int(label)]

            results.append({
                "id": item["id"],
                "score": float(1 - distance),
                "metadata": item["metadata"],
                "vector": item["vector"]
            })

        return results


    def get_all_items(self):

        return self.items


    def size(self):

        return self.count