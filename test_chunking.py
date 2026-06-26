from pdf_loader import load_pdf
from chunking import chunk_text

text = load_pdf("uploads/resume (1).pdf")

chunks = chunk_text(text)

print("Total Chunks:", len(chunks))

print("\n====================\n")

for i, chunk in enumerate(chunks[:3]):
    print(f"Chunk {i+1}")
    print(chunk)
    print("\n--------------------\n")