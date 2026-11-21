"""
Geographic Hotspots router:
Evaluates monitoring network, admin zones, and explicit data gaps.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from backend.database import get_db
from backend.models.models import MonitoringStation, ValidatedObservation
from backend.services.hotspot_engine import HotspotEngine

router = APIRouter(prefix="/hotspots", tags=["Geographic Hotspots"])

@router.get("/zones")
def get_evaluated_zones(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    stations = db.query(MonitoringStation).filter_by(active=True).all()
    
    station_metrics = []
    for st in stations:
        # Latest PM2.5 and PM10
        pm25 = (
            db.query(ValidatedObservation)
            .filter_by(station_id=st.id, pollutant="PM2.5")
            .order_by(ValidatedObservation.observation_timestamp.desc())
            .first()
        )
        pm10 = (
            db.query(ValidatedObservation)
            .filter_by(station_id=st.id, pollutant="PM10")
            .order_by(ValidatedObservation.observation_timestamp.desc())
            .first()
        )

        station_metrics.append({
            "id": st.id,
            "station_code": st.station_code,
            "name": st.name,
            "city": st.city,
            "latitude": st.latitude,
            "longitude": st.longitude,
            "pm25_latest": pm25.normalized_value if pm25 else None,
            "pm10_latest": pm10.normalized_value if pm10 else None
        })

    return HotspotEngine.evaluate_zones(station_metrics)
