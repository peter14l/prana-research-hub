"""
PRANA Research Hub - Milestone 2 Test Suite
Automated Verification for:
1. Provenance assignment & SHA-256 hashing
2. Data classification tiers (VERIFIED, IMPORTED, DERIVED, DEMO, UNVERIFIED)
3. Duplicate detection
4. Missing observation detection
5. Completeness calculations with explicit numerator/denominator
6. Station verification registry & CPCB Site IDs
7. Stale data detection
8. Research citation & traceability requirements
"""

import unittest
from datetime import datetime, timedelta
import io
from fastapi.testclient import TestClient

from backend.main import app
from backend.services.data_quality_engine import DataQualityEngine
from backend.database import SessionLocal
from backend.models.models import ValidatedObservation

class DummyStation:
    def __init__(self, id, latest_timestamp=None):
        self.id = id
        self.latest_timestamp = latest_timestamp

class TestMilestone2ScientificIntegrity(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.db = SessionLocal()

    def tearDown(self):
        self.db.close()

    def test_1_provenance_assignment_and_hashing(self):
        """Verify that imported observations receive provenance hash, classification, and provider fields."""
        csv_content = (
            "station_code,pollutant,value,unit,timestamp\n"
            "WB001_VICTORIA,PM2.5,74.5,ug/m3,2026-11-21 12:00:00\n"
            "WB001_VICTORIA,PM10,142.0,ug/m3,2026-11-21 12:00:00\n"
        )
        file_obj = io.BytesIO(csv_content.encode('utf-8'))
        response = self.client.post(
            "/api/quality/import-csv",
            files={"file": ("test_import.csv", file_obj, "text/csv")},
            data={"provider_code": "TEST_WBPCB_AUDIT", "classification": "IMPORTED"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["records_processed"], 2)
        self.assertEqual(data["classification"], "IMPORTED")
        self.assertEqual(data["provider_code"], "TEST_WBPCB_AUDIT")
        # Verify SHA-256 hex string length
        self.assertIn("provenance_fingerprint", data)
        self.assertEqual(len(data["provenance_fingerprint"]), 64)

        # Inspect DB record for provenance fields
        obs = self.db.query(ValidatedObservation).filter(
            ValidatedObservation.original_data_provider == "TEST_WBPCB_AUDIT"
        ).order_by(ValidatedObservation.id.desc()).first()
        self.assertIsNotNone(obs)
        self.assertEqual(obs.data_classification, "IMPORTED")
        self.assertEqual(obs.original_station_id, "WB001_VICTORIA")
        self.assertIsNotNone(obs.provenance_hash)
        self.assertGreaterEqual(len(obs.provenance_hash), 16)

    def test_2_data_classification_tiers(self):
        """Verify the 5 data classifications and ensure seed data is strictly marked as DEMO."""
        response = self.client.get("/api/quality/integrity-summary")
        self.assertEqual(response.status_code, 200)
        summary = response.json()
        
        self.assertIn("counts", summary)
        self.assertIn("percentages", summary)
        
        # Verify all 5 scientific classification tiers are represented
        for tier in ["VERIFIED", "IMPORTED", "DERIVED", "DEMO", "UNVERIFIED"]:
            self.assertIn(tier, summary["counts"])
            self.assertIn(tier, summary["percentages"])
            
        # Baseline seed observations must be classified as DEMO (synthetic baseline)
        self.assertGreater(summary["counts"]["DEMO"], 0)
        self.assertGreater(summary["percentages"]["DEMO"], 50.0)

    def test_3_duplicate_detection(self):
        """Verify that duplicate observations (same station, pollutant, timestamp) are detected."""
        now = datetime.utcnow()
        mock_observations = [
            ValidatedObservation(station_id=1, pollutant="PM2.5", observation_timestamp=now, normalized_value=50.0, unit="ug/m3"),
            ValidatedObservation(station_id=1, pollutant="PM2.5", observation_timestamp=now, normalized_value=50.0, unit="ug/m3"), # Duplicate
            ValidatedObservation(station_id=1, pollutant="PM10", observation_timestamp=now, normalized_value=110.0, unit="ug/m3"),
            ValidatedObservation(station_id=2, pollutant="PM2.5", observation_timestamp=now, normalized_value=65.0, unit="ug/m3"),
        ]
        
        duplicates = DataQualityEngine.detect_duplicates(mock_observations)
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(duplicates[0]["pollutant"], "PM2.5")
        self.assertEqual(duplicates[0]["station_id"], 1)

    def test_4_missing_data_detection(self):
        """Verify that gaps in hourly time series are correctly identified."""
        base_time = datetime(2026, 11, 20, 0, 0, 0)
        # Sequence with missing hour at 02:00:00
        timestamps = [
            base_time,
            base_time + timedelta(hours=1),
            # Missing: base_time + timedelta(hours=2)
            base_time + timedelta(hours=3),
            base_time + timedelta(hours=4),
        ]
        
        missing = DataQualityEngine.detect_missing_observations(
            timestamps=timestamps,
            start_time=base_time,
            end_time=base_time + timedelta(hours=4),
            expected_interval_hours=1
        )
        self.assertEqual(len(missing), 1)
        self.assertEqual(missing[0], base_time + timedelta(hours=2))

    def test_5_completeness_calculations_with_formula(self):
        """Verify that completeness calculation returns exact numerator and denominator."""
        response = self.client.get("/api/quality/audit?hours_window=168")
        self.assertEqual(response.status_code, 200)
        audit = response.json()
        
        self.assertIn("completeness_details", audit)
        details = audit["completeness_details"]
        self.assertIn("received_valid_observations", details)
        self.assertIn("expected_observations_in_window", details)
        self.assertIn("formula", details)
        
        # Verify formula string
        self.assertIn("Completeness (%) = (Received Valid / Expected Observations) * 100", details["formula"])
        
        # Check station completeness items
        self.assertIn("station_completeness", audit)
        self.assertGreaterEqual(len(audit["station_completeness"]), 9)
        for st in audit["station_completeness"]:
            self.assertIn("received_records", st)
            self.assertIn("expected_records", st)
            self.assertIn("completeness_pct", st)
            self.assertGreater(st["expected_records"], 0)

    def test_6_station_verification_registry(self):
        """Verify all 9 stations have official CPCB Site IDs, coordinates, parameters, and verification links."""
        response = self.client.get("/api/quality/stations/verification")
        self.assertEqual(response.status_code, 200)
        stations = response.json()
        
        self.assertEqual(len(stations), 9)
        
        for st in stations:
            self.assertTrue(st["name"])
            self.assertTrue(st["cpcb_site_id"].startswith("site_"))
            self.assertEqual(st["verification_status"], "VERIFIED")
            self.assertTrue(st["verification_date"])
            self.assertTrue(st["verification_source_url"].startswith("http"))
            self.assertIn("PM2.5", st["verified_parameters"])
            self.assertGreater(st["latitude"], 22.0)
            self.assertGreater(st["longitude"], 88.0)

    def test_7_stale_data_detection(self):
        """Verify that stations with no recent readings (>24h) are flagged as stale."""
        now = datetime.utcnow()
        recent_station = DummyStation(id=101, latest_timestamp=now - timedelta(hours=2))
        stale_station = DummyStation(id=102, latest_timestamp=now - timedelta(hours=36))
        no_data_station = DummyStation(id=103, latest_timestamp=None)
        
        stale_list = DataQualityEngine.detect_stale_stations(
            [recent_station, stale_station, no_data_station],
            threshold_hours=24.0,
            current_time=now
        )
        stale_ids = [s["station_id"] for s in stale_list]
        self.assertIn(102, stale_ids)
        self.assertIn(103, stale_ids)
        self.assertNotIn(101, stale_ids)

    def test_8_research_citation_requirements(self):
        """Verify that every research finding and source apportionment profile contains verifiable citations."""
        # Check Research Findings
        res_findings = self.client.get("/api/sources/findings")
        self.assertEqual(res_findings.status_code, 200)
        findings = res_findings.json()
        self.assertGreaterEqual(len(findings), 4)
        
        for f in findings:
            self.assertTrue(f["title"])
            self.assertTrue(f["statement"])
            if f["has_supporting_reference"]:
                self.assertIsNotNone(f["citation_reference"])
                self.assertIsNotNone(f["page_number"])
                self.assertIsNotNone(f["table_figure_ref"])

        # Check Source Profiles
        res_profiles = self.client.get("/api/sources/profiles?city=Kolkata&season=Winter&pollutant=PM2.5")
        self.assertEqual(res_profiles.status_code, 200)
        profiles = res_profiles.json()
        self.assertGreater(len(profiles), 0)
        for p in profiles:
            self.assertTrue(p["has_supporting_reference"])
            self.assertIn("TERI", p["citation_reference"])
            self.assertIn("Table", p["table_figure_ref"])
            self.assertTrue(p["page_number"])

if __name__ == "__main__":
    unittest.main()
