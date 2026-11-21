"""
PRANA Dhapa Remote Fire Intelligence Router
Exposes endpoints for satellite thermal observations, AOI boundaries,
spatial/temporal analysis, and scientific feasibility assessments.
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from backend.services.dhapa_fire_service import DhapaFireService
from backend.services.dhapa_fire_analyzer import DhapaFireAnalyzer

router = APIRouter(prefix="/dhapa-fire", tags=["Dhapa Remote Fire Intelligence"])

# Singletons for services
_service = DhapaFireService()
_analyzer = DhapaFireAnalyzer(_service)

@router.get("/aoi")
def get_aoi_geojson():
    """Returns Dhapa Landfill Area of Interest (AOI) polygon, 1 km buffer, and 2 km buffer in GeoJSON."""
    return _service.get_aoi_geojson()

@router.get("/summary")
def get_fire_summary():
    """Returns high-level summary of satellite observations, hotspot recurrence, and feasibility verdict."""
    spatial = _analyzer.analyze_spatial_clustering()
    temporal = _analyzer.analyze_temporal_distribution()
    feasibility = _analyzer.evaluate_spaceborne_early_warning_feasibility()
    
    return {
        "site_name": "Dhapa Municipal Solid Waste Disposal Ground",
        "jurisdiction": "Kolkata Municipal Corporation (KMC)",
        "core_area_hectares": 58.4,
        "centroid": {"latitude": 22.5453, "longitude": 88.4257},
        "total_detections_cataloged": temporal["total_detections"],
        "core_aoi_detections": temporal["core_aoi_detections"],
        "peak_season": temporal["peak_fire_season"],
        "hotspot_clusters_identified": len(spatial.get("hotspot_clusters", [])),
        "feasibility_verdict": feasibility["verdict"],
        "executive_conclusion": feasibility["executive_conclusion"],
        "recommended_pathway": feasibility["defensible_alternative_engineering_pathway"]["recommended_technology"]
    }

@router.get("/detections")
def get_detections(
    zone: Optional[str] = Query(None, description="Filter by zone: CORE_AOI, BUFFER_1KM, BUFFER_2KM, GREATER_KOLKATA, REGIONAL"),
    min_confidence: Optional[str] = Query(None, description="Minimum confidence: low, nominal, high")
):
    """Returns catalog of satellite thermal detections with preserved provenance and physical metadata."""
    return {
        "count": len(_service.get_detections(zone=zone, min_confidence=min_confidence)),
        "detections": _service.get_detections(zone=zone, min_confidence=min_confidence)
    }

@router.get("/spatial-analysis")
def get_spatial_analysis():
    """Returns spatial clustering, buffer density comparison (detections/km2), and hotspot clusters."""
    return _analyzer.analyze_spatial_clustering()

@router.get("/temporal-analysis")
def get_temporal_analysis():
    """Returns temporal breakdown by year, month, and season for Core AOI and regional context."""
    return _analyzer.analyze_temporal_distribution()

@router.get("/confidence-distribution")
def get_confidence_distribution():
    """Returns distribution of satellite detection confidence classes."""
    return _analyzer.analyze_confidence_distribution()

@router.get("/cloud-limitations")
def get_cloud_limitations():
    """Returns Landsat 8/9 STAC cloud cover statistics, overpass gaps, and monsoon blindness evaluation."""
    return _analyzer.analyze_cloud_limitations()

@router.get("/ground-comparison")
def get_ground_comparison():
    """Returns nearby CAAQM ground monitoring station comparison, meteorology, and causality vs association audit."""
    return _analyzer.compare_with_prana_ground_data()

@router.get("/feasibility-verdict")
def get_feasibility_verdict():
    """Returns comprehensive scientific assessment on the viability of spaceborne fire monitoring."""
    return _analyzer.evaluate_spaceborne_early_warning_feasibility()
