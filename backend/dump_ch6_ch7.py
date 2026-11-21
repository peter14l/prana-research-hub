"""
Extract Chapter 4.7, Chapter 6 and Chapter 7 from CSIR-NEERI 2020
"""
import fitz

doc = fitz.open("backend/data/research_docs/CSIR_NEERI_2020_Final_Report.pdf")

# Search for "7.2.2" or "Winter: Howrah"
for p in range(len(doc)):
    text = doc[p].get_text()
    if "7.2.2" in text or "winter: howrah" in text.lower() or "chapter 7" in text.lower() or "chapter 6" in text.lower():
        print(f"\n==================== PAGE {p+1} (PDF) ====================")
        print(text[:2500])
