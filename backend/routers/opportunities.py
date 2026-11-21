"""
PRANA Opportunity Explorer Router (Milestone 4):
Endpoints for evidence inventory, independent sector analyses,
multi-criteria opportunity evaluation, stage-gate lifecycle governance,
research gap detection, and candidate shortlisting.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional

from backend.database import get_db
from backend.services.opportunity_engine import OpportunityEngine
from backend.services.gap_detector import ResearchGapDetector
from backend.models.schemas import (
    OpportunityEvaluationRequest, CandidateOpportunityOut,
    StageGateTransitionRequest, ShortlistUpdateRequest,
    ResearchGapOut, EvaluationWeights
)
from backend.models.models import CandidateOpportunity

router = APIRouter(prefix="/opportunities", tags=["Opportunity Explorer"])

@router.get("/inventory")
def get_evidence_inventory(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Returns complete evidence inventory cataloging all datasets, date ranges,
    reliability classifications, and data limitations.
    """
    return OpportunityEngine.build_evidence_inventory(db)

@router.get("/sectors")
def get_sector_evaluations(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """
    Returns independent evaluations for all 8 pollution sectors in Kolkata–Howrah.
    """
    return OpportunityEngine.evaluate_sectors(db)

@router.get("/candidates")
def list_candidate_opportunities(
    sector: Optional[str] = Query(None, description="Filter by sector name or 'ALL'"),
    min_evidence: Optional[float] = Query(None, description="Minimum evidence score (1-10)"),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """
    Lists all candidate engineering opportunities scored and ranked using default weights.
    """
    return OpportunityEngine.evaluate_candidates(
        db=db,
        weights=None,
        sector_filter=sector,
        min_evidence=min_evidence
    )

@router.post("/evaluate")
def evaluate_candidates_custom_weights(
    req: OpportunityEvaluationRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Recalculates multi-criteria priority scores using researcher-customized criterion weights.
    Explicitly discloses that composite scores are a prioritization heuristic, not a physical measurement.
    """
    scored = OpportunityEngine.evaluate_candidates(
        db=db,
        weights=req.weights,
        sector_filter=req.sector_filter,
        min_evidence=req.min_evidence_score
    )

    return {
        "disclaimer": (
            "SCIENTIFIC NOTICE: The weighted priority score is a multi-criteria prioritization "
            "heuristic designed to assist engineering decision-making. It is not an empirical "
            "physical measurement of atmospheric concentration or absolute project success."
        ),
        "active_weights": req.weights.model_dump() if req.weights else OpportunityEngine.DEFAULT_WEIGHTS,
        "candidate_count": len(scored),
        "candidates": scored
    }

@router.get("/candidates/{id_or_slug}")
def get_candidate_dossier(
    id_or_slug: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Retrieves a single candidate opportunity's comprehensive 14-field engineering dossier.
    """
    candidate = None
    if id_or_slug.isdigit():
        candidate = db.query(CandidateOpportunity).filter(CandidateOpportunity.id == int(id_or_slug)).first()
    if not candidate:
        candidate = db.query(CandidateOpportunity).filter(CandidateOpportunity.slug == id_or_slug).first()

    if not candidate:
        raise HTTPException(status_code=404, detail=f"Candidate opportunity '{id_or_slug}' not found.")

    # Return scored representation
    scored_all = OpportunityEngine.evaluate_candidates(db=db)
    for c in scored_all:
        if c["id"] == candidate.id:
            return c

    return {
        "id": candidate.id,
        "slug": candidate.slug,
        "title": candidate.title,
        "sector": candidate.sector,
        "target_pollutant": candidate.target_pollutant,
        "problem_statement": candidate.problem_statement,
        "stage_status": candidate.stage_status
    }

@router.post("/candidates/{candidate_id}/stage")
def transition_candidate_stage(
    candidate_id: int,
    req: StageGateTransitionRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Advances or transitions a candidate along the 8-stage engineering lifecycle
    subject to strict evidence and verification gating rules.
    """
    try:
        result = OpportunityEngine.transition_stage(
            db=db,
            candidate_id=candidate_id,
            target_stage=req.target_stage,
            notes=req.notes,
            evidence_ref=req.supporting_evidence_reference,
            verification_dataset_ref=req.verification_dataset_reference
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/candidates/{candidate_id}/shortlist")
def update_candidate_shortlist(
    candidate_id: int,
    req: ShortlistUpdateRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Shortlists, rejects, or marks a candidate for further investigation.
    """
    try:
        result = OpportunityEngine.update_shortlist(
            db=db,
            candidate_id=candidate_id,
            status=req.status,
            notes=req.notes
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/gaps")
def list_research_gaps(
    severity: Optional[str] = Query(None, description="CRITICAL, HIGH, MEDIUM, LOW, or ALL"),
    sector: Optional[str] = Query(None, description="Filter by sector or ALL"),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """
    Returns research gaps classified by severity and sector.
    """
    return ResearchGapDetector.get_all_gaps(db=db, severity=severity, sector=sector)

@router.get("/gaps/audit")
def audit_research_gaps(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Performs dynamic programmatic gap audit identifying unmonitored zones,
    missing emission factor data, and cheapest credible remote vs field resolutions.
    """
    return ResearchGapDetector.perform_gap_audit(db=db)
