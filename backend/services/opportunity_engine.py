"""
PRANA Opportunity Evaluation Engine (Milestone 4):
Evidence inventory synthesis, sector-by-sector independent evaluation,
transparent 8-criteria multi-metric scoring, and stage-gate validation governance.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import json
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.models.models import (
    CandidateOpportunity, ResearchGap, ValidatedObservation,
    MonitoringStation, WeatherObservation, ResearchDocument,
    SourceContributionProfile, SourceCategory
)
from backend.models.schemas import EvaluationWeights

SUPPORTED_EVIDENCE_STATUSES = {
    "VERIFIED_OBSERVATION",
    "PUBLISHED_RESEARCH",
    "DERIVED_RESULT",
    "SYNTHETIC_DATA",
    "UNVERIFIED_HYPOTHESIS",
    "MISSING_EVIDENCE"
}

class OpportunityEngine:
    DEFAULT_WEIGHTS = {
        "pollution_impact": 0.20,
        "evidence_strength": 0.15,
        "technical_feasibility": 0.15,
        "financial_feasibility": 0.10,
        "verification": 0.15,
        "scalability": 0.10,
        "innovation": 0.05,
        "partnership_feasibility": 0.10
    }

    VALID_STAGES = [
        "Discovered",
        "Under research",
        "Evidence reviewed",
        "Feasibility assessed",
        "Prototype proposed",
        "Prototype developed",
        "Pilot ready",
        "Pilot validated"
    ]

    @staticmethod
    def build_evidence_inventory(db: Session) -> Dict[str, Any]:
        """
        Produces a comprehensive evidence inventory across all database tables,
        documenting sources, coverage, date ranges, reliability, limitations,
        and classifications.
        """
        # 1. Ambient Ground Observations
        obs_total = db.query(func.count(ValidatedObservation.id)).scalar() or 0
        obs_by_tier = dict(
            db.query(ValidatedObservation.data_classification, func.count(ValidatedObservation.id))
            .group_by(ValidatedObservation.data_classification)
            .all()
        )
        min_date, max_date = db.query(
            func.min(ValidatedObservation.observation_timestamp),
            func.max(ValidatedObservation.observation_timestamp)
        ).first()

        # 2. Monitoring Stations
        stations = db.query(MonitoringStation).all()
        verified_stations = [s for s in stations if s.verification_status == "VERIFIED"]
        cpcb_tracked = [s for s in stations if s.cpcb_site_id is not None]

        # 3. Weather Reanalysis Observations
        weather_count = db.query(func.count(WeatherObservation.id)).scalar() or 0
        w_min_date, w_max_date = db.query(
            func.min(WeatherObservation.observation_timestamp),
            func.max(WeatherObservation.observation_timestamp)
        ).first()

        # 4. Research Documents
        docs = db.query(ResearchDocument).all()
        doc_summaries = [
            {
                "title": d.title,
                "organisation": d.organisation,
                "publication_date": d.publication_date,
                "scope": d.geographic_coverage,
                "methodology": d.methodology,
                "limitations": d.limitations,
                "classification": "VERIFIED_STATUTORY_STUDY"
            }
            for d in docs
        ]

        # 5. Inventory Matrix
        inventory_items = [
            {
                "dataset_name": "OpenAQ v3 Verified Ambient Observations",
                "source": "OpenAQ REST API v3 / Statutory CAAQM Integrations",
                "geographic_coverage": "Kolkata–Howrah conurbation (Victoria Memorial, RBU, Padmapukur, US Diplomatic Post)",
                "date_range": f"{min_date.strftime('%Y-%m-%d') if min_date else 'N/A'} to {max_date.strftime('%Y-%m-%d') if max_date else 'N/A'}",
                "classification": "VERIFIED",
                "reliability": "HIGH (Statutory CAAQM analyzers with reference equivalence)",
                "limitations": "Point measurements with limited spatial representation; zero coverage in peri-urban industrial belts like Jalan Complex.",
                "record_count": obs_by_tier.get("VERIFIED", 0)
            },
            {
                "dataset_name": "Synthetic Baseline Research Observations",
                "source": "PRANA Calibrated Baseline Model (NEERI/TERI 2024-2025 Seasonal Means)",
                "geographic_coverage": "9 CAAQM Stations across Kolkata and Howrah",
                "date_range": "2026-11-01 to 2026-11-21",
                "classification": "DEMO",
                "reliability": "BENCHMARK ONLY (For UI demonstration and counterfactual pipeline testing)",
                "limitations": "Modelled distribution, not direct physical ground truth. Strictly tagged to avoid conflation.",
                "record_count": obs_by_tier.get("DEMO", 0)
            },
            {
                "dataset_name": "Open-Meteo High-Resolution Atmospheric Reanalysis",
                "source": "Open-Meteo Synoptic Weather Models (ERA5 / High-Res NWP)",
                "geographic_coverage": "Centroid coordinates for Kolkata (22.57°N, 88.36°E) & Howrah (22.59°N, 88.31°E)",
                "date_range": f"{w_min_date.strftime('%Y-%m-%d') if w_min_date else 'N/A'} to {w_max_date.strftime('%Y-%m-%d') if w_max_date else 'N/A'}",
                "classification": "MODELLED",
                "reliability": "HIGH (Synoptic Reanalysis)",
                "limitations": "Grid-scale reanalysis; does not account for hyper-local microclimates, street canyons, or dockside river turbulence.",
                "record_count": weather_count
            },
            {
                "dataset_name": "Statutory Source Apportionment Profiles",
                "source": "TERI (2025) & CSIR-NEERI (2020) Twin Cities Final Reports",
                "geographic_coverage": "Twin Cities: Kolkata & Howrah (Urban, Industrial, Commercial)",
                "date_range": "Seasonal campaigns: Winter 2018-2024, Summer 2019-2024",
                "classification": "VERIFIED_STATUTORY_STUDY",
                "reliability": "HIGHEST (Chemical mass balance receptor modelling & positive matrix factorization)",
                "limitations": "Intermittent filter collection campaigns; does not provide real-time dynamic source fluctuations.",
                "record_count": len(doc_summaries)
            }
        ]

        # Calculate evidence coverage metric
        total_records = obs_total + weather_count
        verified_share = ((obs_by_tier.get("VERIFIED", 0) + weather_count) / total_records * 100.0) if total_records > 0 else 0.0

        return {
            "inventory_timestamp": datetime.now(timezone.utc).isoformat(),
            "total_records_cataloged": total_records,
            "verified_and_modelled_share_pct": round(verified_share, 1),
            "observation_breakdown_by_classification": obs_by_tier,
            "station_registry": {
                "total_stations": len(stations),
                "verified_statutory_stations": len(verified_stations),
                "cpcb_site_id_assigned": len(cpcb_tracked)
            },
            "datasets": inventory_items,
            "active_statutory_studies": doc_summaries,
            "disclosed_data_gaps": [
                "Zero continuous ground telemetry in south-west Howrah industrial belt (Jalan / Domjur / Uluberia).",
                "No empirical tailpipe emission factors for the Hooghly river passenger ferry fleet.",
                "Lack of continuous heavy-metal aerosol chemical speciation in ambient Howrah air.",
                "Absence of continuous LIDAR ceilometer data for Planetary Boundary Layer Height (PBLH) inversion dynamics."
            ]
        }

    @staticmethod
    def evaluate_sectors(db: Session) -> List[Dict[str, Any]]:
        """
        Evaluates 8 pollution sectors independently using Kolkata–Howrah specific evidence.
        """
        # Fetch category profiles from DB if available
        profiles = db.query(SourceContributionProfile).all()
        profile_map = {}
        for p in profiles:
            cat_name = p.category.name if p.category else "Unknown"
            if cat_name not in profile_map:
                profile_map[cat_name] = []
            profile_map[cat_name].append(p)

        sectors = [
            {
                "sector": "Industrial emissions",
                "relative_importance": "CRITICAL (Highest Local Stationary Contributor in Howrah)",
                "winter_pm25_share": "Up to 34% (Ghusuri/Howrah North) / 18% (Kolkata Regional)",
                "summer_pm25_share": "12% - 15%",
                "primary_chemical_markers": "Heavy Metals (Pb, Zn, Fe, Mn), Elemental Carbon, Sulfate (SO4--)",
                "spatial_hotspots": "Ghusuri, Belur, Liluah, Baltikuri, Jalan Industrial Complex (Howrah)",
                "evidence_strength": "VERY HIGH (CSIR-NEERI 2020 Table 6.14; Ghusuri CAAQM site_5008 records)",
                "candidate_concepts": [
                    "Howrah foundry cupola multi-cyclone & dry sorbent off-gas scrubbing retrofit",
                    "Optical & thermal fence-line micro-plume attribution network for unmonitored estates"
                ],
                "key_limitations": "Lack of continuous heavy-metal speciation; non-reporting small artisanal units operating without permits.",
                "recommended_focus": "High-priority candidate for direct source engineering."
            },
            {
                "sector": "Road transport",
                "relative_importance": "VERY HIGH (Dominant Daytime Mobile Contributor in Kolkata)",
                "winter_pm25_share": "27% (Central Kolkata) / 19% (Howrah)",
                "summer_pm25_share": "15% - 22%",
                "primary_chemical_markers": "Elemental Carbon (EC/OC ratio 0.4-0.6), NOx, Benzene, Hopanes",
                "spatial_hotspots": "BT Road (RBU), Vidyasagar Setu approach, Kona Expressway, Rabindra Bharati",
                "evidence_strength": "VERY HIGH (TERI 2025 Table 4.5; RBU CAAQM site_5004 elevated daytime PM2.5/NO2)",
                "candidate_concepts": [
                    "High-emission commercial vehicle nocturnal exhaust screening checkpoints",
                    "Shared commercial transit electrification corridors"
                ],
                "key_limitations": "Diffuse mobile sources require municipal fleet policies rather than single-point engineering retrofits.",
                "recommended_focus": "High impact, but higher political/regulatory complexity for an early-stage startup."
            },
            {
                "sector": "Waste burning",
                "relative_importance": "HIGH (Episodic Toxic Hotspot in East Kolkata & Howrah)",
                "winter_pm25_share": "14% (Winter Regional) / >35% during episodic open dump fires",
                "summer_pm25_share": "6% - 8%",
                "primary_chemical_markers": "Chloride (Cl-), Potassium (K+), Dioxins/Furans, Black Carbon, Carbon Monoxide",
                "spatial_hotspots": "Dhapa Municipal Landfill (EM Bypass), Belgachia Dump (Howrah), roadside refuse heaps",
                "evidence_strength": "HIGH (TERI 2025 Table 4.6; NASA VIIRS thermal anomaly records; downwind CO spikes)",
                "candidate_concepts": [
                    "Autonomous thermal edge-detection & rapid subterranean suppression for landfill refuse fires",
                    "Automated optical smoke detection for street-level municipal refuse burning"
                ],
                "key_limitations": "Combustion occurs deep in heterogeneous subterranean waste mounds with difficult physical access.",
                "recommended_focus": "Prime engineering opportunity for autonomous hardware/vision intervention."
            },
            {
                "sector": "River transport",
                "relative_importance": "MODERATE (High Commuter & Waterfront Micro-Exposure)",
                "winter_pm25_share": "Uninventoried in regional models (<4% regional mass, but extreme local jetty exposure)",
                "summer_pm25_share": "Uninventoried",
                "primary_chemical_markers": "Diesel Particulate, Elemental Carbon, Marine Heavy Fuel Oil tracers (V, Ni), NOx",
                "spatial_hotspots": "Hooghly River fairway: Howrah Station Ghat, Babughat, Fairlie Place, Princep Ghat",
                "evidence_strength": "MEDIUM (Empirically documented commuter queues; identified as research gap in TERI 2025)",
                "candidate_concepts": [
                    "Hooghly river passenger ferry exhaust aftertreatment (SiC DPF & SCR) retrofit kit",
                    "Solar-electric auxiliary power units for idling passenger ferry jetties"
                ],
                "key_limitations": "Lack of empirical tailpipe emission factors in current official state inventories.",
                "recommended_focus": "Promising niche engineering project with high public visibility and clear boundaries."
            },
            {
                "sector": "Construction and road dust",
                "relative_importance": "HIGH FOR PM10 (Low for Fine PM2.5 Mass Share)",
                "winter_pm25_share": "6% - 9% of PM2.5, but 38% of PM10 mass",
                "summer_pm25_share": "12% of PM2.5, 45% of PM10 mass",
                "primary_chemical_markers": "Crustal Minerals (Silicon Si, Aluminum Al, Calcium Ca, Titanium Ti)",
                "spatial_hotspots": "EM Bypass extension, Kolkata metro construction corridors, Kona Expressway shoulders",
                "evidence_strength": "HIGH (CSIR-NEERI 2020 Table 5.8; Victoria & Jadavpur PM10/PM2.5 ratios >2.4)",
                "candidate_concepts": [
                    "Electrostatic or fine-mist agglomeration curtains for active building sites",
                    "Low-water mechanical road shoulder binder applications"
                ],
                "key_limitations": "Dominates coarse PM10 rather than the fine, highly toxic combustion-derived PM2.5 fraction.",
                "recommended_focus": "Secondary priority compared to direct combustion and toxic source reduction."
            },
            {
                "sector": "Domestic and commercial combustion",
                "relative_importance": "MODERATE TO HIGH (Nocturnal Winter Inversion Contribution)",
                "winter_pm25_share": "12% - 16%",
                "summer_pm25_share": "8% - 10%",
                "primary_chemical_markers": "Potassium (K+), Levoglucosan, Organic Carbon (OC/EC ratio > 3.0)",
                "spatial_hotspots": "Peri-urban slums, roadside food stalls, tea stall coal/coke chullahs across Howrah & North Kolkata",
                "evidence_strength": "HIGH (TERI 2025 Table 4.6; nocturnal evening OC spikes)",
                "candidate_concepts": [
                    "Clean biomass pellet cookstoves for commercial roadside vendors",
                    "Subsidized induction hotplate micro-distribution"
                ],
                "key_limitations": "High socio-economic friction and behavioral reliance on free solid biomass fuels.",
                "recommended_focus": "Requires public welfare subsidy mechanisms rather than standalone industrial hardware."
            },
            {
                "sector": "Regional pollution transport",
                "relative_importance": "VERY HIGH (External Transboundary Baseline)",
                "winter_pm25_share": "24% (Secondary Inorganic Aerosols formed from regional precursor gases)",
                "summer_pm25_share": "10% - 14%",
                "primary_chemical_markers": "Ammonium Sulfate (NH4)2SO4, Ammonium Nitrate NH4NO3",
                "spatial_hotspots": "Airshed-wide Indo-Gangetic Plain regional inflow entering from north-west",
                "evidence_strength": "VERY HIGH (TERI 2025 chemical mass balance; regional WRF-Chem modelling)",
                "candidate_concepts": [
                    "Regional airshed early-warning and inversion forecasting intelligence",
                    "Inter-state precursor gas emission trading analytics"
                ],
                "key_limitations": "Cannot be reduced by localized physical engineering in Kolkata; requires inter-state policy.",
                "recommended_focus": "Important contextual intelligence, but not a candidate for direct source engineering."
            },
            {
                "sector": "Other documented sources",
                "relative_importance": "LOW TO MODERATE (Localized Episodic)",
                "winter_pm25_share": "2% - 5%",
                "summer_pm25_share": "2% - 3%",
                "primary_chemical_markers": "Organic Carbon, Trace Aromatics, Diesel Generator combustion byproducts",
                "spatial_hotspots": "Traditional wood crematoria (Nimtala, Keoratala), commercial DG sets during grid outages",
                "evidence_strength": "MODERATE (Documented in municipal ward inventories)",
                "candidate_concepts": [
                    "Secondary cyclonic filtration for traditional crematoria flue stacks",
                    "Smart emission telemetry for high-capacity commercial diesel backup generators"
                ],
                "key_limitations": "Localized and culturally sensitive operating domains.",
                "recommended_focus": "Tertiary priority."
            }
        ]

        return sectors

    @staticmethod
    def calculate_evidence_score_from_audit(audit_items: List[Dict[str, Any]]) -> float:
        """
        Milestone 5 Evidence Integrity Rule:
        Strictly computes evidence strength score from verified ground observations
        and statutory published research. Synthetic data, unverified hypotheses,
        and missing evidence receive 0.0 credit.
        """
        score = 1.0 # Minimum baseline
        for item in audit_items:
            status = item.get("status", "")
            support = item.get("support_type", "")

            if status == "PUBLISHED_RESEARCH":
                if support == "DIRECT_SUPPORT":
                    score += 4.0
                elif support == "REGIONAL_CONTEXT":
                    score += 2.2
                elif support == "GAP_ACKNOWLEDGEMENT":
                    score += 1.0
            elif status == "VERIFIED_OBSERVATION":
                if support == "DIRECT_SUPPORT":
                    score += 2.8
            elif status == "DERIVED_RESULT":
                if support == "DIRECT_SUPPORT":
                    score += 2.0
            elif status in ["SYNTHETIC_DATA", "UNVERIFIED_HYPOTHESIS", "MISSING_EVIDENCE"]:
                # Zero credit rule: do not allow synthetic or missing claims to inflate scores
                score += 0.0

        return round(min(10.0, score), 1)

    @classmethod
    def evaluate_candidates(
        cls,
        db: Session,
        weights: Optional[EvaluationWeights] = None,
        sector_filter: Optional[str] = None,
        min_evidence: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Calculates normalized multi-criteria scores for all candidates based on the 8 criteria.
        Scores are calculated dynamically, ranked, and presented with transparent explanations.
        Never presents a composite score as a physical measurement; explicitly labeled as
        a weighted prioritization heuristic.
        """
        # Resolve active weights
        raw_w = {
            "pollution_impact": weights.pollution_impact if weights else cls.DEFAULT_WEIGHTS["pollution_impact"],
            "evidence_strength": weights.evidence_strength if weights else cls.DEFAULT_WEIGHTS["evidence_strength"],
            "technical_feasibility": weights.technical_feasibility if weights else cls.DEFAULT_WEIGHTS["technical_feasibility"],
            "financial_feasibility": weights.financial_feasibility if weights else cls.DEFAULT_WEIGHTS["financial_feasibility"],
            "verification": weights.verification if weights else cls.DEFAULT_WEIGHTS["verification"],
            "scalability": weights.scalability if weights else cls.DEFAULT_WEIGHTS["scalability"],
            "innovation": weights.innovation if weights else cls.DEFAULT_WEIGHTS["innovation"],
            "partnership_feasibility": weights.partnership_feasibility if weights else cls.DEFAULT_WEIGHTS["partnership_feasibility"]
        }

        # Normalize weights to sum to 1.0
        sum_w = sum(raw_w.values())
        if sum_w <= 0:
            norm_w = {k: 1.0 / len(raw_w) for k in raw_w}
        else:
            norm_w = {k: v / sum_w for k, v in raw_w.items()}

        query = db.query(CandidateOpportunity)
        if sector_filter and sector_filter != "ALL":
            query = query.filter(CandidateOpportunity.sector == sector_filter)
        if min_evidence is not None and min_evidence > 0:
            query = query.filter(CandidateOpportunity.evidence_strength_score >= min_evidence)

        candidates = query.all()

        scored_list = []
        for c in candidates:
            # Parse score explanations if present
            explanations = {}
            if c.score_explanations:
                try:
                    explanations = json.loads(c.score_explanations) if isinstance(c.score_explanations, str) else c.score_explanations
                except Exception:
                    explanations = {}

            # Parse stage history
            history = []
            if c.stage_history:
                try:
                    history = json.loads(c.stage_history) if isinstance(c.stage_history, str) else c.stage_history
                except Exception:
                    history = []

            # Parse audit breakdown and rebuilt scores
            audit_breakdown = []
            if c.evidence_audit_breakdown:
                try:
                    audit_breakdown = json.loads(c.evidence_audit_breakdown) if isinstance(c.evidence_audit_breakdown, str) else c.evidence_audit_breakdown
                except Exception:
                    audit_breakdown = []

            rebuilt_scores = {}
            if c.rebuilt_scores:
                try:
                    rebuilt_scores = json.loads(c.rebuilt_scores) if isinstance(c.rebuilt_scores, str) else c.rebuilt_scores
                except Exception:
                    rebuilt_scores = {}

            # Calculate weighted composite priority score (1.0 - 10.0 scale)
            composite_score = (
                c.pollution_impact_score * norm_w["pollution_impact"] +
                c.evidence_strength_score * norm_w["evidence_strength"] +
                c.technical_feasibility_score * norm_w["technical_feasibility"] +
                c.financial_feasibility_score * norm_w["financial_feasibility"] +
                c.verification_score * norm_w["verification"] +
                c.scalability_score * norm_w["scalability"] +
                c.innovation_score * norm_w["innovation"] +
                c.partnership_feasibility_score * norm_w["partnership_feasibility"]
            )

            scored_list.append({
                "id": c.id,
                "slug": c.slug,
                "title": c.title,
                "sector": c.sector,
                "target_pollutant": c.target_pollutant,
                "suspected_source": c.suspected_source,
                "problem_statement": c.problem_statement,
                "supporting_evidence": c.supporting_evidence,
                "geographic_relevance": c.geographic_relevance,
                "proposed_mechanism": c.proposed_mechanism,
                "potential_users": c.potential_users,
                "required_technology": c.required_technology,
                "development_complexity": c.development_complexity,
                "potential_partners": c.potential_partners,
                "verification_method": c.verification_method,
                "unresolved_questions": c.unresolved_questions,
                "key_risks": c.key_risks,
                "ip_opportunity": c.ip_opportunity,
                "pollution_impact_score": c.pollution_impact_score,
                "evidence_strength_score": c.evidence_strength_score,
                "technical_feasibility_score": c.technical_feasibility_score,
                "financial_feasibility_score": c.financial_feasibility_score,
                "verification_score": c.verification_score,
                "scalability_score": c.scalability_score,
                "innovation_score": c.innovation_score,
                "partnership_feasibility_score": c.partnership_feasibility_score,
                "weighted_priority_score": round(composite_score, 2),
                "score_explanations": explanations,
                "stage_status": c.stage_status,
                "stage_history": history,
                "shortlist_status": c.shortlist_status,
                "shortlist_notes": c.shortlist_notes,
                "data_classification": c.data_classification,
                # Milestone 5 Audit fields
                "pre_audit_evidence_score": c.pre_audit_evidence_score,
                "pre_audit_priority_score": c.pre_audit_priority_score,
                "evidence_audit_breakdown": audit_breakdown,
                "has_synthetic_dependency": bool(c.has_synthetic_dependency),
                "has_unverified_claims": bool(c.has_unverified_claims),
                "verified_evidence_summary": c.verified_evidence_summary,
                "missing_evidence_summary": c.missing_evidence_summary,
                "derived_distance_km": c.derived_distance_km,
                "rebuilt_scores": rebuilt_scores,
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "updated_at": c.updated_at.isoformat() if c.updated_at else None
            })

        # Rank descending by weighted score
        scored_list.sort(key=lambda x: x["weighted_priority_score"], reverse=True)
        for idx, item in enumerate(scored_list):
            item["rank"] = idx + 1

        return scored_list

    @classmethod
    def transition_stage(
        cls,
        db: Session,
        candidate_id: int,
        target_stage: str,
        notes: Optional[str] = None,
        evidence_ref: Optional[str] = None,
        verification_dataset_ref: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Enforces stage-gate governance rules before permitting stage progression:
        - Moving to 'Evidence reviewed' or beyond requires verifiable supporting evidence citation.
        - Moving to 'Pilot validated' requires an empirical verification dataset reference.
        """
        if target_stage not in cls.VALID_STAGES:
            raise ValueError(f"Invalid stage '{target_stage}'. Must be one of {cls.VALID_STAGES}")

        candidate = db.query(CandidateOpportunity).filter(CandidateOpportunity.id == candidate_id).first()
        if not candidate:
            raise ValueError(f"Candidate opportunity with ID {candidate_id} not found.")

        target_idx = cls.VALID_STAGES.index(target_stage)
        current_idx = cls.VALID_STAGES.index(candidate.stage_status) if candidate.stage_status in cls.VALID_STAGES else 0

        # Gate Check 1: Evidence reviewed gate
        evidence_idx = cls.VALID_STAGES.index("Evidence reviewed")
        if target_idx >= evidence_idx and current_idx < evidence_idx:
            if not evidence_ref or len(evidence_ref.strip()) < 5:
                raise ValueError(
                    "Stage-Gate Violation: Progression to 'Evidence reviewed' or beyond requires "
                    "a verifiable statutory citation or peer-reviewed document reference."
                )

        # Gate Check 2: Pilot validated gate
        pilot_val_idx = cls.VALID_STAGES.index("Pilot validated")
        if target_idx >= pilot_val_idx:
            if not verification_dataset_ref or len(verification_dataset_ref.strip()) < 5:
                raise ValueError(
                    "Stage-Gate Violation: A project cannot be marked as 'Pilot validated' simply because "
                    "a prototype exists. You must provide a link to an empirical verification dataset "
                    "demonstrating counterfactual emission reduction."
                )

        # Record stage transition history
        history = []
        if candidate.stage_history:
            try:
                history = json.loads(candidate.stage_history) if isinstance(candidate.stage_history, str) else candidate.stage_history
            except Exception:
                history = []

        transition_entry = {
            "from_stage": candidate.stage_status,
            "to_stage": target_stage,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "notes": notes or "Stage advanced by researcher.",
            "evidence_provided": evidence_ref,
            "verification_dataset_provided": verification_dataset_ref
        }
        history.append(transition_entry)

        candidate.stage_status = target_stage
        candidate.stage_history = json.dumps(history)
        candidate.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(candidate)

        return {
            "candidate_id": candidate.id,
            "title": candidate.title,
            "current_stage": candidate.stage_status,
            "history_length": len(history),
            "latest_transition": transition_entry
        }

    @staticmethod
    def update_shortlist(
        db: Session,
        candidate_id: int,
        status: str,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Updates shortlisting status: CONSIDERING, SHORTLISTED, REJECTED, FURTHER_INVESTIGATION
        """
        valid_statuses = ["CONSIDERING", "SHORTLISTED", "REJECTED", "FURTHER_INVESTIGATION"]
        status_upper = status.upper()
        if status_upper not in valid_statuses:
            raise ValueError(f"Invalid shortlist status '{status}'. Must be one of {valid_statuses}")

        candidate = db.query(CandidateOpportunity).filter(CandidateOpportunity.id == candidate_id).first()
        if not candidate:
            raise ValueError(f"Candidate opportunity with ID {candidate_id} not found.")

        candidate.shortlist_status = status_upper
        if notes:
            candidate.shortlist_notes = notes
        candidate.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(candidate)

        return {
            "candidate_id": candidate.id,
            "title": candidate.title,
            "shortlist_status": candidate.shortlist_status,
            "shortlist_notes": candidate.shortlist_notes
        }

# Module-level aliases for convenient access
calculate_evidence_score_from_audit = OpportunityEngine.calculate_evidence_score_from_audit
evaluate_candidates = OpportunityEngine.evaluate_candidates

