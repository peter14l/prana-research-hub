"""
Audit script for TERI 2025 Report
File: backend/data/research_docs/TERI_2025_Kolkata_Study.pdf
"""
import fitz

doc = fitz.open("backend/data/research_docs/TERI_2025_Kolkata_Study.pdf")
print("Total Pages in TERI 2025:", len(doc))

# Search for "Dhapa"
dhapa_pages = []
for p in range(len(doc)):
    text = doc[p].get_text()
    if "dhapa" in text.lower():
        dhapa_pages.append(p + 1)
print(f"Dhapa appears on pages ({len(dhapa_pages)}): {dhapa_pages}")

# Search for "Table 4.6" and "Table 4.5" and "Table 6.14"
target_tables = ["table 4.6", "table 4.5", "table 6.14", "table 6.4"]
table_matches = []
for p in range(len(doc)):
    text = doc[p].get_text()
    for t in target_tables:
        if t in text.lower():
            table_matches.append((p + 1, t))
print(f"Target table mentions: {table_matches}")

# Search for "14%" or "14 %"
fourteen_matches = []
for p in range(len(doc)):
    text = doc[p].get_text()
    if ("14%" in text or "14 %" in text) and ("waste" in text.lower() or "refuse" in text.lower() or "burning" in text.lower() or "pm2.5" in text.lower()):
        fourteen_matches.append(p + 1)
print(f"Pages with 14% and waste/burning/PM2.5 ({len(fourteen_matches)}): {fourteen_matches}")

# Search for "34%" in TERI
thirtyfour_matches = []
for p in range(len(doc)):
    text = doc[p].get_text()
    if ("34%" in text or "34 %" in text) and ("industrial" in text.lower() or "ghusuri" in text.lower() or "howrah" in text.lower()):
        thirtyfour_matches.append(p + 1)
print(f"Pages with 34% and industrial/howrah in TERI: {thirtyfour_matches}")
