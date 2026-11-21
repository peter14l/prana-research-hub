"""
Unit Tests for PRANA Milestone 7: Dhapa Remote Fire Intelligence Proof of Concept
Verifies:
1. Dhapa Landfill AOI and buffer geometries, closed polygons, and metadata uncertainty.
2. Spatial containment and ray-casting point-in-polygon classification.
3. Satellite data ingestion with preserved provenance (NASA FIRMS & Landsat 8/9 STAC).
4. Temporal and seasonal aggregation.
5. Spatial density and recurring hotspot clustering.
6. Cloud cover limitation audits and monsoon blindness quantification.
7. Ground monitoring comparison and causality vs association distinction.
8. Spaceborne early-warning feasibility verdict and alternative engineering pathway.
9. FastAPI REST endpoints for the Dhapa fire intelligence module.
"""
import os
import json
import unittest
from fastapi.testclient import TestClient

from backend.main import app
from backend.services.dhapa_fire_service import DhapaFireService
from backend.services.dhapa_fire_analyzer import DhapaFireAnalyzer

class TestMilestone7DhapaFireIntelligence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.service = DhapaFireService()
        cls.analyzer = DhapaFireAnalyzer(cls.service)

    def test_01_aoi_geojson_validity(self):
        """Verifies Dhapa Landfill AOI GeoJSON geometry, closed polygons, and metadata uncertainty."""
        geojson_path = "backend/data/dhapa_fire/dhapa_aoi_and_buffers.geojson"
        self.assertTrue(os.path.exists(geojson_path), f"File {geojson_path} must exist.")
        
        with open(geojson_path, "r") as f:
            data = json.load(f)
            
        self.assertEqual(data.get("type"), "FeatureCollection")
        metadata = data.get("metadata", {})
        self.assertEqual(metadata.get("site_name"), "Dhapa Municipal Solid Waste Disposal Ground")
        self.assertEqual(metadata.get("core_area_hectares"), 58.4)
        self.assertEqual(metadata.get("boundary_uncertainty_meters"), 75.0)
        self.assertIn("boundary_source", metadata)
        
        features = data.get("features", [])
        feature_ids = [f.get("properties", {}).get("id") for f in features]
        self.assertIn("DHAPA_CORE_AOI", feature_ids)
        self.assertIn("DHAPA_1KM_BUFFER", feature_ids)
        self.assertIn("DHAPA_2KM_BUFFER", feature_ids)
        self.assertIn("DHAPA_CENTROID_POINT", feature_ids)
        
        # Verify polygon coordinate closure
        for f in features:
            if f.get("geometry", {}).get("type") == "Polygon":
                coords = f["geometry"]["coordinates"][0]
                self.assertGreaterEqual(len(coords), 4)
                self.assertEqual(coords[0], coords[-1], "Polygon must be closed (first coordinate equals last).")

    def test_02_spatial_containment_and_classification(self):
        """Verifies Point-in-Polygon and Haversine buffer classification."""
        centroid_lat, centroid_lon = self.service.centroid
        
        # Centroid point must be inside CORE_AOI
        zone_core = self.service.classify_zone(centroid_lat, centroid_lon)
        self.assertEqual(zone_core, "CORE_AOI")
        
        # Point 0.8 km north
        zone_1km = self.service.classify_zone(centroid_lat + 0.007, centroid_lon)
        self.assertIn(zone_1km, ["CORE_AOI", "BUFFER_1KM"])
        
        # Point 1.6 km east
        zone_2km = self.service.classify_zone(centroid_lat, centroid_lon + 0.015)
        self.assertIn(zone_2km, ["BUFFER_1KM", "BUFFER_2KM"])
        
        # Point 10 km away in Kolkata
        zone_kol = self.service.classify_zone(22.60, 88.35)
        self.assertEqual(zone_kol, "GREATER_KOLKATA")
        
        # Point far away
        zone_reg = self.service.classify_zone(28.6139, 77.2090) # Delhi
        self.assertEqual(zone_reg, "REGIONAL")

    def test_03_satellite_data_provenance_preservation(self):
        """Verifies that all satellite thermal detections preserve complete provenance fields."""
        detections = self.service.get_detections()
        self.assertGreater(len(detections), 0, "Detections list must not be empty.")
        
        required_fields = [
            "detection_id", "latitude", "longitude", "acq_date", "acq_time",
            "satellite", "instrument", "confidence_label", "confidence_percent",
            "brightness_kelvin", "frp_mw", "spatial_resolution_m", "zone",
            "distance_to_dhapa_km", "source_product", "source_url", "verification_status"
        ]
        
        for d in detections[:10]:
            for field in required_fields:
                self.assertIn(field, d, f"Detection {d.get('detection_id')} missing field {field}")
                self.assertIsNotNone(d[field], f"Field {field} must not be None")
                
        # Check Landsat metadata
        landsat = self.service.get_landsat_scenes()
        self.assertGreater(len(landsat), 0)
        for s in landsat[:5]:
            self.assertIn("scene_id", s)
            self.assertIn("cloud_cover_pct", s)
            self.assertIn("path_row", s)

    def test_04_temporal_and_seasonal_aggregation(self):
        """Verifies aggregation by day, month, year, and season."""
        temporal = self.analyzer.analyze_temporal_distribution()
        self.assertIn("total_detections", temporal)
        self.assertIn("core_aoi_detections", temporal)
        self.assertIn("by_year", temporal)
        self.assertIn("by_month", temporal)
        self.assertIn("by_season", temporal)
        self.assertIn("peak_fire_season", temporal)
        
        # Total must match sum of season counts
        season_sum = sum(temporal["by_season"].values())
        self.assertEqual(season_sum, temporal["total_detections"])

    def test_05_spatial_density_and_hotspot_clustering(self):
        """Verifies detection density per km2 and recurring hotspot identification."""
        spatial = self.analyzer.analyze_spatial_clustering()
        self.assertIn("density_per_sq_km", spatial)
        self.assertIn("CORE_AOI", spatial["density_per_sq_km"])
        self.assertIn("BUFFER_1KM", spatial["density_per_sq_km"])
        self.assertIn("BUFFER_2KM", spatial["density_per_sq_km"])
        
        # Core AOI density must be positive and non-zero
        self.assertGreater(spatial["density_per_sq_km"]["CORE_AOI"], 0.0)
        
        # Hotspot clusters
        clusters = spatial.get("hotspot_clusters", [])
        self.assertGreater(len(clusters), 0, "Must identify at least one recurring hotspot in Dhapa.")
        self.assertEqual(clusters[0]["recurrence_classification"], "RECURRING_ACUTE_HOTSPOT")
        self.assertLessEqual(clusters[0]["cluster_radius_meters"], 500)

    def test_06_cloud_cover_and_monsoon_blindness(self):
        """Verifies cloud cover limitations and monsoon blindness quantification."""
        cloud_audit = self.analyzer.analyze_cloud_limitations()
        self.assertIn("obscuration_rate_percent", cloud_audit)
        self.assertIn("monsoon_average_cloud_cover_pct", cloud_audit)
        self.assertGreaterEqual(cloud_audit["monsoon_average_cloud_cover_pct"], 75.0, "Monsoon cloud cover must exceed 75%.")
        self.assertEqual(cloud_audit["monsoon_blindness_assessment"], "COMPLETE_BLINDNESS_JUNE_TO_SEPTEMBER")

    def test_07_ground_comparison_and_causality_audit(self):
        """Verifies nearby ground station comparison and strict causality vs association audit."""
        ground = self.analyzer.compare_with_prana_ground_data()
        stations = ground.get("nearest_stations", [])
        self.assertGreaterEqual(len(stations), 2)
        
        # Nearest station must be Bidhannagar at ~4.25 km
        bidhannagar = next((s for s in stations if "BIDHANNAGAR" in s["station_code"]), None)
        self.assertIsNotNone(bidhannagar)
        self.assertAlmostEqual(bidhannagar["distance_to_dhapa_km"], 4.25, delta=0.5)
        
        causality = ground.get("causality_audit", {})
        self.assertTrue(causality.get("temporal_association_observed"))
        self.assertFalse(causality.get("causal_attribution_defensible"), "Causal attribution to Dhapa must be flagged indefensible.")
        self.assertGreaterEqual(len(causality.get("scientific_rationale", [])), 2)

    def test_08_early_warning_feasibility_verdict(self):
        """Verifies the definitive scientific verdict on spaceborne early-warning feasibility."""
        verdict = self.analyzer.evaluate_spaceborne_early_warning_feasibility()
        self.assertEqual(verdict["verdict"], "INSUFFICIENT_FOR_SPACEBORNE_EARLY_WARNING")
        self.assertIn("critical_failure_modes", verdict)
        self.assertGreaterEqual(len(verdict["critical_failure_modes"]), 4)
        
        # Must recommend ground-based radiometric LWIR PTZ
        pathway = verdict.get("defensible_alternative_engineering_pathway", {})
        self.assertIn("LWIR", pathway.get("recommended_technology", ""))

    def test_09_api_endpoints_http_200(self):
        """Verifies that all Dhapa Fire Intelligence FastAPI endpoints return HTTP 200."""
        endpoints = [
            "/api/dhapa-fire/aoi",
            "/api/dhapa-fire/summary",
            "/api/dhapa-fire/detections",
            "/api/dhapa-fire/spatial-analysis",
            "/api/dhapa-fire/temporal-analysis",
            "/api/dhapa-fire/confidence-distribution",
            "/api/dhapa-fire/cloud-limitations",
            "/api/dhapa-fire/ground-comparison",
            "/api/dhapa-fire/feasibility-verdict"
        ]
        
        for ep in endpoints:
            resp = self.client.get(ep)
            self.assertEqual(resp.status_code, 200, f"Endpoint {ep} failed with status {resp.status_code}: {resp.text}")

if __name__ == "__main__":
    unittest.main()
