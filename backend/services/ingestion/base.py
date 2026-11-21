"""
Base Ingestion Adapter & Utilities
Provides exponential backoff retry, rate-limiting, and timezone normalization.
"""
import time
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime, timezone, timedelta
import zoneinfo

logger = logging.getLogger("prana.ingestion")

# Kolkata Timezone (+05:30)
try:
    KOLKATA_TZ = zoneinfo.ZoneInfo("Asia/Kolkata")
except Exception:
    KOLKATA_TZ = timezone(timedelta(hours=5, minutes=30))

class BaseIngestionAdapter(ABC):
    def __init__(self, provider_code: str, provider_name: str):
        self.provider_code = provider_code
        self.provider_name = provider_name

    def execute_with_retry(
        self,
        func: Callable,
        max_retries: int = 3,
        base_delay: float = 1.0,
        retry_exceptions: tuple = (Exception,)
    ) -> Any:
        """Executes a callable with exponential backoff and jitter."""
        retries = 0
        delay = base_delay
        last_exception = None

        while retries < max_retries:
            try:
                return func()
            except retry_exceptions as e:
                retries += 1
                last_exception = e
                logger.warning(
                    f"[{self.provider_code}] Attempt {retries}/{max_retries} failed: {e}. "
                    f"Retrying in {delay:.2f}s..."
                )
                time.sleep(delay)
                delay *= 2.0

        logger.error(f"[{self.provider_code}] All {max_retries} retry attempts failed: {last_exception}")
        raise last_exception

    @staticmethod
    def parse_to_utc_and_local(ts_input: Any) -> tuple[datetime, datetime]:
        """
        Parses an ISO timestamp string or datetime object into:
        (utc_datetime_naive, kolkata_datetime)
        """
        if isinstance(ts_input, str):
            clean_str = ts_input.replace("Z", "+00:00")
            dt = datetime.fromisoformat(clean_str)
        elif isinstance(ts_input, datetime):
            dt = ts_input
        else:
            raise ValueError(f"Cannot parse timestamp: {ts_input}")

        if dt.tzinfo is None:
            # Assume UTC if naive
            utc_dt = dt
            local_dt = dt.replace(tzinfo=timezone.utc).astimezone(KOLKATA_TZ)
        else:
            utc_dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
            local_dt = dt.astimezone(KOLKATA_TZ)

        return utc_dt, local_dt

    @staticmethod
    def standardize_pollutant_name(param_str: str) -> str:
        """Normalizes external API pollutant strings to PRANA standard conventions."""
        p = param_str.strip().lower()
        if p in ["pm25", "pm2.5", "pm_2.5", "particulate matter < 2.5 µm"]:
            return "PM2.5"
        if p in ["pm10", "pm_10", "particulate matter < 10 µm"]:
            return "PM10"
        if p in ["no2", "nitrogen dioxide"]:
            return "NO2"
        if p in ["so2", "sulfur dioxide"]:
            return "SO2"
        if p in ["co", "carbon monoxide"]:
            return "CO"
        if p in ["o3", "ozone"]:
            return "O3"
        if p in ["nh3", "ammonia"]:
            return "NH3"
        return param_str.upper()

    @staticmethod
    def standardize_unit(pollutant: str, raw_unit: str, raw_value: float) -> tuple[str, float]:
        """
        Standardizes concentration units:
        PM2.5, PM10, NO2, SO2, O3, NH3 -> ug/m3
        CO -> mg/m3
        Converts ppb or ppm using standard ambient molecular weights at 25°C, 1 atm.
        """
        u = raw_unit.lower().replace("µ", "u").strip()
        val = float(raw_value)

        # Standard targets
        if pollutant == "CO":
            if "ppm" in u:
                return "mg/m3", round(val * 1.145, 2) # CO: 1 ppm ≈ 1.145 mg/m3
            return "mg/m3", round(val, 2)

        # For NO2: 1 ppb ≈ 1.88 ug/m3
        if pollutant == "NO2" and "ppb" in u:
            return "ug/m3", round(val * 1.88, 2)

        # For SO2: 1 ppb ≈ 2.62 ug/m3
        if pollutant == "SO2" and "ppb" in u:
            return "ug/m3", round(val * 2.62, 2)

        # For O3: 1 ppb ≈ 2.0 ug/m3
        if pollutant == "O3" and "ppb" in u:
            return "ug/m3", round(val * 2.0, 2)

        return "ug/m3", round(val, 2)

    @abstractmethod
    def ingest(self, db: Any, **kwargs) -> Dict[str, Any]:
        """Ingests observations from the provider."""
        pass
