import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from pdf_loader import load_pdf

text = load_pdf("uploads/resume (1).pdf")

print(text[:1000])