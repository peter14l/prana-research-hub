"""
PRANA Modular Ingestion Services
"""
from backend.services.ingestion.base import BaseIngestionAdapter
from backend.services.ingestion.openaq_adapter import OpenAQV3Adapter
from backend.services.ingestion.openmeteo_adapter import OpenMeteoAdapter
from backend.services.ingestion.wbpcb_adapter import WBPCBAdapter
from backend.services.ingestion.cpcb_adapter import CPCBAdapter
from backend.services.ingestion.ingestion_manager import IngestionManager

__all__ = [
    "BaseIngestionAdapter",
    "OpenAQV3Adapter",
    "OpenMeteoAdapter",
    "WBPCBAdapter",
    "CPCBAdapter",
    "IngestionManager"
]
