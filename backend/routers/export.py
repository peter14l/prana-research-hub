"""
Export and Reporting Router:
Generates formal Research Brief markdown/text document.
"""
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.models import InterventionHypothesis
from backend.routers.overview import get_regional_summary
from backend.routers.hotspots import get_evaluated_zones
from backend.services.export_service import ExportService

router = APIRouter(prefix="/export", tags=["Export & Reporting"])

@router.get("/report")
def export_research_report(db: Session = Depends(get_db)):
    summary = get_regional_summary(db)
    hotspots = get_evaluated_zones(db)
    hypotheses = [
        {
            "title": h.title,
            "target_area": h.target_area,
            "target_pollutant": h.target_pollutant,
            "suspected_source": h.suspected_source,
            "proposed_intervention": h.proposed_intervention,
            "measurable_indicators": h.measurable_indicators,
            "feasibility_score": h.feasibility_score,
            "potential_reduction_score": h.potential_reduction_score
        }
        for h in db.query(InterventionHypothesis).all()
    ]

    report_md = ExportService.generate_research_brief_markdown(summary, hypotheses, hotspots)
    
    return Response(
        content=report_md,
        media_type="text/markdown",
        headers={"Content-Disposition": "attachment; filename=PRANA_Research_Hub_Brief.md"}
    )
