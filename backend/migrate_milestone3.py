"""
PRANA Research Hub - Milestone 3 Database Migration
Safely adds:
1. openaq_location_id, last_observed_at to monitoring_stations
2. openaq_sensor_id to sensors
3. provider_code, error_details to ingestion_logs
4. creates saved_analyses table
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "prana.db")

def run_migration():
    print(f"Running Milestone 3 migration on {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. MonitoringStation columns
    cursor.execute("PRAGMA table_info(monitoring_stations)")
    existing_cols = [row[1] for row in cursor.fetchall()]
    
    if "openaq_location_id" not in existing_cols:
        cursor.execute("ALTER TABLE monitoring_stations ADD COLUMN openaq_location_id INTEGER")
        print("Added openaq_location_id to monitoring_stations")
    
    if "last_observed_at" not in existing_cols:
        cursor.execute("ALTER TABLE monitoring_stations ADD COLUMN last_observed_at DATETIME")
        print("Added last_observed_at to monitoring_stations")

    # 2. Sensor columns
    cursor.execute("PRAGMA table_info(sensors)")
    existing_sensor_cols = [row[1] for row in cursor.fetchall()]
    if "openaq_sensor_id" not in existing_sensor_cols:
        cursor.execute("ALTER TABLE sensors ADD COLUMN openaq_sensor_id INTEGER")
        print("Added openaq_sensor_id to sensors")

    # 3. IngestionLog columns
    cursor.execute("PRAGMA table_info(ingestion_logs)")
    existing_log_cols = [row[1] for row in cursor.fetchall()]
    if "provider_code" not in existing_log_cols:
        cursor.execute("ALTER TABLE ingestion_logs ADD COLUMN provider_code VARCHAR(50)")
        print("Added provider_code to ingestion_logs")
    if "error_details" not in existing_log_cols:
        cursor.execute("ALTER TABLE ingestion_logs ADD COLUMN error_details TEXT")
        print("Added error_details to ingestion_logs")

    # 4. Create saved_analyses table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(200) NOT NULL,
        description TEXT,
        author VARCHAR(100) DEFAULT 'PRANA Environmental Researcher',
        pollutant VARCHAR(20) NOT NULL,
        station_ids JSON NOT NULL,
        date_range_start DATETIME,
        date_range_end DATETIME,
        met_variables JSON,
        methodology TEXT,
        source_references TEXT,
        analysis_results JSON,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    print("Created or verified saved_analyses table")

    # 5. Populate initial OpenAQ location mappings for known stations
    # Victoria Memorial: OpenAQ ID 910
    # Rabindra Bharati University: OpenAQ ID 716 / 6310
    # Padmapukur Howrah: OpenAQ ID 5614
    cursor.execute("UPDATE monitoring_stations SET openaq_location_id = 910 WHERE station_code = 'WB001_VICTORIA'")
    cursor.execute("UPDATE monitoring_stations SET openaq_location_id = 716 WHERE station_code = 'WB003_RBU'")
    cursor.execute("UPDATE monitoring_stations SET openaq_location_id = 5614 WHERE station_code = 'WB009_PADMAPUKUR'")

    # Update OpenAQ provider status to CONNECTED since valid API key is now configured
    cursor.execute("""
        UPDATE data_providers 
        SET connection_status = 'CONNECTED', 
            retrieval_method = 'REST_API_V3',
            last_error_message = NULL
        WHERE code = 'OPENAQ'
    """)

    conn.commit()
    conn.close()
    print("Milestone 3 database migration completed successfully.")

if __name__ == "__main__":
    run_migration()
