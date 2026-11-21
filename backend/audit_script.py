import sqlite3

conn = sqlite3.connect('D:/project-prana/backend/data/prana.db')
c = conn.cursor()

print("=== Table Counts ===")
tables = c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
for t in tables:
    count = c.execute(f"SELECT count(*) FROM {t[0]}").fetchone()[0]
    print(f"{t[0]}: {count}")

print("\n=== Monitoring Stations ===")
for row in c.execute("SELECT id, station_code, name, city, latitude, longitude, active, is_demo, metadata_json FROM monitoring_stations").fetchall():
    print(row)

print("\n=== Data Providers ===")
for row in c.execute("SELECT id, code, name, provider_type, portal_url, status, last_synced_at FROM data_providers").fetchall():
    print(row)

print("\n=== Quality Breakdown in Validated Observations ===")
for row in c.execute("SELECT quality_status, count(*) FROM validated_observations GROUP BY quality_status").fetchall():
    print(row)

print("\n=== Provenance in Validated Observations ===")
for row in c.execute("SELECT provenance, count(*) FROM validated_observations GROUP BY provenance").fetchall():
    print(row)

print("\n=== Research Documents ===")
for row in c.execute("SELECT id, title, organisation, original_url, confidence_tier FROM research_documents").fetchall():
    print(row)

print("\n=== Source Contribution Profiles ===")
for row in c.execute("SELECT id, pollutant, season, city, contribution_percentage, evidence_type FROM source_contribution_profiles").fetchall():
    print(row)

print("\n=== Intervention Hypotheses ===")
for row in c.execute("SELECT id, title, target_area, status, research_confidence FROM intervention_hypotheses").fetchall():
    print(row)
