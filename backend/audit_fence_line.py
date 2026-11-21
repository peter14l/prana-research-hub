import sqlite3
import json
import math

conn = sqlite3.connect('backend/data/prana.db')
cursor = conn.cursor()

print("================================================================================")
print("1. CANDIDATE OPPORTUNITY RECORD IN DATABASE")
print("================================================================================")
cursor.execute("SELECT * FROM candidate_opportunities WHERE slug = 'industrial-fence-line-attribution'")
row = cursor.fetchone()
cols = [desc[0] for desc in cursor.description]
cand = dict(zip(cols, row))
for k, v in cand.items():
    if k in ['title', 'slug', 'sector', 'problem_statement', 'supporting_evidence', 'geographic_relevance', 'evidence_strength_score', 'score_explanations', 'data_classification']:
        print(f"{k}: {v}\n")

print("================================================================================")
print("2. JALAN INDUSTRIAL COMPLEX & MONITORING STATIONS COORDINATES")
print("================================================================================")
# Check Jalan coordinates in research_gaps or candidate
cursor.execute("SELECT * FROM research_gaps WHERE gap_code = 'GAP-001'")
gap_row = cursor.fetchone()
gap_cols = [desc[0] for desc in cursor.description]
gap = dict(zip(gap_cols, gap_row))
print("GAP-001 record:", gap)

cursor.execute("SELECT id, station_code, cpcb_site_id, name, city, latitude, longitude, verification_status FROM monitoring_stations")
stations = cursor.fetchall()
print("\nAll monitoring stations in DB:")
jalan_lat, jalan_lon = 22.59, 88.24  # from candidate / gap record
print(f"Jalan Coordinates recorded in PRANA: lat={jalan_lat}, lon={jalan_lon}")

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

station_distances = []
for s in stations:
    d = haversine(jalan_lat, jalan_lon, s[5], s[6])
    station_distances.append((s[0], s[1], s[2], s[3], s[4], s[5], s[6], round(d, 2), s[7]))

station_distances.sort(key=lambda x: x[7])
print("\nStations sorted by distance to Jalan Complex:")
for s in station_distances:
    print(f"ID {s[0]} | {s[1]} ({s[2]}) | {s[3]}, {s[4]} | Coords: ({s[5]}, {s[6]}) | Distance: {s[7]} km | Status: {s[8]}")

print("================================================================================")
print("3. PADMAPUKUR PM2.5 OBSERVATIONS IN DATABASE")
print("================================================================================")
# Padmapukur station id
padmapukur = [s for s in stations if "PADMAPUKUR" in s[1].upper() or "PADMAPUKUR" in s[3].upper()]
print("Padmapukur station:", padmapukur)

if padmapukur:
    pad_id = padmapukur[0][0]
    # Check sensor for PM2.5 at Padmapukur
    cursor.execute("SELECT id, pollutant, unit, sampling_interval FROM sensors WHERE station_id = ?", (pad_id,))
    sensors = cursor.fetchall()
    print("Sensors at Padmapukur:", sensors)
    
    # Check columns of validated_observations
    cursor.execute("PRAGMA table_info(validated_observations)")
    vo_cols = [c[1] for c in cursor.fetchall()]
    print("Columns in validated_observations:", vo_cols)

    # Query PM2.5 observations at Padmapukur
    cursor.execute("""
        SELECT *
        FROM validated_observations
        WHERE station_id = ? AND pollutant = 'PM2.5'
        ORDER BY observation_timestamp ASC
    """, (pad_id,))
    pad_obs_rows = cursor.fetchall()
    print(f"Total PM2.5 observations for Padmapukur: {len(pad_obs_rows)}")
    pad_obs = [dict(zip(vo_cols, r)) for r in pad_obs_rows]
    
    # Check values > 180
    high_obs = [o for o in pad_obs if (o.get('normalized_value') or 0) > 180]
    print(f"Observations with normalized_value > 180 µg/m³: {len(high_obs)}")
    
    # Check midnight to dawn (00:00 to 06:00)
    midnight_to_dawn = []
    for o in pad_obs:
        dt = str(o.get('observation_timestamp', ''))
        # check hour
        hour = int(dt[11:13]) if len(dt) > 13 else -1
        if 0 <= hour <= 6:
            midnight_to_dawn.append(o)
    print(f"Observations between 00:00 and 06:00: {len(midnight_to_dawn)}")
    high_night_obs = [o for o in midnight_to_dawn if (o.get('normalized_value') or 0) > 180]
    print(f"Midnight-to-dawn observations > 180 µg/m³: {len(high_night_obs)}")
    
    print("\nSample Padmapukur PM2.5 observations (first 5):")
    for o in pad_obs[:5]:
        print(o)
        
    print("\nMax concentration at Padmapukur PM2.5:")
    if pad_obs:
        max_obs = max(pad_obs, key=lambda x: x.get('normalized_value') or 0)
        print("Max record:", max_obs)
        min_obs = min(pad_obs, key=lambda x: x.get('normalized_value') or 0)
        print("Min record:", min_obs)

    # Let's also check if there are raw_observations
    cursor.execute("PRAGMA table_info(raw_observations)")
    raw_cols = [c[1] for c in cursor.fetchall()]
    print("\nColumns in raw_observations:", raw_cols)
    cursor.execute("SELECT COUNT(*) FROM raw_observations WHERE station_id = ? AND pollutant = 'PM2.5'", (pad_id,))
    print("Raw observations for Padmapukur PM2.5 count:", cursor.fetchone()[0])
    cursor.execute("SELECT * FROM raw_observations WHERE station_id = ? AND pollutant = 'PM2.5' AND raw_value > 180", (pad_id,))
    high_raw = cursor.fetchall()
    print("Raw observations > 180 count:", len(high_raw))
    if high_raw:
        print("Sample high raw:", high_raw[:3])

print("================================================================================")
print("4. WEATHER / WIND DATA IN DATABASE")
print("================================================================================")
cursor.execute("SELECT COUNT(*) FROM weather_observations")
total_weather = cursor.fetchone()[0]
print(f"Total weather observations: {total_weather}")

cursor.execute("""
    SELECT id, observation_timestamp, wind_speed_kmh, wind_direction_deg, wind_direction_cardinal, data_classification, data_provider
    FROM weather_observations
    WHERE wind_direction_cardinal LIKE '%NW%' OR (wind_direction_deg >= 292.5 AND wind_direction_deg <= 337.5)
    ORDER BY observation_timestamp ASC
""")
nw_winds = cursor.fetchall()
print(f"Weather records with NW winds: {len(nw_winds)}")
if nw_winds:
    print("Sample NW wind records:")
    for w in nw_winds[:5]:
        print(f"ID {w[0]} | Time: {w[1]} | Speed: {w[2]} km/h | Dir: {w[3]}° ({w[4]}) | Class: {w[5]} | Provider: {w[6]}")

print("================================================================================")
print("5. NASA VIIRS DATA IN DATABASE OR CODEBASE")
print("================================================================================")
# Check all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cursor.fetchall()]
print("Database tables:", tables)

# Check if VIIRS is mentioned in research_documents or research_findings
cursor.execute("SELECT id, title, organisation, key_findings FROM research_documents WHERE key_findings LIKE '%VIIRS%' OR title LIKE '%VIIRS%'")
viirs_docs = cursor.fetchall()
print("Research documents mentioning VIIRS:", viirs_docs)

cursor.execute("SELECT id, title, statement, evidence_data FROM research_findings WHERE statement LIKE '%VIIRS%' OR title LIKE '%VIIRS%'")
viirs_findings = cursor.fetchall()
print("Research findings mentioning VIIRS:", viirs_findings)

# Check if Jalan is mentioned in research_documents or research_findings
cursor.execute("SELECT id, title, key_findings FROM research_documents WHERE key_findings LIKE '%Jalan%' OR title LIKE '%Jalan%'")
jalan_docs = cursor.fetchall()
print("Research documents mentioning Jalan:", jalan_docs)

cursor.execute("SELECT id, title, statement FROM research_findings WHERE statement LIKE '%Jalan%' OR title LIKE '%Jalan%'")
jalan_findings = cursor.fetchall()
print("Research findings mentioning Jalan:", jalan_findings)

conn.close()
