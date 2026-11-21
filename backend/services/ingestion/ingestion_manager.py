"""
PRANA Automated Ingestion Manager
Orchestrates multi-provider ingestion (OpenAQ v3, Open-Meteo, WBPCB, CPCB)
with failure isolation, status tracking, and logging.
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from backend.models.models import DataProvider, IngestionLog
from backend.services.ingestion.openaq_adapter import OpenAQV3Adapter
from backend.services.ingestion.openmeteo_adapter import OpenMeteoAdapter
from backend.services.ingestion.wbpcb_adapter import WBPCBAdapter
from backend.services.ingestion.cpcb_adapter import CPCBAdapter

logger = logging.getLogger("prana.ingestion.manager")

class IngestionManager:
    def __init__(self):
        self.openaq_adapter = OpenAQV3Adapter()
        self.openmeteo_adapter = OpenMeteoAdapter()
        self.wbpcb_adapter = WBPCBAdapter()
        self.cpcb_adapter = CPCBAdapter()

    def refresh_provider(self, db: Session, provider_code: str, **kwargs) -> Dict[str, Any]:
        """Refreshes a single provider with isolated error containment."""
        code = provider_code.upper()
        logger.info(f"[INGESTION] Triggering refresh for provider: {code}")

        if code == "OPENAQ":
            return self.openaq_adapter.ingest(db, **kwargs)
        elif code in ["OPEN_METEO", "OPENMETEO"]:
            return self.openmeteo_adapter.ingest(db, **kwargs)
        elif code == "WBPCB":
            return self.wbpcb_adapter.ingest(db, **kwargs)
        elif code == "CPCB":
            return self.cpcb_adapter.ingest(db, **kwargs)
        else:
            raise ValueError(f"Unknown provider code: {provider_code}")

    def refresh_all(self, db: Session, fetch_historical: bool = False, days_back: int = 3) -> Dict[str, Any]:
        """
        Executes a full ingestion cycle across all providers in isolation.
        A failure in one provider (e.g. OpenAQ or CPCB) does NOT stop other providers (e.g. Open-Meteo).
        """
        results = {}

        # 1. OpenAQ
        try:
            results["OPENAQ"] = self.openaq_adapter.ingest(db, fetch_historical=fetch_historical, days_back=days_back)
        except Exception as e:
            logger.error(f"[INGESTION] OpenAQ runner error: {e}")
            results["OPENAQ"] = {"status": "FAILED", "error": str(e)}

        # 2. Open-Meteo
        try:
            results["OPEN_METEO"] = self.openmeteo_adapter.ingest(db, past_days=days_back)
        except Exception as e:
            logger.error(f"[INGESTION] Open-Meteo runner error: {e}")
            results["OPEN_METEO"] = {"status": "FAILED", "error": str(e)}

        # 3. WBPCB
        try:
            results["WBPCB"] = self.wbpcb_adapter.ingest(db)
        except Exception as e:
            results["WBPCB"] = {"status": "FAILED", "error": str(e)}

        # 4. CPCB
        try:
            results["CPCB"] = self.cpcb_adapter.ingest(db)
        except Exception as e:
            results["CPCB"] = {"status": "FAILED", "error": str(e)}

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "results": results
        }

    @staticmethod
    def get_provider_statuses(db: Session) -> List[Dict[str, Any]]:
        """Returns live status, last fetch time, error message, and total records processed per provider."""
        providers = db.query(DataProvider).all()
        status_list = []

        for p in providers:
            # Query latest log for total records processed
            logs = db.query(IngestionLog).filter(
                (IngestionLog.provider_id == p.id) | (IngestionLog.provider_code == p.code)
            ).order_by(IngestionLog.started_at.desc()).limit(1).all()

            latest_log = logs[0] if logs else None
            
            status_list.append({
                "provider_code": p.code,
                "name": p.name,
                "connection_status": p.connection_status,
                "retrieval_method": p.retrieval_method,
                "last_successful_fetch": p.last_synced_at.isoformat() if p.last_synced_at else None,
                "last_failed_at": p.last_failed_at.isoformat() if p.last_failed_at else None,
                "last_error_message": p.last_error_message,
                "latest_log_status": latest_log.status if latest_log else "NO_LOGS",
                "latest_records_processed": latest_log.records_processed if latest_log else 0,
                "latest_log_message": latest_log.message if latest_log else None
            })

        return status_list

    @staticmethod
    def get_ingestion_logs(db: Session, limit: int = 50) -> List[Dict[str, Any]]:
        """Returns recent ingestion pipeline logs."""
        logs = db.query(IngestionLog).order_by(IngestionLog.started_at.desc()).limit(limit).all()
        return [
            {
                "id": log.id,
                "provider_code": log.provider_code,
                "source_name": log.source_name,
                "started_at": log.started_at.isoformat() if log.started_at else None,
                "completed_at": log.completed_at.isoformat() if log.completed_at else None,
                "status": log.status,
                "records_processed": log.records_processed,
                "records_flagged": log.records_flagged,
                "data_classification": log.data_classification,
                "message": log.message,
                "error_details": log.error_details
            }
            for log in logs
        ]
