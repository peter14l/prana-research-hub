"""
PRANA Research Hub - Environmental Analysis Router (Milestone 3)
Provides research endpoints for:
- Temporal pollution analysis (diurnal 24h, daily averages, weekly cycles)
- Meteorological analysis (dispersion, bivariate correlations, 16-sector pollution rose)
- Hotspot investigation & spatial coverage voids
- Analysis workspace: save, retrieve, and export reproducible research analyses
"""
import csv
import io
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from backend.database import get_db
from backend.services.environmental_analysis_engine import EnvironmentalAnalysisEngine
from backend.models.models import SavedAnalysis, ValidatedObservation, MonitoringStation
from backend.models.schemas import SavedAnalysisCreate, SavedAnalysisOut

router = APIRouter(prefix="/analysis", tags=["Environmental Analysis Engine"])

@router.get("/temporal")
def get_temporal_analysis(
    pollutant: str = Query("PM2.5"),
    station_ids: Optional[str] = Query(None, description="Comma-separated station IDs, e.g. 1,3,7"),
    days: int = Query(7, ge=1, le=90),
    classifications: Optional[str] = Query(None, description="Comma-separated tiers, e.g. VERIFIED,IMPORTED,DEMO"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Returns diurnal profile, daily aggregated series, and weekday/weekend patterns."""
    parsed_ids = [int(i.strip()) for i in station_ids.split(",") if i.strip().isdigit()] if station_ids else None
    cutoff = datetime.utcnow() - timedelta(days=days)
    parsed_classes = [c.strip().upper() for c in classifications.split(",")] if classifications else None

    obs = EnvironmentalAnalysisEngine.get_filtered_observations(
        db=db,
        pollutant=pollutant,
        station_ids=parsed_ids,
        date_from=cutoff,
        allowed_classifications=parsed_classes
    )
    return EnvironmentalAnalysisEngine.analyze_temporal_patterns(obs, pollutant=pollutant)

@router.get("/meteorological")
def get_meteorological_analysis(
    pollutant: str = Query("PM2.5"),
    city: str = Query("Kolkata"),
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Returns synchronous correlation with wind speed, temperature, humidity, rainfall, and 16-sector pollution rose."""
    cutoff = datetime.utcnow() - timedelta(days=days)
    obs = EnvironmentalAnalysisEngine.get_filtered_observations(
        db=db,
        pollutant=pollutant,
        date_from=cutoff
    )
    return EnvironmentalAnalysisEngine.analyze_meteorological_relationships(
        db=db,
        observations=obs,
        pollutant=pollutant,
        city=city
    )

@router.get("/hotspots")
def get_hotspot_investigation(
    pollutant: str = Query("PM2.5"),
    hours_window: int = Query(168, ge=24, le=720),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Returns monitored hotspots ranked by concentration & exceedances, plus unmonitored coverage void disclosures."""
    return EnvironmentalAnalysisEngine.investigate_hotspots_and_coverage_gaps(
        db=db,
        pollutant=pollutant,
        hours_window=hours_window
    )

@router.post("/workspace/save", response_model=SavedAnalysisOut)
def save_workspace_analysis(
    payload: SavedAnalysisCreate,
    db: Session = Depends(get_db)
):
    """Saves a research analysis configuration and findings for reproducibility."""
    analysis = SavedAnalysis(
        title=payload.title,
        description=payload.description,
        author=payload.author or "PRANA Environmental Researcher",
        pollutant=payload.pollutant,
        station_ids=payload.station_ids,
        date_range_start=payload.date_range_start,
        date_range_end=payload.date_range_end,
        met_variables=payload.met_variables,
        methodology=payload.methodology,
        source_references=payload.source_references,
        analysis_results=payload.analysis_results,
        created_at=datetime.utcnow()
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis

@router.get("/workspace/list")
def list_saved_analyses(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """Returns all saved reproducible research analyses."""
    analyses = db.query(SavedAnalysis).order_by(SavedAnalysis.created_at.desc()).all()
    return [
        {
            "id": a.id,
            "title": a.title,
            "description": a.description,
            "author": a.author,
            "pollutant": a.pollutant,
            "station_ids": a.station_ids,
            "date_range_start": a.date_range_start.isoformat() if a.date_range_start else None,
            "date_range_end": a.date_range_end.isoformat() if a.date_range_end else None,
            "met_variables": a.met_variables,
            "methodology": a.methodology,
            "source_references": a.source_references,
            "created_at": a.created_at.isoformat() if a.created_at else None
        }
        for a in analyses
    ]

@router.get("/workspace/{analysis_id}")
def get_saved_analysis(analysis_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Retrieves full details of a saved reproducible analysis."""
    analysis = db.query(SavedAnalysis).filter(SavedAnalysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Saved analysis not found.")

    return {
        "id": analysis.id,
        "title": analysis.title,
        "description": analysis.description,
        "author": analysis.author,
        "pollutant": analysis.pollutant,
        "station_ids": analysis.station_ids,
        "date_range_start": analysis.date_range_start.isoformat() if analysis.date_range_start else None,
        "date_range_end": analysis.date_range_end.isoformat() if analysis.date_range_end else None,
        "met_variables": analysis.met_variables,
        "methodology": analysis.methodology,
        "source_references": analysis.source_references,
        "analysis_results": analysis.analysis_results,
        "created_at": analysis.created_at.isoformat() if analysis.created_at else None
    }

@router.get("/workspace/{analysis_id}/export")
def export_analysis_dataset(analysis_id: int, db: Session = Depends(get_db)):
    """Exports the underlying observation dataset for a saved analysis as CSV."""
    analysis = db.query(SavedAnalysis).filter(SavedAnalysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Saved analysis not found.")

    obs_query = db.query(
        ValidatedObservation, MonitoringStation.name.label("station_name"), MonitoringStation.station_code
    ).join(
        MonitoringStation, ValidatedObservation.station_id == MonitoringStation.id
    ).filter(
        ValidatedObservation.pollutant == analysis.pollutant,
        ValidatedObservation.station_id.in_(analysis.station_ids),
        ValidatedObservation.is_valid == True
    )

    if analysis.date_range_start:
        obs_query = obs_query.filter(ValidatedObservation.observation_timestamp >= analysis.date_range_start)
    if analysis.date_range_end:
        obs_query = obs_query.filter(ValidatedObservation.observation_timestamp <= analysis.date_range_end)

    records = obs_query.order_by(ValidatedObservation.observation_timestamp.asc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "observation_timestamp_utc", "station_code", "station_name", "pollutant",
        "value", "unit", "data_classification", "provenance_hash"
    ])

    for row in records:
        o = row.ValidatedObservation
        writer.writerow([
            o.observation_timestamp.isoformat(),
            row.station_code,
            row.station_name,
            o.pollutant,
            o.normalized_value,
            o.unit,
            o.data_classification,
            o.provenance_hash or ""
        ])

    csv_data = output.getvalue()
    filename = f"PRANA_Analysis_{analysis.id}_{analysis.pollutant}.csv"

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
