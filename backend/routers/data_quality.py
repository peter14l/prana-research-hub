"""
Data Sources & Quality router:
Data provenance, ingestion auditing, outlier inspections, and CSV import workflow.
"""
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
import io
import csv
from datetime import datetime
from backend.database import get_db
from backend.models.models import (
    DataProvider, IngestionLog, ValidatedObservation, MonitoringStation, RawObservation
)

router = APIRouter(prefix="/quality", tags=["Data Quality & Integrity"])

@router.get("/providers")
def get_providers(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    providers = db.query(DataProvider).all()
    return [
        {
            "id": p.id,
            "code": p.code,
            "name": p.name,
            "provider_type": p.provider_type,
            "portal_url": p.portal_url,
            "description": p.description,
            "status": p.status,
            "last_synced_at": p.last_synced_at.isoformat() if p.last_synced_at else None
        }
        for p in providers
    ]

@router.get("/audit")
def get_quality_audit(db: Session = Depends(get_db)) -> Dict[str, Any]:
    total_validated = db.query(ValidatedObservation).count()
    valid_count = db.query(ValidatedObservation).filter_by(is_valid=True).count()
    flagged_count = db.query(ValidatedObservation).filter(ValidatedObservation.quality_status != "VALID").count()
    
    # Recent flagged observations
    flagged_samples = (
        db.query(ValidatedObservation, MonitoringStation.name.label("station_name"))
        .join(MonitoringStation, ValidatedObservation.station_id == MonitoringStation.id)
        .filter(ValidatedObservation.quality_status != "VALID")
        .order_by(ValidatedObservation.observation_timestamp.desc())
        .limit(20)
        .all()
    )

    logs = db.query(IngestionLog).order_by(IngestionLog.started_at.desc()).limit(10).all()

    return {
        "total_records": total_validated,
        "valid_records": valid_count,
        "flagged_records": flagged_count,
        "completeness_rate_pct": round((valid_count / total_validated * 100.0) if total_validated > 0 else 100.0, 2),
        "flagged_samples": [
            {
                "id": obs.ValidatedObservation.id,
                "station_name": obs.station_name,
                "pollutant": obs.ValidatedObservation.pollutant,
                "value": obs.ValidatedObservation.normalized_value,
                "unit": obs.ValidatedObservation.unit,
                "quality_status": obs.ValidatedObservation.quality_status,
                "flag_reason": obs.ValidatedObservation.flag_reason,
                "timestamp": obs.ValidatedObservation.observation_timestamp.isoformat()
            }
            for obs in flagged_samples
        ],
        "ingestion_logs": [
            {
                "id": l.id,
                "source_name": l.source_name,
                "status": l.status,
                "records_processed": l.records_processed,
                "records_flagged": l.records_flagged,
                "message": l.message,
                "started_at": l.started_at.isoformat() if l.started_at else None
            }
            for l in logs
        ]
    }

@router.post("/import-csv")
async def import_csv_observations(
    file: UploadFile = File(...),
    provider_code: str = Form("MANUAL_CSV_IMPORT"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Ingests research observation CSV with validation and provenance tracking.
    Required CSV columns: station_code, pollutant, value, unit, timestamp
    """
    content = await file.read()
    decoded = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(decoded))
    
    processed = 0
    flagged = 0
    stations_cache = {s.station_code: s.id for s in db.query(MonitoringStation).all()}

    for row in reader:
        st_code = row.get("station_code") or row.get("station")
        pollutant = row.get("pollutant")
        val_str = row.get("value")
        unit = row.get("unit", "ug/m3")
        ts_str = row.get("timestamp")

        if not (st_code and pollutant and val_str and ts_str):
            continue

        station_id = stations_cache.get(st_code)
        if not station_id:
            continue

        try:
            val = float(val_str)
            dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00")).replace(tzinfo=None)
        except Exception:
            continue

        # Quality check: negative or extreme spike
        quality = "VALID"
        flag_reason = None
        if val < 0:
            quality = "SENSOR_FAULT"
            flag_reason = "Negative concentration rejected"
            flagged += 1
        elif val > 1500:
            quality = "SUSPECT_OUTLIER"
            flag_reason = "Concentration exceeds physical ambient threshold (1500 ug/m3)"
            flagged += 1

        raw = RawObservation(
            station_id=station_id,
            pollutant=pollutant,
            raw_value=val,
            original_unit=unit,
            observation_timestamp=dt,
            provider_code=provider_code,
            raw_payload={"source_file": file.filename}
        )
        db.add(raw)
        db.flush()

        val_obs = ValidatedObservation(
            raw_id=raw.id,
            station_id=station_id,
            pollutant=pollutant,
            normalized_value=val,
            unit=unit,
            observation_timestamp=dt,
            is_valid=(quality == "VALID"),
            quality_status=quality,
            flag_reason=flag_reason,
            provenance=f"CSV Import: {file.filename}"
        )
        db.add(val_obs)
        processed += 1

    log = IngestionLog(
        source_name=f"Manual CSV: {file.filename}",
        status="SUCCESS",
        records_processed=processed,
        records_flagged=flagged,
        message=f"Ingested {processed} records from {file.filename}. {flagged} flagged by quality gate."
    )
    db.add(log)
    db.commit()

    return {
        "status": "SUCCESS",
        "filename": file.filename,
        "records_processed": processed,
        "records_flagged": flagged
    }
