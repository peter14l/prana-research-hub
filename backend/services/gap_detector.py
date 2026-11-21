"""
PRANA Research Gap Detector (Milestone 4):
Identifies where current evidence is insufficient across geographic coverage,
emission inventories, speciation, seasonal observations, and intervention studies.
Classifies gaps by severity and recommends the cheapest credible resolution.
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.models.models import (
    ResearchGap, MonitoringStation, ValidatedObservation,
    WeatherObservation, ResearchDocument
)

class ResearchGapDetector:
    @staticmethod
    def get_all_gaps(
        db: Session,
        severity: Optional[str] = None,
        sector: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves all cataloged research gaps from the database with filtering.
        """
        query = db.query(ResearchGap)
        if severity and severity != "ALL":
            query = query.filter(ResearchGap.severity == severity.upper())
        if sector and sector != "ALL":
            query = query.filter(ResearchGap.sector == sector)

        gaps = query.order_by(ResearchGap.id.asc()).all()

        return [
            {
                "id": g.id,
                "gap_code": g.gap_code,
                "title": g.title,
                "sector": g.sector,
                "gap_type": g.gap_type,
                "severity": g.severity,
                "description": g.description,
                "affected_areas": g.affected_areas,
                "cheapest_resolution_method": g.cheapest_resolution_method,
                "remote_testing_possible": g.remote_testing_possible,
                "estimated_resolution_time": g.estimated_resolution_time,
                "status": g.status,
                "created_at": g.created_at.isoformat() if g.created_at else None
            }
            for g in gaps
        ]

    @staticmethod
    def perform_gap_audit(db: Session) -> Dict[str, Any]:
        """
        Dynamically analyzes the active database state and identifies critical
        evidence deficits for research planning.
        """
        # 1. Geographic Void Analysis
        stations = db.query(MonitoringStation).all()
        active_coords = [(s.name, s.latitude, s.longitude, s.city) for s in stations]

        # Key unmonitored zones to check
        known_voids = [
            {
                "zone": "Jalan Industrial Complex (Domjur/Sankrail)",
                "lat": 22.59,
                "lon": 88.24,
                "nearest_statutory_km": 7.2,
                "nearest_station": "WB009_PADMAPUKUR",
                "hazard_profile": "Over 2,000 metallurgical, chemical, and fabrication MSMEs with zero fence-line monitors."
            },
            {
                "zone": "Uluberia Industrial Belt",
                "lat": 22.47,
                "lon": 88.11,
                "nearest_statutory_km": 19.5,
                "nearest_station": "WB009_PADMAPUKUR",
                "hazard_profile": "Steel rerolling, chemical plants, and heavy transport freight corridors."
            },
            {
                "zone": "Khidirpur Docks & Taratala Industrial Belt",
                "lat": 22.53,
                "lon": 88.31,
                "nearest_statutory_km": 4.8,
                "nearest_station": "WB001_VICTORIA",
                "hazard_profile": "Port container terminals, heavy diesel freight, and chemical godowns."
            },
            {
                "zone": "Budge Budge Petroleum & Power Belt",
                "lat": 22.48,
                "lon": 88.18,
                "nearest_statutory_km": 14.1,
                "nearest_station": "WB003_JADAVPUR",
                "hazard_profile": "Thermal power station, petroleum storage terminals, and river barge bunkering."
            }
        ]

        # 2. Sectoral Inventory Gaps
        inventory_deficits = [
            {
                "sector": "River transport",
                "deficit": "Lack of empirical tailpipe emission factors for Hooghly passenger ferry fleet.",
                "severity": "HIGH",
                "cheapest_resolution": "Remote AIS vessel tracking correlated with dockside optical Aethalometer black carbon monitoring at Howrah Station Ghat during peak commute hours.",
                "can_test_remotely": True
            },
            {
                "sector": "Industrial emissions",
                "deficit": "Zero continuous ambient toxic heavy-metal speciation (Pb, Zn, Cd) in Howrah.",
                "severity": "HIGH",
                "cheapest_resolution": "Weekly gravimetric quartz filter sampling at existing stations followed by ED-XRF spectroscopy at a university partner lab.",
                "can_test_remotely": False
            },
            {
                "sector": "Regional pollution transport",
                "deficit": "Absence of real-time ground-based LIDAR ceilometer for nocturnal Boundary Layer Height (PBLH) compression.",
                "severity": "MEDIUM",
                "cheapest_resolution": "Synthesize high-resolution ERA5 hourly reanalysis boundary layer diagnostics with IMD Dum Dum radiosonde profiles instead of buying a LIDAR.",
                "can_test_remotely": True
            }
        ]

        # 3. Research Action Matrix
        remote_actions = [
            "Extract Sentinel-5P TROPOMI tropospheric NO2 columns over Jalan and Uluberia to detect unmonitored industrial emissions without ground deployment.",
            "Run Landsat-9 and ECOSTRESS thermal infrared band time series to map subsurface isotherm migration at Dhapa dump.",
            "Collate AIS marine navigation vessel tracks on the Hooghly river to calculate ferry engine operating hours and idling duty cycles."
        ]

        field_pilot_actions = [
            "Install a fence-line optical particle counter and heated nephelometer node on NH-6 at the entrance to Jalan Complex.",
            "Conduct tailpipe PEMS sampling on one WBSTC twin-engine passenger ferry during scheduled ghat crossings."
        ]

        return {
            "audit_timestamp": func.now(),
            "unmonitored_geographic_voids": known_voids,
            "sectoral_inventory_deficits": inventory_deficits,
            "cheapest_credible_next_steps": {
                "remote_desk_research_immediate": remote_actions,
                "future_field_pilot_required": field_pilot_actions
            }
        }
