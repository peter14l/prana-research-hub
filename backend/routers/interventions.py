"""
Intervention Lab router:
Hypothesis formulation, multi-criteria scoring, and counterfactual validation frameworks.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime
from backend.database import get_db
from backend.models.models import InterventionHypothesis
from backend.models.schemas import InterventionHypothesisCreate

router = APIRouter(prefix="/interventions", tags=["Intervention Lab"])

@router.get("/hypotheses")
def get_hypotheses(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    hyps = db.query(InterventionHypothesis).order_by(InterventionHypothesis.id.asc()).all()
    return [
        {
            "id": h.id,
            "title": h.title,
            "problem_statement": h.problem_statement,
            "target_area": h.target_area,
            "target_pollutant": h.target_pollutant,
            "suspected_source": h.suspected_source,
            "supporting_evidence": h.supporting_evidence,
            "proposed_intervention": h.proposed_intervention,
            "mechanism_of_action": h.mechanism_of_action,
            "required_resources": h.required_resources,
            "possible_implementation_partner": h.possible_implementation_partner,
            "measurable_indicators": h.measurable_indicators,
            "risks_limitations": h.risks_limitations,
            "research_confidence": h.research_confidence,
            "validation_requirements": h.validation_requirements,
            "feasibility_score": h.feasibility_score,
            "potential_reduction_score": h.potential_reduction_score,
            "cost_complexity_score": h.cost_complexity_score,
            "ease_of_verification_score": h.ease_of_verification_score,
            "scalability_score": h.scalability_score,
            "evaluation_framework": h.evaluation_framework,
            "status": h.status,
            "created_at": h.created_at.isoformat()
        }
        for h in hyps
    ]

@router.post("/hypotheses")
def create_hypothesis(
    hyp_in: InterventionHypothesisCreate,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    hyp = InterventionHypothesis(
        title=hyp_in.title,
        problem_statement=hyp_in.problem_statement,
        target_area=hyp_in.target_area,
        target_pollutant=hyp_in.target_pollutant,
        suspected_source=hyp_in.suspected_source,
        supporting_evidence=hyp_in.supporting_evidence,
        proposed_intervention=hyp_in.proposed_intervention,
        mechanism_of_action=hyp_in.mechanism_of_action,
        required_resources=hyp_in.required_resources,
        possible_implementation_partner=hyp_in.possible_implementation_partner,
        measurable_indicators=hyp_in.measurable_indicators,
        risks_limitations=hyp_in.risks_limitations,
        research_confidence=hyp_in.research_confidence,
        validation_requirements=hyp_in.validation_requirements,
        feasibility_score=hyp_in.feasibility_score,
        potential_reduction_score=hyp_in.potential_reduction_score,
        cost_complexity_score=hyp_in.cost_complexity_score,
        ease_of_verification_score=hyp_in.ease_of_verification_score,
        scalability_score=hyp_in.scalability_score,
        evaluation_framework=hyp_in.evaluation_framework or {
            "baseline_period_days": 45,
            "intervention_period_days": 90,
            "control_station": "Victoria Memorial",
            "weather_normalization_method": "Regression de-weathering"
        },
        status="DRAFT_HYPOTHESIS",
        created_at=datetime.utcnow()
    )
    db.add(hyp)
    db.commit()
    db.refresh(hyp)

    return {"id": hyp.id, "title": hyp.title, "status": "SUCCESS"}
