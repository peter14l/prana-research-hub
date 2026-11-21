"""
PRANA Research Hub - FastAPI Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.database import engine, Base
from backend.routers import (
    overview, live_aq, explorer, hotspots, sources,
    weather, library, interventions, data_quality,
    ai_assistant, export, ingestion, analysis
)
from backend.seed.seed_data import seed_database

# Initialize database schema
Base.metadata.create_all(bind=engine)

# Ensure seed data exists
try:
    seed_database()
except Exception as e:
    print(f"[PRANA Startup] Seed check: {e}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Internal environmental intelligence platform for Kolkata–Howrah outdoor air pollution research.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Accessible to frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(overview.router, prefix=settings.API_V1_PREFIX)
app.include_router(live_aq.router, prefix=settings.API_V1_PREFIX)
app.include_router(explorer.router, prefix=settings.API_V1_PREFIX)
app.include_router(hotspots.router, prefix=settings.API_V1_PREFIX)
app.include_router(sources.router, prefix=settings.API_V1_PREFIX)
app.include_router(weather.router, prefix=settings.API_V1_PREFIX)
app.include_router(library.router, prefix=settings.API_V1_PREFIX)
app.include_router(interventions.router, prefix=settings.API_V1_PREFIX)
app.include_router(data_quality.router, prefix=settings.API_V1_PREFIX)
app.include_router(ai_assistant.router, prefix=settings.API_V1_PREFIX)
app.include_router(export.router, prefix=settings.API_V1_PREFIX)
app.include_router(ingestion.router, prefix=settings.API_V1_PREFIX)
app.include_router(analysis.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
@app.get("/health")
def health_check():
    return {
        "status": "ONLINE",
        "service": "PRANA Research Hub API",
        "region": "Kolkata–Howrah, West Bengal",
        "version": "1.0.0",
        "endpoints": f"{settings.API_V1_PREFIX}/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
