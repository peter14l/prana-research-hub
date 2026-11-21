"""
PRANA Research Hub - Automated Ingestion Router (Milestone 3)
Provides endpoints for:
- Manual & scheduled refresh triggering across OpenAQ v3, Open-Meteo, WBPCB, CPCB
- Live telemetry provider status
- Ingestion pipeline logs
- Dedicated official CSV import for WBPCB and CPCB CCR formats
"""
from fastapi import APIRouter, Depends, Query, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime

from backend.database import get_db
from backend.services.ingestion.ingestion_manager import IngestionManager
from backend.services.ingestion.wbpcb_adapter import WBPCBAdapter
from backend.services.ingestion.cpcb_adapter import CPCBAdapter
from backend.models.schemas import IngestionRefreshRequest, IngestionStatusOut

router = APIRouter(prefix="/ingestion", tags=["Automated Data Ingestion"])
manager = IngestionManager()
wbpcb_adapter = WBPCBAdapter()
cpcb_adapter = CPCBAdapter()

@router.post("/refresh")
def trigger_refresh(
    req: IngestionRefreshRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Triggers automated ingestion refresh.
    If provider_code is omitted, executes refresh across all providers in isolation.
    """
    if req.provider_code:
        code = req.provider_code.upper()
        res = manager.refresh_provider(db, code, fetch_historical=req.force_historical, days_back=req.days_back)
        return {"status": "COMPLETED", "provider": code, "result": res}
    else:
        summary = manager.refresh_all(db, fetch_historical=req.force_historical, days_back=req.days_back)
        return {"status": "COMPLETED", "summary": summary}

@router.get("/status")
def get_ingestion_statuses(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """Returns real-time connection status, telemetry health, and last fetch timestamp per provider."""
    return manager.get_provider_statuses(db)

@router.get("/logs")
def get_ingestion_logs(
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Returns recent historical ingestion logs."""
    return manager.get_ingestion_logs(db, limit=limit)

@router.post("/wbpcb-csv")
async def import_wbpcb_csv(
    file: UploadFile = File(...),
    classification: str = Form("IMPORTED"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Researcher-assisted ingestion of official WBPCB portal CSV extracts."""
    content = await file.read()
    decoded = content.decode("utf-8-sig")
    return wbpcb_adapter.parse_wbpcb_export_csv(
        csv_content=decoded,
        filename=file.filename,
        db=db,
        classification=classification
    )

@router.post("/cpcb-ccr-csv")
async def import_cpcb_ccr_csv(
    file: UploadFile = File(...),
    classification: str = Form("IMPORTED"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Researcher-assisted ingestion of official CPCB CCR CSV extracts.
    Strictly separates official AQI index values into StationAQIRecord from individual concentrations.
    """
    content = await file.read()
    decoded = content.decode("utf-8-sig")
    return cpcb_adapter.parse_cpcb_ccr_csv(
        csv_content=decoded,
        filename=file.filename,
        db=db,
        classification=classification
    )
