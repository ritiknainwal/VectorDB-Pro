import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from embeddings import get_embedding

vec = get_embedding("Machine Learning")

print(len(vec))
print(vec[:10])