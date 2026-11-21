"""
Pydantic schemas for data serialization and validation (Milestone 2)
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class DataProviderBase(BaseModel):
    code: str
    name: str
    provider_type: str = "OFFICIAL"
    portal_url: Optional[str] = None
    description: Optional[str] = None
    status: str = "ACTIVE"
    connection_status: str = "CONNECTED"
    retrieval_method: str = "REST_API"

class DataProviderOut(DataProviderBase):
    id: int
    last_synced_at: Optional[datetime] = None
    last_failed_at: Optional[datetime] = None
    last_error_message: Optional[str] = None

    class Config:
        from_attributes = True

class SensorOut(BaseModel):
    id: int
    pollutant: str
    unit: str
    sensor_model: Optional[str] = None
    sampling_interval: str = "1-hour"
    is_active: bool = True

    class Config:
        from_attributes = True

class MonitoringStationOut(BaseModel):
    id: int
    station_code: str
    cpcb_site_id: Optional[str] = None
    name: str
    city: str
    area_type: str
    address: Optional[str] = None
    latitude: float
    longitude: float
    elevation: Optional[float] = None
    provider_id: int
    active: bool
    is_demo: bool
    commissioned_date: Optional[str] = None
    verification_status: str = "VERIFIED"
    verification_date: Optional[str] = None
    verification_source_url: Optional[str] = None
    verified_parameters: Optional[str] = None
    verification_notes: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = None
    sensors: List[SensorOut] = []

    class Config:
        from_attributes = True

class ValidatedObservationOut(BaseModel):
    id: int
    station_id: int
    pollutant: str
    normalized_value: float
    unit: str
    observation_timestamp: datetime
    is_valid: bool
    quality_status: str
    data_classification: str = "DEMO"
    original_data_provider: Optional[str] = None
    original_station_id: Optional[str] = None
    provenance_hash: Optional[str] = None
    z_score: Optional[float] = None
    flag_reason: Optional[str] = None
    provenance: str

    class Config:
        from_attributes = True

class StationAQIOut(BaseModel):
    id: int
    station_id: int
    timestamp: datetime
    aqi_value: Optional[int]
    category: Optional[str]
    dominant_pollutant: Optional[str]
    sub_indices: Optional[Dict[str, Any]]
    is_valid_cpcb: bool
    methodology: str
    data_classification: str = "DERIVED"

    class Config:
        from_attributes = True

class WeatherObservationOut(BaseModel):
    id: int
    city: str
    latitude: float
    longitude: float
    observation_timestamp: datetime
    temperature_c: Optional[float]
    relative_humidity_pct: Optional[float]
    wind_speed_kmh: Optional[float]
    wind_direction_deg: Optional[float]
    wind_direction_cardinal: Optional[str]
    rainfall_mm: Optional[float]
    surface_pressure_hpa: Optional[float]
    boundary_layer_height_m: Optional[float]
    data_provider: str
    data_classification: str = "DEMO"

    class Config:
        from_attributes = True

class ResearchDocumentOut(BaseModel):
    id: int
    title: str
    organisation: str
    publication_date: str
    geographic_coverage: str
    pollutants_studied: str
    methodology: str
    key_findings: str
    limitations: str
    original_url: Optional[str]
    study_type: str
    confidence_tier: str
    tags: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class ResearchFindingOut(BaseModel):
    id: int
    document_id: int
    finding_type: str
    title: str
    statement: str
    citation_reference: Optional[str] = None
    page_number: Optional[str] = None
    table_figure_ref: Optional[str] = None
    has_supporting_reference: bool = True
    confidence: str

    class Config:
        from_attributes = True

class ResearchNoteCreate(BaseModel):
    document_id: Optional[int] = None
    station_id: Optional[int] = None
    title: str
    content: str
    tags: Optional[str] = None

class ResearchNoteOut(BaseModel):
    id: int
    document_id: Optional[int]
    station_id: Optional[int]
    title: str
    content: str
    tags: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class SourceCategoryOut(BaseModel):
    id: int
    code: str
    name: str
    sector: str
    description: Optional[str]
    primary_pollutants: str
    typical_marker_species: Optional[str]

    class Config:
        from_attributes = True

class SourceContributionProfileOut(BaseModel):
    id: int
    study_id: int
    category_id: int
    pollutant: str
    season: str
    city: str
    contribution_percentage: float
    concentration_ugm3: Optional[float]
    uncertainty_min: Optional[float]
    uncertainty_max: Optional[float]
    evidence_type: str
    citation_reference: Optional[str] = None
    page_number: Optional[str] = None
    table_figure_ref: Optional[str] = None
    has_supporting_reference: bool = True
    category_name: Optional[str] = None
    study_name: Optional[str] = None

    class Config:
        from_attributes = True

class InterventionHypothesisCreate(BaseModel):
    title: str
    problem_statement: str
    target_area: str
    target_pollutant: str = "PM2.5 & PM10"
    suspected_source: str
    supporting_evidence: str
    proposed_intervention: str
    mechanism_of_action: str
    required_resources: str
    possible_implementation_partner: str
    measurable_indicators: str
    risks_limitations: str
    research_confidence: str = "MEDIUM"
    validation_requirements: str
    feasibility_score: float = 7.0
    potential_reduction_score: float = 8.0
    cost_complexity_score: float = 6.0
    ease_of_verification_score: float = 7.5
    scalability_score: float = 8.0
    evaluation_framework: Optional[Dict[str, Any]] = None

class InterventionHypothesisOut(InterventionHypothesisCreate):
    id: int
    status: str
    data_classification: str = "RESEARCH_HYPOTHESIS"
    created_at: datetime

    class Config:
        from_attributes = True

class RegionalSummaryOut(BaseModel):
    region: str
    timestamp: str
    pm25_avg: Optional[float]
    pm10_avg: Optional[float]
    no2_avg: Optional[float]
    so2_avg: Optional[float]
    co_avg: Optional[float]
    o3_avg: Optional[float]
    reporting_stations: int
    stale_stations: int
    total_stations: int
    dominant_category: str
    data_integrity: Optional[Dict[str, Any]] = None
    highlights: List[Dict[str, Any]]
