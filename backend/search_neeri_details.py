"""
Search Chapter 6 and Ghusuri in CSIR-NEERI 2020 Report
"""
import fitz

doc = fitz.open("backend/data/research_docs/CSIR_NEERI_2020_Final_Report.pdf")

# Search for Ghusuri
ghusuri_pages = []
for p in range(len(doc)):
    text = doc[p].get_text()
    if "ghusuri" in text.lower():
        ghusuri_pages.append(p + 1)
print(f"Ghusuri appears on pages: {ghusuri_pages}")

# Search for "foundry" or "foundries"
foundry_pages = []
for p in range(len(doc)):
    text = doc[p].get_text()
    if "foundr" in text.lower():
        foundry_pages.append(p + 1)
print(f"Foundry/Foundries appears on pages: {foundry_pages}")

# Search for Table 6.
table6_pages = []
for p in range(len(doc)):
    text = doc[p].get_text()
    for line in text.split("\n"):
        if "table 6." in line.lower():
            table6_pages.append((p + 1, line.strip()))
print(f"\nTables in Chapter 6 found ({len(table6_pages)}):")
for p, title in table6_pages[:25]:
    print(f"Page {p}: {title}")

# Search for source apportionment results for Howrah / PM2.5
sa_pages = []
for p in range(len(doc)):
    text = doc[p].get_text()
    if ("source apportionment" in text.lower() or "cmb" in text.lower()) and "pm2.5" in text.lower():
        sa_pages.append(p + 1)
print(f"\nSource apportionment / CMB & PM2.5 mentioned on pages: {sa_pages[:20]}")
