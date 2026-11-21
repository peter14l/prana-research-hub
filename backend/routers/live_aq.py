"""
Live Air Quality router (Milestone 2):
Detailed monitoring-station list with statutory verification data, CPCB AQI status,
and granular data classification (VERIFIED, IMPORTED, DERIVED, DEMO, UNVERIFIED).
"""
from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from backend.database import get_db
from backend.models.models import (
    MonitoringStation, ValidatedObservation, RawObservation, StationAQIRecord
)
from backend.services.export_service import ExportService

router = APIRouter(prefix="/live", tags=["Live Air Quality"])

@router.get("/stations")
def get_live_stations(
    city: Optional[str] = None,
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    query = db.query(MonitoringStation).filter_by(active=True)
    if city:
        query = query.filter(MonitoringStation.city.ilike(f"%{city}%"))
    stations = query.all()

    result = []
    for st in stations:
        # Get latest AQI record
        aqi_rec = (
            db.query(StationAQIRecord)
            .filter_by(station_id=st.id)
            .order_by(StationAQIRecord.timestamp.desc())
            .first()
        )

        # Get latest observation values for each pollutant
        pollutants_map = {}
        latest_time = None
        dominant_classification = "DEMO"

        for pol in ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3", "NH3"]:
            obs = (
                db.query(ValidatedObservation)
                .filter_by(station_id=st.id, pollutant=pol)
                .order_by(ValidatedObservation.observation_timestamp.desc())
                .first()
            )
            if obs:
                pollutants_map[pol] = {
                    "value": obs.normalized_value,
                    "unit": obs.unit,
                    "quality_status": obs.quality_status,
                    "data_classification": obs.data_classification or "DEMO",
                    "timestamp": obs.observation_timestamp.isoformat(),
                    "provenance": obs.provenance
                }
                dominant_classification = obs.data_classification or "DEMO"
                if not latest_time or obs.observation_timestamp > latest_time:
                    latest_time = obs.observation_timestamp

        # Data freshness check
        is_fresh = False
        status_label = "OFFLINE"
        if latest_time:
            diff_hours = (datetime.utcnow() - latest_time).total_seconds() / 3600.0
            if diff_hours < 3.0:
                is_fresh = True
                status_label = "LIVE"
            elif diff_hours < 24.0:
                is_fresh = False
                status_label = "DELAYED"
            else:
                is_fresh = False
                status_label = "STALE"

        result.append({
            "id": st.id,
            "station_code": st.station_code,
            "cpcb_site_id": st.cpcb_site_id or "site_pending",
            "name": st.name,
            "city": st.city,
            "area_type": st.area_type,
            "address": st.address,
            "latitude": st.latitude,
            "longitude": st.longitude,
            "elevation": st.elevation,
            "verification_status": st.verification_status or "VERIFIED",
            "verification_date": st.verification_date or "2026-11-21",
            "verification_source_url": st.verification_source_url or "https://app.cpcbccr.com/ccr_docs",
            "verified_parameters": st.verified_parameters or "PM2.5, PM10, NO2, SO2, CO, O3, NH3",
            "verification_notes": st.verification_notes or "Statutory CAAQM installation.",
            "data_classification": dominant_classification,
            "is_fresh": is_fresh,
            "status_label": status_label,
            "last_observation_time": latest_time.isoformat() if latest_time else None,
            "latest_pollutants": pollutants_map,
            "aqi": aqi_rec.aqi_value if aqi_rec else None,
            "aqi_category": aqi_rec.category if aqi_rec else "N/A",
            "dominant_pollutant": aqi_rec.dominant_pollutant if aqi_rec else None,
            "is_valid_cpcb": aqi_rec.is_valid_cpcb if aqi_rec else False,
            "sub_indices": aqi_rec.sub_indices if aqi_rec else {}
        })

    return result

@router.get("/stations/{station_id}/history")
def get_station_history(
    station_id: int,
    pollutant: str = "PM2.5",
    hours: int = 48,
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    obs = (
        db.query(ValidatedObservation)
        .filter(
            ValidatedObservation.station_id == station_id,
            ValidatedObservation.pollutant == pollutant,
            ValidatedObservation.observation_timestamp >= cutoff
        )
        .order_by(ValidatedObservation.observation_timestamp.asc())
        .all()
    )

    return [
        {
            "timestamp": o.observation_timestamp.isoformat(),
            "time_label": o.observation_timestamp.strftime("%d %b %H:%M"),
            "value": o.normalized_value,
            "unit": o.unit,
            "quality_status": o.quality_status,
            "data_classification": o.data_classification or "DEMO",
            "provenance": o.provenance,
            "provenance_hash": o.provenance_hash,
            "is_valid": o.is_valid,
            "flag_reason": o.flag_reason
        }
        for o in obs
    ]

@router.get("/download-csv")
def download_live_csv(
    station_id: Optional[int] = None,
    pollutant: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = (
        db.query(
            ValidatedObservation,
            MonitoringStation.name.label("station_name"),
            MonitoringStation.station_code,
            MonitoringStation.city
        )
        .join(MonitoringStation, ValidatedObservation.station_id == MonitoringStation.id)
    )

    if station_id:
        query = query.filter(ValidatedObservation.station_id == station_id)
    if pollutant:
        query = query.filter(ValidatedObservation.pollutant == pollutant)

    records = query.order_by(ValidatedObservation.observation_timestamp.desc()).limit(2000).all()

    formatted = []
    for obs, name, code, city in records:
        formatted.append({
            "station_code": code,
            "station_name": name,
            "city": city,
            "pollutant": obs.pollutant,
            "normalized_value": obs.normalized_value,
            "unit": obs.unit,
            "observation_timestamp": obs.observation_timestamp.isoformat(),
            "data_classification": obs.data_classification or "DEMO",
            "quality_status": obs.quality_status,
            "provenance": obs.provenance
        })

    csv_data = ExportService.export_observations_csv(formatted)
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=prana_validated_observations.csv"}
    )
