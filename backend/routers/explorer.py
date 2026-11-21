"""
Pollution Explorer router:
Diurnal cycles, day-of-week patterns, and bivariate correlation analysis.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from backend.database import get_db
from backend.models.models import (
    MonitoringStation, ValidatedObservation, WeatherObservation
)
from backend.services.analytics_engine import AnalyticsEngine

router = APIRouter(prefix="/explorer", tags=["Pollution Explorer"])

@router.get("/diurnal")
def get_diurnal_profile(
    pollutant: str = "PM2.5",
    station_id: Optional[int] = None,
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    query = db.query(ValidatedObservation).filter(
        ValidatedObservation.pollutant == pollutant,
        ValidatedObservation.is_valid == True
    )
    if station_id:
        query = query.filter(ValidatedObservation.station_id == station_id)

    obs = query.all()
    records = [
        {
            "pollutant": o.pollutant,
            "normalized_value": o.normalized_value,
            "observation_timestamp": o.observation_timestamp
        }
        for o in obs
    ]
    return AnalyticsEngine.calculate_diurnal_profile(records, pollutant)

@router.get("/day-of-week")
def get_day_of_week_profile(
    pollutant: str = "PM2.5",
    station_id: Optional[int] = None,
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    query = db.query(ValidatedObservation).filter(
        ValidatedObservation.pollutant == pollutant,
        ValidatedObservation.is_valid == True
    )
    if station_id:
        query = query.filter(ValidatedObservation.station_id == station_id)

    obs = query.all()
    records = [
        {
            "pollutant": o.pollutant,
            "normalized_value": o.normalized_value,
            "observation_timestamp": o.observation_timestamp
        }
        for o in obs
    ]
    return AnalyticsEngine.calculate_day_of_week_profile(records, pollutant)

@router.get("/correlation")
def get_correlation(
    var_x: str = "PM2.5",
    var_y: str = "PBLH", # PM10, NO2, Temperature, WindSpeed, PBLH, Humidity
    station_id: Optional[int] = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Computes Pearson and Spearman correlation between two environmental parameters.
    Supports pollutant-to-pollutant or pollutant-to-weather bivariate comparisons.
    """
    # 1. Fetch Var X
    x_map = {}
    if var_x in ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3", "NH3"]:
        q_x = db.query(ValidatedObservation).filter(
            ValidatedObservation.pollutant == var_x,
            ValidatedObservation.is_valid == True
        )
        if station_id:
            q_x = q_x.filter(ValidatedObservation.station_id == station_id)
        for o in q_x.all():
            x_map[o.observation_timestamp] = o.normalized_value
    else:
        # Weather var x
        w_records = db.query(WeatherObservation).all()
        for w in w_records:
            val = getattr(w, _map_weather_field(var_x), None)
            if val is not None:
                x_map[w.observation_timestamp] = val

    # 2. Fetch Var Y
    y_map = {}
    if var_y in ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3", "NH3"]:
        q_y = db.query(ValidatedObservation).filter(
            ValidatedObservation.pollutant == var_y,
            ValidatedObservation.is_valid == True
        )
        if station_id:
            q_y = q_y.filter(ValidatedObservation.station_id == station_id)
        for o in q_y.all():
            y_map[o.observation_timestamp] = o.normalized_value
    else:
        # Weather var y
        w_records = db.query(WeatherObservation).all()
        for w in w_records:
            val = getattr(w, _map_weather_field(var_y), None)
            if val is not None:
                y_map[w.observation_timestamp] = val

    # Align common timestamps
    common_keys = sorted(list(set(x_map.keys()).intersection(set(y_map.keys()))))
    xs = [x_map[k] for k in common_keys]
    ys = [y_map[k] for k in common_keys]

    return AnalyticsEngine.calculate_bivariate_correlation(xs, ys, var_x, var_y)

def _map_weather_field(name: str) -> str:
    mapping = {
        "Temperature": "temperature_c",
        "Humidity": "relative_humidity_pct",
        "WindSpeed": "wind_speed_kmh",
        "PBLH": "boundary_layer_height_m",
        "Rainfall": "rainfall_mm",
        "Pressure": "surface_pressure_hpa"
    }
    return mapping.get(name, "temperature_c")

@router.get("/station-comparison")
def compare_stations(
    pollutant: str = "PM2.5",
    station_ids: str = "1,3,7", # Victoria, RBU, Ghusuri default
    hours: int = 72,
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Returns side-by-side time series for selected monitoring stations."""
    st_id_list = [int(s.strip()) for s in station_ids.split(",") if s.strip().isdigit()]
    cutoff = datetime.utcnow() - timedelta(hours=hours)

    stations = db.query(MonitoringStation).filter(MonitoringStation.id.in_(st_id_list)).all()
    st_name_map = {s.id: s.name for s in stations}

    obs = (
        db.query(ValidatedObservation)
        .filter(
            ValidatedObservation.pollutant == pollutant,
            ValidatedObservation.station_id.in_(st_id_list),
            ValidatedObservation.observation_timestamp >= cutoff,
            ValidatedObservation.is_valid == True
        )
        .order_by(ValidatedObservation.observation_timestamp.asc())
        .all()
    )

    time_map: Dict[str, Dict[str, Any]] = {}
    for o in obs:
        t_str = o.observation_timestamp.strftime("%Y-%m-%d %H:%M")
        if t_str not in time_map:
            time_map[t_str] = {"timestamp": t_str, "display_time": o.observation_timestamp.strftime("%d %b %H:%M")}
        station_key = f"st_{o.station_id}"
        time_map[t_str][station_key] = o.normalized_value

    return list(time_map.values())
