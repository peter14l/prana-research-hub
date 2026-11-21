"""
PRANA Milestone 5 Unit Test Suite: Evidence Integrity & Opportunity Recalibration

Validates:
1. Jalan candidate corrections (8.56 km derived distance, no 2,000+ unit claim, no synthetic spike claims).
2. Zero-credit rule for synthetic, unverified, and missing evidence.
3. Opportunity evidence score recalibrations and pre-audit score preservation.
4. Ranking inversion: Foundry takes Rank #1 under authentic evidence.
5. Distinct evidence classifications and separation of 6 rebuilt dimensions.
"""

import unittest
from backend.database import SessionLocal
from backend.models.models import CandidateOpportunity, ResearchGap
from backend.services.opportunity_engine import (
    calculate_evidence_score_from_audit,
    evaluate_candidates,
    SUPPORTED_EVIDENCE_STATUSES,
)


class TestMilestone5EvidenceIntegrity(unittest.TestCase):
    def setUp(self):
        self.db = SessionLocal()

    def tearDown(self):
        self.db.close()

    def test_jalan_candidate_corrections(self):
        """Verify Jalan candidate corrections per Milestone 5 Section 1."""
        jalan = self.db.query(CandidateOpportunity).filter(
            CandidateOpportunity.slug == "industrial-fence-line-attribution"
        ).first()
        self.assertIsNotNone(jalan, "Jalan candidate opportunity must exist in database")

        # 1. 2,000+ industrial units claim removed
        self.assertNotIn("2,000", jalan.problem_statement)
        self.assertNotIn("2,000+", jalan.problem_statement)
        self.assertNotIn("2,000", jalan.title)

        # 2. Corrected monitoring distance to 8.56 km labelled DERIVED_RESULT
        self.assertEqual(jalan.derived_distance_km, 8.56)
        breakdown = jalan.evidence_audit_breakdown or []
        distance_items = [item for item in breakdown if "monitoring gap" in item.get("claim", "").lower() or "distance" in item.get("claim", "").lower()]
        self.assertTrue(len(distance_items) > 0, "Distance claim must be present in audit breakdown")
        self.assertEqual(distance_items[0].get("status"), "DERIVED_RESULT")

        # 3. Unsupported nocturnal Padmapukur spike removed / flagged
        spike_items = [item for item in breakdown if "180" in item.get("claim", "")]
        self.assertTrue(len(spike_items) > 0, "Spike claim must be explicitly audited")
        self.assertEqual(spike_items[0].get("status"), "SYNTHETIC_DATA")

        # 4. NW wind association reclassified as UNVERIFIED_HYPOTHESIS
        wind_items = [item for item in breakdown if "wind" in item.get("claim", "").lower()]
        self.assertTrue(len(wind_items) > 0, "Wind association must be audited")
        self.assertEqual(wind_items[0].get("status"), "UNVERIFIED_HYPOTHESIS")

        # 5. VIIRS anomaly claims flagged MISSING_EVIDENCE
        viirs_items = [item for item in breakdown if "viirs" in item.get("claim", "").lower()]
        self.assertTrue(len(viirs_items) > 0, "VIIRS claim must be audited")
        self.assertEqual(viirs_items[0].get("status"), "MISSING_EVIDENCE")

        # 6. Recalibrated evidence score
        self.assertEqual(jalan.evidence_strength_score, 3.5)
        self.assertEqual(jalan.pre_audit_evidence_score, 8.8)

    def test_zero_credit_rule_for_synthetic_and_missing_data(self):
        """Verify that synthetic data, unverified hypotheses, and missing evidence receive 0 credit."""
        # Test synthetic only gives 0
        synthetic_claims = [
            {"status": "SYNTHETIC_DATA", "support_type": "DIRECT_MEASUREMENT"},
            {"status": "UNVERIFIED_HYPOTHESIS", "support_type": "UNLINKED_DATASET"},
            {"status": "MISSING_EVIDENCE", "support_type": "UNFULFILLED_CITATION"},
        ]
        score = calculate_evidence_score_from_audit(synthetic_claims)
        self.assertEqual(score, 1.0, "Synthetic, unverified, and missing evidence must yield 0.0 additional credit above baseline")

        # Adding synthetic items to verified evidence does not inflate score
        verified_claims = [
            {"status": "PUBLISHED_RESEARCH", "support_type": "DIRECT_SUPPORT"},
        ]
        base_score = calculate_evidence_score_from_audit(verified_claims)
        self.assertGreater(base_score, 1.0)

        inflated_attempt = verified_claims + [
            {"status": "SYNTHETIC_DATA", "support_type": "DIRECT_SUPPORT"},
            {"status": "UNVERIFIED_HYPOTHESIS", "support_type": "DIRECT_SUPPORT"},
            {"status": "MISSING_EVIDENCE", "support_type": "DIRECT_SUPPORT"},
        ]
        inflated_score = calculate_evidence_score_from_audit(inflated_attempt)
        self.assertEqual(
            base_score,
            inflated_score,
            "Adding synthetic or unverified claims must not increase evidence score"
        )

    def test_distinct_evidence_classifications(self):
        """Verify all 6 distinct evidence classifications are supported."""
        expected_statuses = {
            "VERIFIED_OBSERVATION",
            "PUBLISHED_RESEARCH",
            "DERIVED_RESULT",
            "SYNTHETIC_DATA",
            "UNVERIFIED_HYPOTHESIS",
            "MISSING_EVIDENCE"
        }
        self.assertEqual(SUPPORTED_EVIDENCE_STATUSES, expected_statuses)

        # Ensure every candidate in DB uses only valid classifications
        candidates = self.db.query(CandidateOpportunity).all()
        for cand in candidates:
            breakdown = cand.evidence_audit_breakdown or []
            self.assertGreater(len(breakdown), 0, f"Candidate {cand.slug} must have audit breakdown")
            for item in breakdown:
                self.assertIn(
                    item["status"],
                    SUPPORTED_EVIDENCE_STATUSES,
                    f"Invalid status {item['status']} in candidate {cand.slug}"
                )

    def test_all_candidates_recalibrated_scores(self):
        """Verify recalibrated evidence scores across all 4 candidates."""
        expected_scores = {
            "howrah-foundry-cupola-retrofit": 6.8,
            "industrial-fence-line-attribution": 3.5,
            "landfill-fire-thermal-suppression": 4.2,
            "hooghly-ferry-exhaust-retrofit": 2.0,
        }
        for slug, expected in expected_scores.items():
            cand = self.db.query(CandidateOpportunity).filter(
                CandidateOpportunity.slug == slug
            ).first()
            self.assertIsNotNone(cand, f"Candidate {slug} must exist")
            self.assertEqual(
                cand.evidence_strength_score,
                expected,
                f"Candidate {slug} evidence score mismatch"
            )
            # Verify pre-audit scores preserved
            self.assertIsNotNone(cand.pre_audit_evidence_score)
            self.assertIsNotNone(cand.pre_audit_priority_score)

    def test_ranking_inversion(self):
        """Verify that under authentic evidence, Howrah Foundry ranks #1."""
        result = evaluate_candidates(self.db)
        candidates = result if isinstance(result, list) else result.get("candidates", [])
        self.assertGreaterEqual(len(candidates), 4)

        # Rank #1 must be Howrah Foundry
        self.assertEqual(
            candidates[0]["slug"],
            "howrah-foundry-cupola-retrofit",
            f"Expected Foundry at Rank #1, got {candidates[0]['slug']}"
        )
        self.assertEqual(candidates[0]["rank"], 1)

        # Rank #2 must be Fence-Line Attribution
        self.assertEqual(
            candidates[1]["slug"],
            "industrial-fence-line-attribution",
            f"Expected Fence-Line at Rank #2, got {candidates[1]['slug']}"
        )
        self.assertEqual(candidates[1]["rank"], 2)

    def test_rebuilt_6_dimensions(self):
        """Verify that 6 evaluation dimensions are separated from technical narrative."""
        candidates = self.db.query(CandidateOpportunity).all()
        required_dimensions = [
            "pollution_impact_potential",
            "evidence_strength",
            "engineering_feasibility",
            "prototype_affordability",
            "verification_feasibility",
            "partnership_feasibility"
        ]
        for cand in candidates:
            self.assertIsNotNone(cand.rebuilt_scores, f"Candidate {cand.slug} must have rebuilt_scores")
            for dim in required_dimensions:
                self.assertIn(dim, cand.rebuilt_scores, f"Missing dimension {dim} in {cand.slug}")
                val = cand.rebuilt_scores[dim]
                self.assertIsInstance(val, (int, float))
                self.assertGreaterEqual(val, 0.0)
                self.assertLessEqual(val, 10.0)

    def test_research_gap_gap001_updated(self):
        """Verify GAP-001 has no 2,500 units claim and specifies 8.56 km derived distance."""
        gap = self.db.query(ResearchGap).filter(ResearchGap.gap_code == "GAP-001").first()
        self.assertIsNotNone(gap)
        self.assertNotIn("2,500", gap.description)
        self.assertIn("8.56 km", gap.description)
        self.assertIn("derived", gap.description.lower())


if __name__ == "__main__":
    unittest.main()
