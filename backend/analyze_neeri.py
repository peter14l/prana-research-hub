"""
Audit script for CSIR-NEERI 2020 Report
File: backend/data/research_docs/CSIR_NEERI_2020_Final_Report.pdf
"""
import fitz # PyMuPDF
import re

doc = fitz.open("backend/data/research_docs/CSIR_NEERI_2020_Final_Report.pdf")
print("Total Pages in CSIR-NEERI 2020:", len(doc))

# Search for "34%", "34 %", "Table 6.14", "Ghusuri", "foundr", "cupola", "industrial"
findings = []

for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    
    # Check for 34% or Table 6.14
    if "34%" in text or "34 %" in text or "Table 6.14" in text or "6.14" in text:
        findings.append((page_num + 1, "34% / Table 6.14 reference", text))
    
    # Check for cupola
    if "cupola" in text.lower():
        print(f"Page {page_num + 1} mentions cupola!")

print(f"\nFound {len(findings)} pages matching '34%' or 'Table 6.14':")
for pnum, label, txt in findings:
    print(f"\n--- PAGE {pnum} ({label}) ---")
    lines = [line.strip() for line in txt.split("\n") if line.strip()]
    for i, line in enumerate(lines):
        if any(term in line.lower() for term in ["34%", "34 %", "table 6.14", "ghusuri", "industrial"]):
            start = max(0, i - 4)
            end = min(len(lines), i + 5)
            snippet = " // ".join(lines[start:end])
            print(f"Line match: {snippet}\n")
