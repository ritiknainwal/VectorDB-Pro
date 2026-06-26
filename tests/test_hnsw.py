from hnsw_engine import HNSWVectorDB
import numpy as np

db = HNSWVectorDB(dim=4)

db.insert(
    np.array([1,0,0,0]),
    {"name":"A"}
)

db.insert(
    np.array([0,1,0,0]),
    {"name":"B"}
)

db.insert(
    np.array([0,0,1,0]),
    {"name":"C"}
)

result = db.search(
    np.array([1,0,0,0]),
    2
)

print(result)