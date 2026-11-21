import sqlite3
import json

conn = sqlite3.connect('backend/data/prana.db')
cursor = conn.cursor()

cursor.execute("SELECT slug, title, problem_statement, supporting_evidence, geographic_relevance, evidence_strength_score, score_explanations FROM candidate_opportunities")
candidates = cursor.fetchall()

print("ALL CANDIDATES IN DB:")
for c in candidates:
    print(f"\n--- {c[0]} ({c[1]}) ---")
    print(f"Problem: {c[2]}")
    print(f"Evidence: {c[3]}")
    print(f"Geo: {c[4]}")
    print(f"Current Evidence Score: {c[5]}")

print("\n\nRESEARCH DOCUMENTS IN DB:")
cursor.execute("SELECT id, title, organisation, publication_date, geographic_coverage, key_findings FROM research_documents")
docs = cursor.fetchall()
for d in docs:
    print(f"ID {d[0]} | {d[1]} | Org: {d[2]} | Date: {d[3]} | Scope: {d[4]}")
    print(f"   Findings: {d[5][:150]}...")

print("\n\nRESEARCH FINDINGS IN DB:")
cursor.execute("SELECT id, document_id, title, statement, citation_reference, page_number FROM research_findings")
findings = cursor.fetchall()
for f in findings:
    print(f"ID {f[0]} | DocID: {f[1]} | {f[2]} | Citation: {f[4]} (p. {f[5]})")

print("\n\nSOURCE APPORTIONMENT PROFILES IN DB:")
cursor.execute("""
    SELECT scp.id, sc.name, scp.pollutant, scp.season, scp.city, scp.contribution_percentage, scp.citation_reference, scp.page_number
    FROM source_contribution_profiles scp
    JOIN source_categories sc ON scp.category_id = sc.id
""")
profiles = cursor.fetchall()
for p in profiles:
    print(f"ID {p[0]} | Sector: {p[1]} | {p[2]} {p[3]} in {p[4]}: {p[5]}% | Citation: {p[6]} (p. {p[7]})")

print("\n\nCAAQM STATIONS IN DB:")
cursor.execute("SELECT id, station_code, cpcb_site_id, name, city, latitude, longitude, verification_status FROM monitoring_stations")
stations = cursor.fetchall()
for s in stations:
    print(f"ID {s[0]} | {s[1]} ({s[2]}) | {s[3]}, {s[4]} | Coords: ({s[5]}, {s[6]}) | Status: {s[7]}")

conn.close()
