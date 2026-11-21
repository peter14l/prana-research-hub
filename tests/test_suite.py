"""
Automated Test Suite for PRANA Research Hub
Tests:
1. CPCB NAQI calculation & breakpoints
2. Spatial Haversine distance & coverage gap detection
3. Correlation engine & scientific non-causal disclaimer
4. FastAPI endpoint responses across all modules
"""
import unittest
from fastapi.testclient import TestClient
from backend.main import app
from backend.services.aqi_engine import calculate_cpcb_aqi, calculate_sub_index
from backend.services.hotspot_engine import haversine_km, HotspotEngine
from backend.services.analytics_engine import AnalyticsEngine

class TestPranaResearchHub(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_cpcb_sub_index_pm25(self):
        # 15 ug/m3 -> 0-50 range -> 25
        self.assertEqual(calculate_sub_index("PM2.5", 15.0), 25)
        # 60 ug/m3 -> Satisfactory limit -> 100
        self.assertEqual(calculate_sub_index("PM2.5", 60.0), 100)
        # 120 ug/m3 -> Poor limit -> 300
        self.assertEqual(calculate_sub_index("PM2.5", 120.0), 300)

    def test_cpcb_validity_rule(self):
        # Rule: Minimum 3 pollutants with at least one PM parameter
        # Case A: Only 2 pollutants -> Insufficient
        res_invalid = calculate_cpcb_aqi({"PM2.5": 80.0, "NO2": 45.0})
        self.assertFalse(res_invalid["is_valid_cpcb"])
        self.assertIsNone(res_invalid["aqi"])

        # Case B: 3 gaseous pollutants without PM -> Insufficient
        res_no_pm = calculate_cpcb_aqi({"NO2": 50.0, "SO2": 20.0, "CO": 1.2})
        self.assertFalse(res_no_pm["is_valid_cpcb"])

        # Case C: 3 pollutants with PM2.5 -> Valid CPCB AQI
        res_valid = calculate_cpcb_aqi({"PM2.5": 85.0, "PM10": 160.0, "NO2": 42.0})
        self.assertTrue(res_valid["is_valid_cpcb"])
        self.assertIsNotNone(res_valid["aqi"])
        self.assertEqual(res_valid["dominant_pollutant"], "PM2.5")

    def test_spatial_haversine(self):
        # Distance between Victoria Memorial (22.5448, 88.3426) and Fort William (22.5535, 88.3378)
        dist = haversine_km(22.5448, 88.3426, 22.5535, 88.3378)
        self.assertAlmostEqual(dist, 1.09, delta=0.2)

    def test_correlation_caveat(self):
        xs = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0]
        ys = [100.0, 90.0, 80.0, 70.0, 60.0, 50.0, 40.0, 30.0, 20.0, 10.0]
        res = AnalyticsEngine.calculate_bivariate_correlation(xs, ys, "PM2.5", "PBLH")
        self.assertTrue(res["is_significant"])
        self.assertEqual(res["pearson_r"], -1.0)
        self.assertIn("DOES NOT prove direct physical or chemical causation", res["scientific_caveat"])

    def test_api_endpoints(self):
        # 1. Overview Summary
        res = self.client.get("/api/overview/summary")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("pm25_avg", data)
        self.assertIn("highlights", data)

        # 2. Live Stations
        res = self.client.get("/api/live/stations")
        self.assertEqual(res.status_code, 200)
        stations = res.json()
        self.assertGreaterEqual(len(stations), 9)

        # 3. Hotspots Zones
        res = self.client.get("/api/hotspots/zones")
        self.assertEqual(res.status_code, 200)
        zones = res.json()
        self.assertGreaterEqual(len(zones), 9)

        # 4. Source Studies
        res = self.client.get("/api/sources/studies")
        self.assertEqual(res.status_code, 200)

        # 5. Weather Current
        res = self.client.get("/api/weather/current")
        self.assertEqual(res.status_code, 200)

        # 6. Research Documents
        res = self.client.get("/api/library/documents")
        self.assertEqual(res.status_code, 200)

        # 7. Intervention Hypotheses
        res = self.client.get("/api/interventions/hypotheses")
        self.assertEqual(res.status_code, 200)

        # 8. Data Quality Audit
        res = self.client.get("/api/quality/audit")
        self.assertEqual(res.status_code, 200)

        # 9. AI Assistant Query
        res = self.client.post("/api/assistant/query", json={"query": "Why is PM2.5 high at Ghusuri?"})
        self.assertEqual(res.status_code, 200)
        self.assertIn("response", res.json())

        # 10. Research Report Export
        res = self.client.get("/api/export/report")
        self.assertEqual(res.status_code, 200)
        self.assertIn("PRANA Research Hub", res.text)

if __name__ == "__main__":
    unittest.main()
