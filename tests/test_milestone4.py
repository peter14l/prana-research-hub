"""
PRANA Research Hub - Milestone 4 Test Suite:
Automated testing for Opportunity Discovery, 8-Criteria Scoring Engine,
Stage-Gate Lifecycle Governance, Research Gap Detection, and AI Opportunity Analysis.
"""
import unittest
import json
from datetime import datetime
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import SessionLocal
from backend.models.models import CandidateOpportunity, ResearchGap
from backend.services.opportunity_engine import OpportunityEngine
from backend.services.gap_detector import ResearchGapDetector
from backend.models.schemas import EvaluationWeights

class TestMilestone4Opportunities(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.db = SessionLocal()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def test_01_candidate_model_integrity_and_14_fields(self):
        """Verify that candidate opportunities have all 14 required engineering fields."""
        c = self.db.query(CandidateOpportunity).first()
        self.assertIsNotNone(c, "At least one candidate opportunity must exist in DB.")
        
        # Verify 14 mandatory fields
        required_fields = [
            "problem_statement", "target_pollutant", "suspected_source",
            "supporting_evidence", "geographic_relevance", "proposed_mechanism",
            "potential_users", "required_technology", "development_complexity",
            "potential_partners", "verification_method", "unresolved_questions",
            "key_risks", "ip_opportunity"
        ]
        for f in required_fields:
            val = getattr(c, f, None)
            self.assertTrue(val and len(str(val).strip()) >= 3, f"Candidate field {f} must be non-empty.")

    def test_02_evidence_inventory_synthesis(self):
        """Verify that evidence inventory compiles ground observations, stations, and studies."""
        inventory = OpportunityEngine.build_evidence_inventory(self.db)
        self.assertIn("total_records_cataloged", inventory)
        self.assertIn("observation_breakdown_by_classification", inventory)
        self.assertIn("station_registry", inventory)
        self.assertIn("datasets", inventory)
        self.assertIn("disclosed_data_gaps", inventory)
        self.assertGreater(inventory["station_registry"]["verified_statutory_stations"], 0)
        self.assertGreater(len(inventory["disclosed_data_gaps"]), 0)

    def test_03_sector_evaluations_independent(self):
        """Verify that all 8 pollution sectors are evaluated independently with local evidence."""
        sectors = OpportunityEngine.evaluate_sectors(self.db)
        self.assertEqual(len(sectors), 8, "Must independently evaluate exactly 8 sectors.")
        
        sector_names = [s["sector"] for s in sectors]
        expected_sectors = [
            "Industrial emissions", "Road transport", "Waste burning", "River transport",
            "Construction and road dust", "Domestic and commercial combustion",
            "Regional pollution transport", "Other documented sources"
        ]
        for exp in expected_sectors:
            self.assertIn(exp, sector_names, f"Sector '{exp}' must be evaluated.")
            
        for s in sectors:
            self.assertIn("winter_pm25_share", s)
            self.assertIn("primary_chemical_markers", s)
            self.assertIn("spatial_hotspots", s)
            self.assertIn("evidence_strength", s)

    def test_04_multi_criteria_scoring_and_ranking(self):
        """Verify that candidate evaluation produces ranked list with 8 criteria."""
        candidates = OpportunityEngine.evaluate_candidates(self.db)
        self.assertGreaterEqual(len(candidates), 3, "PRANA must produce approximately 3-5 candidates.")
        
        for idx, c in enumerate(candidates):
            self.assertEqual(c["rank"], idx + 1, "Candidates must be sequentially ranked.")
            self.assertGreaterEqual(c["weighted_priority_score"], 1.0)
            self.assertLessEqual(c["weighted_priority_score"], 10.0)
            
            # Check individual 8 criteria scores
            for crit in [
                "pollution_impact_score", "evidence_strength_score", "technical_feasibility_score",
                "financial_feasibility_score", "verification_score", "scalability_score",
                "innovation_score", "partnership_feasibility_score"
            ]:
                self.assertGreaterEqual(c[crit], 1.0)
                self.assertLessEqual(c[crit], 10.0)

    def test_05_dynamic_weights_normalization(self):
        """Verify that custom weights are normalized and dynamically adjust rankings."""
        # Weighting emphasizing technical and financial feasibility over impact
        custom_w = EvaluationWeights(
            pollution_impact=0.05,
            evidence_strength=0.10,
            technical_feasibility=0.35,
            financial_feasibility=0.35,
            verification=0.05,
            scalability=0.05,
            innovation=0.02,
            partnership_feasibility=0.03
        )
        scored = OpportunityEngine.evaluate_candidates(self.db, weights=custom_w)
        top_cand = scored[0]
        # Under feasibility-heavy weighting, fence-line network should rank top
        self.assertEqual(top_cand["slug"], "industrial-fence-line-attribution")

    def test_06_evaluate_endpoint_heuristic_disclaimer(self):
        """Verify API /api/opportunities/evaluate includes statutory non-measurement disclaimer."""
        res = self.client.post("/api/opportunities/evaluate", json={
            "weights": {
                "pollution_impact": 0.25,
                "evidence_strength": 0.20,
                "technical_feasibility": 0.15,
                "financial_feasibility": 0.10,
                "verification": 0.15,
                "scalability": 0.05,
                "innovation": 0.05,
                "partnership_feasibility": 0.05
            }
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("disclaimer", data)
        self.assertIn("prioritization heuristic", data["disclaimer"].lower())
        self.assertIn("candidates", data)

    def test_07_stage_gate_blocks_evidence_reviewed_without_citations(self):
        """Stage-Gate rule: Cannot advance to 'Evidence reviewed' without supporting citations."""
        c = self.db.query(CandidateOpportunity).filter(
            CandidateOpportunity.slug == "hooghly-ferry-exhaust-retrofit"
        ).first()
        self.assertIsNotNone(c)
        c.stage_status = "Under research"
        self.db.commit()

        # Attempt to advance to "Evidence reviewed" with empty citation
        res = self.client.post(f"/api/opportunities/candidates/{c.id}/stage", json={
            "target_stage": "Evidence reviewed",
            "notes": "Testing empty citation gate",
            "supporting_evidence_reference": ""
        })
        self.assertEqual(res.status_code, 400)
        self.assertIn("Stage-Gate Violation", res.json()["detail"])

    def test_08_stage_gate_blocks_pilot_validated_without_dataset(self):
        """Stage-Gate rule: Cannot advance to 'Pilot validated' without empirical verification dataset."""
        c = self.db.query(CandidateOpportunity).filter(
            CandidateOpportunity.slug == "howrah-foundry-cupola-retrofit"
        ).first()
        self.assertIsNotNone(c)
        c.stage_status = "Pilot ready"
        self.db.commit()

        # Attempt to mark validated without dataset reference
        res = self.client.post(f"/api/opportunities/candidates/{c.id}/stage", json={
            "target_stage": "Pilot validated",
            "notes": "Prototype deployed in shed",
            "supporting_evidence_reference": "TERI 2025",
            "verification_dataset_reference": ""
        })
        self.assertEqual(res.status_code, 400)
        self.assertIn("Stage-Gate Violation", res.json()["detail"])

    def test_09_stage_gate_advancement_success_with_audit(self):
        """Verify successful stage-gate advancement with audit history logging."""
        c = self.db.query(CandidateOpportunity).filter(
            CandidateOpportunity.slug == "hooghly-ferry-exhaust-retrofit"
        ).first()
        self.assertIsNotNone(c)

        res = self.client.post(f"/api/opportunities/candidates/{c.id}/stage", json={
            "target_stage": "Evidence reviewed",
            "notes": "Completed waterfront commuter exposure and TERI 2025 review",
            "supporting_evidence_reference": "TERI 2025 Section 3.4 & WBSTC Fleet Inventory"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["current_stage"], "Evidence reviewed")
        self.assertGreater(data["history_length"], 0)

    def test_10_shortlist_decision_governance(self):
        """Verify shortlisting decision workflow updates database status and notes."""
        c = self.db.query(CandidateOpportunity).first()
        self.assertIsNotNone(c)

        res = self.client.post(f"/api/opportunities/candidates/{c.id}/shortlist", json={
            "status": "SHORTLISTED",
            "notes": "Approved by PRANA Research Council for detailed engineering study."
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["shortlist_status"], "SHORTLISTED")
        self.assertEqual(data["shortlist_notes"], "Approved by PRANA Research Council for detailed engineering study.")

    def test_11_research_gap_detector_catalog_and_severity(self):
        """Verify research gap catalog retrieval and severity filtering."""
        gaps = ResearchGapDetector.get_all_gaps(self.db)
        self.assertGreaterEqual(len(gaps), 4, "Must identify multiple research gaps.")
        
        # Verify critical gap exists
        critical_gaps = ResearchGapDetector.get_all_gaps(self.db, severity="CRITICAL")
        self.assertGreater(len(critical_gaps), 0)
        self.assertIn("Jalan", critical_gaps[0]["title"])
        self.assertTrue(critical_gaps[0]["remote_testing_possible"])

    def test_12_research_gap_programmatic_audit(self):
        """Verify research gap audit identifies unmonitored zones and low-cost resolutions."""
        audit = ResearchGapDetector.perform_gap_audit(self.db)
        self.assertIn("unmonitored_geographic_voids", audit)
        self.assertIn("sectoral_inventory_deficits", audit)
        self.assertIn("cheapest_credible_next_steps", audit)
        
        void_zones = [v["zone"] for v in audit["unmonitored_geographic_voids"]]
        self.assertTrue(any("Jalan" in z for z in void_zones))
        self.assertTrue(any("Khidirpur" in z for z in void_zones))

    def test_13_ai_assistant_opportunity_analysis_and_contradictions(self):
        """Verify AI assistant analyzes opportunities, explains ranking, and resolves contradictions."""
        res = self.client.post("/api/assistant/query", json={
            "query": "Compare our candidate opportunities and explain why foundry retrofit ranks higher than ferry retrofit."
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("Foundry Cupola", data["response"])
        self.assertIn("34%", data["response"])
        self.assertIn("Contradiction", data["response"])
        self.assertGreater(len(data["citations"]), 0)

if __name__ == "__main__":
    unittest.main()
