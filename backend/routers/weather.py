"""
Weather & Atmospheric conditions router:
High-resolution meteorology, diurnal PBLH, and wind rose computation.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from backend.database import get_db
from backend.models.models import WeatherObservation
from backend.services.weather_service import WeatherService

router = APIRouter(prefix="/weather", tags=["Weather & Atmospheric"])

@router.get("/current")
async def get_current_weather(
    city: str = "Kolkata",
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    # Check latest from DB or fetch live
    latest_db = (
        db.query(WeatherObservation)
        .filter_by(city=city)
        .order_by(WeatherObservation.observation_timestamp.desc())
        .first()
    )

    if latest_db:
        return {
            "city": latest_db.city,
            "temperature_c": latest_db.temperature_c,
            "relative_humidity_pct": latest_db.relative_humidity_pct,
            "wind_speed_kmh": latest_db.wind_speed_kmh,
            "wind_direction_deg": latest_db.wind_direction_deg,
            "wind_direction_cardinal": latest_db.wind_direction_cardinal,
            "rainfall_mm": latest_db.rainfall_mm,
            "surface_pressure_hpa": latest_db.surface_pressure_hpa,
            "boundary_layer_height_m": latest_db.boundary_layer_height_m,
            "observation_timestamp": latest_db.observation_timestamp.isoformat(),
            "data_provider": latest_db.data_provider
        }

    # Fallback to service live probe
    return await WeatherService.fetch_current_weather()

@router.get("/history")
def get_weather_history(
    hours: int = 72,
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    records = (
        db.query(WeatherObservation)
        .filter(WeatherObservation.observation_timestamp >= cutoff)
        .order_by(WeatherObservation.observation_timestamp.asc())
        .all()
    )

    return [
        {
            "timestamp": r.observation_timestamp.isoformat(),
            "display_time": r.observation_timestamp.strftime("%d %b %H:%M"),
            "temperature_c": r.temperature_c,
            "relative_humidity_pct": r.relative_humidity_pct,
            "wind_speed_kmh": r.wind_speed_kmh,
            "wind_direction_deg": r.wind_direction_deg,
            "boundary_layer_height_m": r.boundary_layer_height_m,
            "surface_pressure_hpa": r.surface_pressure_hpa,
            "rainfall_mm": r.rainfall_mm
        }
        for r in records
    ]

@router.get("/wind-rose")
def get_wind_rose(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    records = db.query(WeatherObservation).all()
    dict_records = [
        {"wind_direction_deg": r.wind_direction_deg, "wind_speed_kmh": r.wind_speed_kmh}
        for r in records
    ]
    return WeatherService.compute_wind_rose(dict_records)
