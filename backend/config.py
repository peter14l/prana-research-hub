"""
PRANA Research Hub Backend Configuration
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "PRANA Research Hub"
    API_V1_PREFIX: str = "/api"
    
    # Database: Default to embedded SQLite file in backend/data (zero external database / docker needed)
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'data' / 'prana.db'}")
    
    # Study Region: Kolkata–Howrah Twin Cities, West Bengal, India
    REGION_NAME: str = "Kolkata–Howrah"
    REGION_BOUNDS: dict = {
        "min_lat": 22.45,
        "max_lat": 22.68,
        "min_lng": 88.22,
        "max_lng": 88.48,
        "center_lat": 22.5726,
        "center_lng": 88.3639
    }
    
    # OpenAQ API (v3) - Key optional, public tier accessible
    OPENAQ_API_KEY: str = os.getenv("OPENAQ_API_KEY", "")
    OPENAQ_BASE_URL: str = "https://api.openaq.org/v3"
    
    # Open-Meteo API (Free, high-resolution meteorological reanalysis & forecast)
    OPEN_METEO_URL: str = "https://archive-api.open-meteo.com/v1/archive"
    OPEN_METEO_CURRENT_URL: str = "https://api.open-meteo.com/v1/forecast"
    
    # Optional Gemini / AI Assistant Key
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    class Config:
        case_sensitive = True

settings = Settings()
