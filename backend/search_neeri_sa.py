"""
Search for source apportionment results and tables in CSIR-NEERI 2020
"""
import fitz

doc = fitz.open("backend/data/research_docs/CSIR_NEERI_2020_Final_Report.pdf")

# Search for Chapter 5 or Chapter 6 or CMB results
for p in range(len(doc)):
    text = doc[p].get_text()
    if "cmb" in text.lower() or "source apportionment" in text.lower() or "apportionment" in text.lower():
        # Check if table or percentage is mentioned
        for line in text.split("\n"):
            if "%" in line and any(w in line.lower() for w in ["industry", "industrial", "foundry"]):
                print(f"Page {p + 1}: {line.strip()}")
            if "table 5." in line.lower() or "table 6." in line.lower():
                print(f"Page {p + 1} Table: {line.strip()}")
