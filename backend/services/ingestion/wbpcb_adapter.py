"""
WBPCB Ingestion Adapter
Transparently addresses WBPCB portal realities:
The state portal (https://aqmsdata.wbpcb.gov.in/) does not provide an open, unauthenticated REST API.
Implements a researcher-assisted CSV ingestion workflow for WBPCB portal exports with schema validation,
provenance hashing, and unit preservation.
"""
import io
import csv
import hashlib
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from backend.services.ingestion.base import BaseIngestionAdapter
from backend.models.models import (
    MonitoringStation, ValidatedObservation, RawObservation, DataProvider, IngestionLog
)

logger = logging.getLogger("prana.ingestion.wbpcb")

class WBPCBAdapter(BaseIngestionAdapter):
    def __init__(self):
        super().__init__(provider_code="WBPCB", provider_name="West Bengal Pollution Control Board")

    def parse_wbpcb_export_csv(
        self,
        csv_content: str,
        filename: str,
        db: Session,
        classification: str = "IMPORTED"
    ) -> Dict[str, Any]:
        """
        Parses WBPCB official CSV data exports with multi-format column detection:
        Format A: Wide format (Date, Time, Station, PM2.5, PM10, NO2, ...)
        Format B: Long format (station_code, pollutant, value, unit, timestamp)
        """
        reader = csv.DictReader(io.StringIO(csv_content))
        rows = list(reader)
        if not rows:
            return {"status": "FAILED", "records_processed": 0, "error": "CSV file is empty"}

        fieldnames = [f.strip() for f in (reader.fieldnames or [])]
        stations = db.query(MonitoringStation).all()
        station_code_map = {s.station_code: s for s in stations}
        station_name_map = {s.name.lower(): s for s in stations}

        processed = 0
        flagged = 0
        file_hash = hashlib.sha256(csv_content.encode("utf-8")).hexdigest()

        # Check if Format A (Wide) or Format B (Long)
        is_wide = any("pm2.5" in f.lower() or "pm10" in f.lower() for f in fieldnames)

        if is_wide:
            # Wide Format Parsing
            pollutant_cols = [f for f in fieldnames if f.lower() not in ["date", "time", "timestamp", "station", "station_name", "id", "sl"]]

            for r in rows:
                st_str = r.get("Station") or r.get("station") or r.get("station_name") or ""
                date_str = r.get("Date") or r.get("date") or ""
                time_str = r.get("Time") or r.get("time") or "00:00:00"
                ts_combo = f"{date_str} {time_str}".strip()

                # Find station
                st_match = station_code_map.get(st_str) or station_name_map.get(st_str.lower())
                if not st_match:
                    # Fuzzy match
                    st_match = next((s for s in stations if s.name.lower() in st_str.lower() or st_str.lower() in s.name.lower()), None)
                if not st_match:
                    continue

                try:
                    utc_dt, _ = self.parse_to_utc_and_local(ts_combo)
                except Exception:
                    continue

                for col in pollutant_cols:
                    val_str = r.get(col)
                    if not val_str or val_str.strip() in ["-", "N/A", "NA", ""]:
                        continue

                    try:
                        raw_v = float(val_str.strip())
                    except ValueError:
                        continue

                    pol = self.standardize_pollutant_name(col)
                    unit, norm_v = self.standardize_unit(pol, "ug/m3", raw_v)

                    # Quality checks
                    quality = "VALID"
                    reason = None
                    if norm_v < 0:
                        quality = "SENSOR_FAULT"
                        reason = "Negative concentration"
                        flagged += 1
                    elif norm_v > 1500:
                        quality = "SUSPECT_OUTLIER"
                        reason = "Exceeds physical ambient limit"
                        flagged += 1

                    # Duplicate check
                    exists = db.query(ValidatedObservation).filter(
                        ValidatedObservation.station_id == st_match.id,
                        ValidatedObservation.pollutant == pol,
                        ValidatedObservation.observation_timestamp == utc_dt
                    ).first()

                    if not exists:
                        p_hash = hashlib.sha256(f"WBPCB:{st_match.id}:{pol}:{norm_v}:{utc_dt}".encode()).hexdigest()
                        db.add(ValidatedObservation(
                            station_id=st_match.id,
                            pollutant=pol,
                            normalized_value=norm_v,
                            unit=unit,
                            observation_timestamp=utc_dt,
                            is_valid=(quality == "VALID"),
                            quality_status=quality,
                            data_classification=classification,
                            original_data_provider="WBPCB",
                            original_station_id=st_match.station_code,
                            original_source_record=filename,
                            provenance_hash=p_hash,
                            flag_reason=reason,
                            provenance=f"WBPCB Official Portal Extract ({filename})"
                        ))
                        processed += 1
                        st_match.last_observed_at = utc_dt
        else:
            # Long Format Parsing
            for r in rows:
                st_code = r.get("station_code") or r.get("station") or ""
                pol_raw = r.get("pollutant") or ""
                val_raw = r.get("value") or ""
                unit_raw = r.get("unit") or "ug/m3"
                ts_raw = r.get("timestamp") or ""

                if not (st_code and pol_raw and val_raw and ts_raw):
                    continue

                st_match = station_code_map.get(st_code) or station_name_map.get(st_code.lower())
                if not st_match:
                    continue

                try:
                    raw_v = float(val_raw)
                    utc_dt, _ = self.parse_to_utc_and_local(ts_raw)
                except Exception:
                    continue

                pol = self.standardize_pollutant_name(pol_raw)
                unit, norm_v = self.standardize_unit(pol, unit_raw, raw_v)

                exists = db.query(ValidatedObservation).filter(
                    ValidatedObservation.station_id == st_match.id,
                    ValidatedObservation.pollutant == pol,
                    ValidatedObservation.observation_timestamp == utc_dt
                ).first()

                if not exists:
                    p_hash = hashlib.sha256(f"WBPCB:{st_match.id}:{pol}:{norm_v}:{utc_dt}".encode()).hexdigest()
                    db.add(ValidatedObservation(
                        station_id=st_match.id,
                        pollutant=pol,
                        normalized_value=norm_v,
                        unit=unit,
                        observation_timestamp=utc_dt,
                        is_valid=True,
                        quality_status="VALID",
                        data_classification=classification,
                        original_data_provider="WBPCB",
                        original_station_id=st_match.station_code,
                        original_source_record=filename,
                        provenance_hash=p_hash,
                        provenance=f"Researcher Upload: WBPCB Export ({filename})"
                    ))
                    processed += 1
                    st_match.last_observed_at = utc_dt

        # Log ingestion
        provider = db.query(DataProvider).filter(DataProvider.code == "WBPCB").first()
        log = IngestionLog(
            provider_id=provider.id if provider else None,
            provider_code="WBPCB",
            source_name=f"WBPCB CSV Extract: {filename}",
            started_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
            status="SUCCESS",
            records_processed=processed,
            records_flagged=flagged,
            data_classification=classification,
            message=f"Ingested {processed} observations from WBPCB extract {filename} with SHA-256 fingerprint {file_hash[:16]}..."
        )
        db.add(log)
        if provider:
            provider.last_synced_at = datetime.utcnow()
        db.commit()

        return {
            "status": "SUCCESS",
            "filename": filename,
            "classification": classification,
            "provenance_fingerprint": file_hash,
            "records_processed": processed,
            "records_flagged": flagged
        }

    def ingest(self, db: Session, **kwargs) -> Dict[str, Any]:
        """Automated polling is unavailable for WBPCB; documents the limitation cleanly."""
        provider = db.query(DataProvider).filter(DataProvider.code == "WBPCB").first()
        msg = (
            "WBPCB portal (https://aqmsdata.wbpcb.gov.in/) does not provide an open public REST API. "
            "Automated scraping is prohibited per terms of use. "
            "Please use the researcher-assisted WBPCB CSV Ingestion tool in Data Sources & Quality."
        )
        if provider:
            provider.connection_status = "MANUAL_PORTAL_ONLY"
            provider.last_error_message = msg
            db.commit()

        return {
            "status": "MANUAL_PORTAL_ONLY",
            "provider_code": "WBPCB",
            "message": msg,
            "records_processed": 0
        }
