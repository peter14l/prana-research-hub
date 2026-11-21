"""
Print Table of Contents of CSIR-NEERI 2020
"""
import fitz

doc = fitz.open("backend/data/research_docs/CSIR_NEERI_2020_Final_Report.pdf")

# Search pages 1-25 for table of contents
for p in range(25):
    text = doc[p].get_text()
    if "table of contents" in text.lower() or "contents" in text.lower() or "chapter" in text.lower():
        print(f"--- PAGE {p+1} ---")
        print(text[:1500])
