"""
AI Research Assistant router:
Answers user queries grounded in database records and official scientific studies.
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from backend.database import get_db
from backend.models.models import (
    MonitoringStation, ResearchDocument, InterventionHypothesis,
    SourceContributionProfile, SourceCategory, WeatherObservation
)
from backend.services.ai_assistant import AIAssistantEngine
from backend.routers.overview import get_regional_summary

router = APIRouter(prefix="/assistant", tags=["AI Research Assistant"])

class QueryRequest(BaseModel):
    query: str

@router.post("/query")
def ask_assistant(
    req: QueryRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    # Gather live context from DB
    stations = db.query(MonitoringStation).all()
    studies = db.query(ResearchDocument).all()
    hypotheses = db.query(InterventionHypothesis).all()
    weather = db.query(WeatherObservation).order_by(WeatherObservation.observation_timestamp.desc()).first()
    summary = get_regional_summary(db)

    context = {
        "stations": [{"name": s.name, "code": s.station_code, "city": s.city} for s in stations],
        "studies": [{"title": d.title, "findings": d.key_findings} for d in studies],
        "hypotheses": [{"title": h.title, "target_area": h.target_area} for h in hypotheses],
        "regional_summary": summary,
        "weather": {
            "temperature": weather.temperature_c if weather else 24.0,
            "pblh": weather.boundary_layer_height_m if weather else 380.0
        }
    }

    return AIAssistantEngine.synthesize_query(req.query, context)
