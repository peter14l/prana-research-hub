"""
Source Intelligence router (Milestone 2):
Evidence-backed source profiles, published studies, and verifiable citations.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from backend.database import get_db
from backend.models.models import (
    SourceCategory, SourceApportionmentStudy, SourceContributionProfile, ResearchFinding
)
from backend.services.source_intelligence_service import EVIDENCE_TYPES

router = APIRouter(prefix="/sources", tags=["Source Intelligence"])

@router.get("/evidence-labels")
def get_evidence_labels() -> Dict[str, Any]:
    return EVIDENCE_TYPES

@router.get("/categories")
def get_source_categories(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    cats = db.query(SourceCategory).all()
    return [
        {
            "id": c.id,
            "code": c.code,
            "name": c.name,
            "sector": c.sector,
            "description": c.description,
            "primary_pollutants": c.primary_pollutants,
            "typical_marker_species": c.typical_marker_species
        }
        for c in cats
    ]

@router.get("/studies")
def get_published_studies(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    studies = db.query(SourceApportionmentStudy).all()
    return [
        {
            "id": s.id,
            "study_name": s.study_name,
            "organisation": s.organisation,
            "publication_year": s.publication_year,
            "methodology": s.methodology,
            "geographic_scope": s.geographic_scope,
            "study_period": s.study_period,
            "documentation_url": s.documentation_url,
            "limitations": s.limitations,
            "confidence_tier": s.confidence_tier
        }
        for s in studies
    ]

@router.get("/findings")
def get_verifiable_findings(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """Returns statutory research findings with page numbers and table citations."""
    findings = db.query(ResearchFinding).all()
    return [
        {
            "id": f.id,
            "document_id": f.document_id,
            "finding_type": f.finding_type,
            "title": f.title,
            "statement": f.statement,
            "citation_reference": f.citation_reference,
            "page_number": f.page_number,
            "table_figure_ref": f.table_figure_ref,
            "has_supporting_reference": bool(f.has_supporting_reference),
            "confidence": f.confidence
        }
        for f in findings
    ]

@router.get("/profiles")
def get_contribution_profiles(
    city: str = "Kolkata",
    season: str = "Winter",
    pollutant: str = "PM2.5",
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    profiles = (
        db.query(SourceContributionProfile, SourceCategory.name.label("category_name"), SourceCategory.sector)
        .join(SourceCategory, SourceContributionProfile.category_id == SourceCategory.id)
        .filter(
            SourceContributionProfile.city == city,
            SourceContributionProfile.season == season,
            SourceContributionProfile.pollutant == pollutant
        )
        .order_by(SourceContributionProfile.contribution_percentage.desc())
        .all()
    )

    return [
        {
            "id": p.SourceContributionProfile.id,
            "category_id": p.SourceContributionProfile.category_id,
            "category_name": p.category_name,
            "sector": p.sector,
            "city": p.SourceContributionProfile.city,
            "season": p.SourceContributionProfile.season,
            "pollutant": p.SourceContributionProfile.pollutant,
            "contribution_percentage": p.SourceContributionProfile.contribution_percentage,
            "concentration_ugm3": p.SourceContributionProfile.concentration_ugm3,
            "uncertainty_min": p.SourceContributionProfile.uncertainty_min,
            "uncertainty_max": p.SourceContributionProfile.uncertainty_max,
            "evidence_type": p.SourceContributionProfile.evidence_type,
            "citation_reference": p.SourceContributionProfile.citation_reference,
            "page_number": p.SourceContributionProfile.page_number,
            "table_figure_ref": p.SourceContributionProfile.table_figure_ref,
            "has_supporting_reference": bool(p.SourceContributionProfile.has_supporting_reference)
        }
        for p in profiles
    ]
