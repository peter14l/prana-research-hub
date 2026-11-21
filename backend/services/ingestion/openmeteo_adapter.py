"""
Open-Meteo Atmospheric Reanalysis Ingestion Adapter
Retrieves historical and recent synoptic meteorological observations:
Temperature, Relative Humidity, Wind Speed, Wind Direction, Precipitation,
Surface Pressure, and Boundary Layer Height.
All records are strictly classified as MODELLED (Numerical Reanalysis).
"""
import urllib.request
import urllib.error
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from backend.services.ingestion.base import BaseIngestionAdapter, KOLKATA_TZ
from backend.models.models import WeatherObservation, DataProvider, IngestionLog

logger = logging.getLogger("prana.ingestion.openmeteo")

REPRESENTATIVE_COORDINATES = [
    {"city": "Kolkata", "latitude": 22.5726, "longitude": 88.3639},
    {"city": "Howrah", "latitude": 22.5958, "longitude": 88.2636}
]

def degrees_to_cardinal(deg: Optional[float]) -> str:
    """Converts wind degrees (0-360) to 16-point cardinal compass string."""
    if deg is None:
        return "CALM"
    directions = [
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
    ]
    idx = int((deg + 11.25) / 22.5) % 16
    return directions[idx]

class OpenMeteoAdapter(BaseIngestionAdapter):
    def __init__(self):
        super().__init__(provider_code="OPEN_METEO", provider_name="Open-Meteo Atmospheric Services")

    def fetch_weather_series(
        self,
        lat: float,
        lon: float,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        past_days: int = 7
    ) -> Dict[str, Any]:
        """
        Fetches hourly reanalysis variables.
        Uses historical archive API if specific past date range requested,
        or forecast API with past_days parameter for recent data.
        """
        vars_requested = (
            "temperature_2m,relative_humidity_2m,wind_speed_10m,"
            "wind_direction_10m,precipitation,surface_pressure,boundary_layer_height"
        )

        if start_date and end_date:
            url = (
                f"https://archive-api.open-meteo.com/v1/archive?"
                f"latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&"
                f"hourly={vars_requested}"
            )
        else:
            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}&hourly={vars_requested}&past_days={past_days}"
            )

        headers = {
            "User-Agent": "PRANA-Research-Hub/2.0 (Environmental Research; Kolkata-Howrah Airshed)"
        }

        def req_call():
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode("utf-8"))

        return self.execute_with_retry(
            req_call,
            max_retries=3,
            base_delay=1.5,
            retry_exceptions=(urllib.error.URLError, TimeoutError)
        )

    def ingest(
        self,
        db: Session,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        past_days: int = 7
    ) -> Dict[str, Any]:
        """
        Ingests hourly modelled weather records for representative Kolkata & Howrah locations.
        """
        start_time = datetime.utcnow()
        provider = db.query(DataProvider).filter(DataProvider.code == "OPEN_METEO").first()

        log = IngestionLog(
            provider_id=provider.id if provider else None,
            provider_code="OPEN_METEO",
            source_name="Open-Meteo Atmospheric Reanalysis",
            started_at=start_time,
            status="PENDING",
            data_classification="MODELLED",
            message="Ingesting synoptic atmospheric reanalysis variables"
        )
        db.add(log)
        db.commit()

        processed_count = 0
        errors = []

        try:
            for loc in REPRESENTATIVE_COORDINATES:
                city = loc["city"]
                lat = loc["latitude"]
                lng = loc["longitude"]

                try:
                    data = self.fetch_weather_series(
                        lat=lat,
                        lon=lng,
                        start_date=start_date,
                        end_date=end_date,
                        past_days=past_days
                    )

                    hourly = data.get("hourly", {})
                    times = hourly.get("time", [])
                    temps = hourly.get("temperature_2m", [])
                    humids = hourly.get("relative_humidity_2m", [])
                    wind_speeds = hourly.get("wind_speed_10m", [])
                    wind_dirs = hourly.get("wind_direction_10m", [])
                    precips = hourly.get("precipitation", [])
                    pressures = hourly.get("surface_pressure", [])
                    pblhs = hourly.get("boundary_layer_height", [])

                    for i, t_str in enumerate(times):
                        # Convert ISO timestamp to UTC
                        utc_dt, _ = self.parse_to_utc_and_local(t_str)

                        # Duplicate check
                        exists = db.query(WeatherObservation).filter(
                            WeatherObservation.city == city,
                            WeatherObservation.observation_timestamp == utc_dt
                        ).first()

                        w_dir = wind_dirs[i] if i < len(wind_dirs) else None
                        cardinal = degrees_to_cardinal(w_dir)

                        if exists:
                            # Update existing record with reanalysis variables if missing
                            if exists.boundary_layer_height_m is None and i < len(pblhs):
                                exists.boundary_layer_height_m = pblhs[i]
                            continue

                        weather_rec = WeatherObservation(
                            city=city,
                            latitude=lat,
                            longitude=lng,
                            observation_timestamp=utc_dt,
                            temperature_c=temps[i] if i < len(temps) else None,
                            relative_humidity_pct=humids[i] if i < len(humids) else None,
                            wind_speed_kmh=wind_speeds[i] if i < len(wind_speeds) else None,
                            wind_direction_deg=w_dir,
                            wind_direction_cardinal=cardinal,
                            rainfall_mm=precips[i] if i < len(precips) else 0.0,
                            surface_pressure_hpa=pressures[i] if i < len(pressures) else None,
                            boundary_layer_height_m=pblhs[i] if i < len(pblhs) else None,
                            data_provider="Open-Meteo High-Resolution Atmospheric Reanalysis",
                            data_classification="MODELLED" # Explicitly modelled reanalysis
                        )
                        db.add(weather_rec)
                        processed_count += 1

                    db.commit()

                except Exception as loc_err:
                    logger.error(f"[OPEN_METEO] Error ingesting for {city}: {loc_err}")
                    errors.append(f"{city}: {str(loc_err)}")

            log.status = "SUCCESS" if not errors else "PARTIAL"
            log.records_processed = processed_count
            log.completed_at = datetime.utcnow()
            log.message = (
                f"Successfully ingested {processed_count} atmospheric reanalysis records. "
                f"Classified strictly as MODELLED (Numerical Reanalysis)."
            )
            if errors:
                log.error_details = "\n".join(errors)

            if provider:
                provider.last_synced_at = datetime.utcnow()
                provider.connection_status = "CONNECTED"
                provider.last_error_message = None if not errors else f"Partial issues: {len(errors)}"
            db.commit()

            return {
                "status": log.status,
                "records_processed": processed_count,
                "classification": "MODELLED",
                "errors": errors
            }

        except Exception as e:
            db.rollback()
            err_msg = str(e)
            logger.error(f"[OPEN_METEO] Ingestion failure: {err_msg}")
            log.status = "FAILED"
            log.completed_at = datetime.utcnow()
            log.message = f"Open-Meteo weather ingestion failed: {err_msg}"
            log.error_details = err_msg

            if provider:
                provider.last_failed_at = datetime.utcnow()
                provider.connection_status = "DEGRADED"
                provider.last_error_message = err_msg
            db.commit()

            return {
                "status": "FAILED",
                "records_processed": processed_count,
                "error": err_msg
            }
