"""
Examine specific pages in CSIR-NEERI 2020
"""
import fitz

doc = fitz.open("backend/data/research_docs/CSIR_NEERI_2020_Final_Report.pdf")

pages_to_check = [36, 54, 95, 96, 97, 98, 114, 148]

for p in pages_to_check:
    print(f"\n==================== PAGE {p} ====================")
    text = doc[p - 1].get_text()
    print(text[:2000])
