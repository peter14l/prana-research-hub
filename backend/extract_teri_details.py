"""
Extract exact text from key pages in TERI 2025
"""
import fitz

doc = fitz.open("backend/data/research_docs/TERI_2025_Kolkata_Study.pdf")

pages_to_extract = [29, 82, 130, 131, 140, 142, 152, 157, 158, 177, 178, 200]

for p in pages_to_extract:
    print(f"\n==================== TERI PAGE {p} ====================")
    text = doc[p - 1].get_text()
    print(text[:3000])
