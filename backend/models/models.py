"""
SQLAlchemy models for PRANA Research Hub (Milestone 2 - Data Provenance & Integrity)
"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
)
from sqlalchemy.orm import relationship
from backend.database import Base

class DataProvider(Base):
    __tablename__ = "data_providers"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False) # e.g. "WBPCB", "CPCB", "OPENAQ", "OPEN_METEO"
    name = Column(String(150), nullable=False)
    provider_type = Column(String(50), default="OFFICIAL") # OFFICIAL, RESEARCH, SATELLITE, COMMUNITY
    portal_url = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String(30), default="ACTIVE") # ACTIVE, DEGRADED, OFFLINE
    connection_status = Column(String(50), default="CONNECTED") # CONNECTED, DEGRADED, DISCONNECTED, AUTH_REQUIRED, MANUAL_PORTAL_ONLY
    last_synced_at = Column(DateTime, nullable=True)
    last_failed_at = Column(DateTime, nullable=True)
    last_error_message = Column(Text, nullable=True)
    retrieval_method = Column(String(50), default="REST_API") # REST_API, MANUAL_CSV_IMPORT, REANALYSIS_API
    available_date_range_start = Column(DateTime, nullable=True)
    available_date_range_end = Column(DateTime, nullable=True)

    stations = relationship("MonitoringStation", back_populates="provider")
    ingestion_logs = relationship("IngestionLog", back_populates="provider_rel")

class MonitoringStation(Base):
    __tablename__ = "monitoring_stations"

    id = Column(Integer, primary_key=True, index=True)
    station_code = Column(String(50), unique=True, index=True, nullable=False) # e.g. "WB001_VICTORIA", "WB007_GHUSURI"
    cpcb_site_id = Column(String(50), nullable=True) # e.g. "site_5002"
    name = Column(String(150), nullable=False)
    city = Column(String(50), nullable=False) # "Kolkata" or "Howrah"
    area_type = Column(String(50), default="Urban") # "Commercial", "Residential", "Industrial", "Background", "Traffic"
    address = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    elevation = Column(Float, nullable=True)
    provider_id = Column(Integer, ForeignKey("data_providers.id"), nullable=False)
    active = Column(Boolean, default=True)
    is_demo = Column(Boolean, default=False)
    commissioned_date = Column(String(20), nullable=True)
    
    # Milestone 2: Station Verification Registry
    verification_status = Column(String(50), default="VERIFIED") # VERIFIED, PENDING_AUDIT, UNVERIFIED, DISCREPANCY_FLAGGED
    verification_date = Column(String(30), default="2026-11-21")
    verification_source_url = Column(String(255), default="https://app.cpcbccr.com/ccr_docs")
    verified_parameters = Column(String(255), default="PM2.5, PM10, NO2, SO2, CO, O3, NH3")
    verification_notes = Column(Text, nullable=True)

    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    provider = relationship("DataProvider", back_populates="stations")
    sensors = relationship("Sensor", back_populates="station")
    raw_observations = relationship("RawObservation", back_populates="station")
    validated_observations = relationship("ValidatedObservation", back_populates="station")
    aqi_records = relationship("StationAQIRecord", back_populates="station")

class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("monitoring_stations.id"), nullable=False)
    pollutant = Column(String(20), nullable=False) # "PM2.5", "PM10", "NO2", "SO2", "CO", "O3", "NH3"
    unit = Column(String(20), nullable=False) # "ug/m3", "mg/m3", "ppb"
    sensor_model = Column(String(100), nullable=True)
    sampling_interval = Column(String(30), default="1-hour")
    is_active = Column(Boolean, default=True)

    station = relationship("MonitoringStation", back_populates="sensors")

class RawObservation(Base):
    __tablename__ = "raw_observations"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("monitoring_stations.id"), nullable=False)
    pollutant = Column(String(20), nullable=False, index=True)
    raw_value = Column(Float, nullable=True)
    original_unit = Column(String(20), nullable=False)
    observation_timestamp = Column(DateTime, nullable=False, index=True)
    ingestion_timestamp = Column(DateTime, default=datetime.utcnow)
    provider_code = Column(String(50), nullable=False)
    raw_payload = Column(JSON, nullable=True)

    station = relationship("MonitoringStation", back_populates="raw_observations")
    validated = relationship("ValidatedObservation", back_populates="raw_observation", uselist=False)

class ValidatedObservation(Base):
    __tablename__ = "validated_observations"

    id = Column(Integer, primary_key=True, index=True)
    raw_id = Column(Integer, ForeignKey("raw_observations.id"), nullable=True)
    station_id = Column(Integer, ForeignKey("monitoring_stations.id"), nullable=False, index=True)
    pollutant = Column(String(20), nullable=False, index=True)
    normalized_value = Column(Float, nullable=False) # standardized to ug/m3 (or mg/m3 for CO)
    unit = Column(String(20), nullable=False)
    observation_timestamp = Column(DateTime, nullable=False, index=True)
    is_valid = Column(Boolean, default=True)
    
    # Milestone 2: Detailed Provenance & Classification
    data_classification = Column(String(30), default="DEMO", index=True) # VERIFIED, IMPORTED, DERIVED, DEMO, UNVERIFIED
    original_data_provider = Column(String(50), default="WBPCB")
    original_station_id = Column(String(50), default="")
    original_source_record = Column(Text, nullable=True) # URL or raw identifier
    provenance_hash = Column(String(64), nullable=True)
    
    # Milestone 2: Rich Quality Status
    quality_status = Column(String(50), default="VALID") # VALID, SUSPECT_OUTLIER, STALE, MISSING, SENSOR_FAULT, INVALID_UNIT, DUPLICATE, TIMESTAMP_ANOMALY
    z_score = Column(Float, nullable=True)
    flag_reason = Column(String(255), nullable=True)
    provenance = Column(String(100), default="Synthetic Demonstration Dataset (seed_data.py)")

    station = relationship("MonitoringStation", back_populates="validated_observations")
    raw_observation = relationship("RawObservation", back_populates="validated")

class StationAQIRecord(Base):
    __tablename__ = "station_aqi_records"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("monitoring_stations.id"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    aqi_value = Column(Integer, nullable=True) # 0 to 500+
    category = Column(String(50), nullable=True) # Good, Satisfactory, Moderate, Poor, Very Poor, Severe
    dominant_pollutant = Column(String(20), nullable=True)
    sub_indices = Column(JSON, nullable=True) # { "PM2.5": 142, "PM10": 110, "NO2": 45, ... }
    is_valid_cpcb = Column(Boolean, default=True) # Requires >=3 pollutants with >=1 PM2.5 or PM10
    methodology = Column(String(50), default="CPCB_2014_NAQI")
    data_classification = Column(String(30), default="DERIVED") # Sub-indices and AQI are derived

    station = relationship("MonitoringStation", back_populates="aqi_records")

class WeatherObservation(Base):
    __tablename__ = "weather_observations"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(50), nullable=False, index=True) # Kolkata or Howrah
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    observation_timestamp = Column(DateTime, nullable=False, index=True)
    temperature_c = Column(Float, nullable=True)
    relative_humidity_pct = Column(Float, nullable=True)
    wind_speed_kmh = Column(Float, nullable=True)
    wind_direction_deg = Column(Float, nullable=True)
    wind_direction_cardinal = Column(String(10), nullable=True)
    rainfall_mm = Column(Float, nullable=True)
    surface_pressure_hpa = Column(Float, nullable=True)
    boundary_layer_height_m = Column(Float, nullable=True)
    data_provider = Column(String(50), default="Open-Meteo High-Resolution Reanalysis")
    data_classification = Column(String(30), default="DEMO") # DEMO for seed, VERIFIED when fetched from live API

class AdministrativeBoundary(Base):
    __tablename__ = "administrative_boundaries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    boundary_type = Column(String(50), nullable=False) # "KMC_Borough", "KMC_Ward", "HMC_Ward", "District"
    code = Column(String(50), unique=True, nullable=False)
    centroid_lat = Column(Float, nullable=False)
    centroid_lng = Column(Float, nullable=False)
    geojson_polygon = Column(JSON, nullable=True)
    area_sqkm = Column(Float, nullable=True)
    population_est = Column(Integer, nullable=True)

class ResearchDocument(Base):
    __tablename__ = "research_documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    organisation = Column(String(150), nullable=False)
    publication_date = Column(String(50), nullable=False)
    geographic_coverage = Column(String(150), nullable=False)
    pollutants_studied = Column(String(150), nullable=False)
    methodology = Column(Text, nullable=False)
    key_findings = Column(Text, nullable=False)
    limitations = Column(Text, nullable=False)
    original_url = Column(String(500), nullable=True)
    study_type = Column(String(100), default="Source Apportionment")
    confidence_tier = Column(String(50), default="HIGH_PEER_REVIEWED")
    tags = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    notes = relationship("ResearchNote", back_populates="document")
    findings = relationship("ResearchFinding", back_populates="document")

class ResearchFinding(Base):
    __tablename__ = "research_findings"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("research_documents.id"), nullable=False)
    finding_type = Column(String(50), default="SOURCE_CONTRIBUTION") # SOURCE_CONTRIBUTION, METEOROLOGY, HEALTH, SPATIAL
    title = Column(String(200), nullable=False)
    statement = Column(Text, nullable=False)
    evidence_data = Column(JSON, nullable=True)
    confidence = Column(String(30), default="HIGH")
    
    # Milestone 2: Exact citation traceability
    citation_reference = Column(String(150), nullable=True) # e.g. "TERI (2025) Table 4.5, p. 84"
    page_number = Column(String(30), nullable=True)
    table_figure_ref = Column(String(50), nullable=True)
    has_supporting_reference = Column(Boolean, default=True)

    document = relationship("ResearchDocument", back_populates="findings")

class ResearchNote(Base):
    __tablename__ = "research_notes"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("research_documents.id"), nullable=True)
    station_id = Column(Integer, ForeignKey("monitoring_stations.id"), nullable=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("ResearchDocument", back_populates="notes")

class SourceCategory(Base):
    __tablename__ = "source_categories"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    sector = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    primary_pollutants = Column(String(100), nullable=False)
    typical_marker_species = Column(String(150), nullable=True)

    profiles = relationship("SourceContributionProfile", back_populates="category")

class SourceApportionmentStudy(Base):
    __tablename__ = "source_apportionment_studies"

    id = Column(Integer, primary_key=True, index=True)
    study_name = Column(String(200), nullable=False)
    organisation = Column(String(150), nullable=False)
    publication_year = Column(Integer, nullable=False)
    methodology = Column(String(100), nullable=False)
    geographic_scope = Column(String(150), nullable=False)
    study_period = Column(String(100), nullable=False)
    documentation_url = Column(String(500), nullable=True)
    limitations = Column(Text, nullable=True)
    confidence_tier = Column(String(50), default="Statutory / CPCB Recognized")

    profiles = relationship("SourceContributionProfile", back_populates="study")

class SourceContributionProfile(Base):
    __tablename__ = "source_contribution_profiles"

    id = Column(Integer, primary_key=True, index=True)
    study_id = Column(Integer, ForeignKey("source_apportionment_studies.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("source_categories.id"), nullable=False)
    pollutant = Column(String(20), nullable=False) # "PM2.5", "PM10"
    season = Column(String(30), nullable=False) # "Winter", "Summer", "Monsoon", "Annual"
    city = Column(String(50), default="Kolkata") # "Kolkata" or "Howrah"
    contribution_percentage = Column(Float, nullable=False)
    concentration_ugm3 = Column(Float, nullable=True)
    uncertainty_min = Column(Float, nullable=True)
    uncertainty_max = Column(Float, nullable=True)
    evidence_type = Column(String(50), default="PUBLISHED_SOURCE_APPORTIONMENT")
    
    # Milestone 2: Citation traceability
    citation_reference = Column(String(150), nullable=True) # e.g. "TERI (2025) Table 4.2, p. 78"
    page_number = Column(String(30), nullable=True)
    table_figure_ref = Column(String(50), nullable=True)
    has_supporting_reference = Column(Boolean, default=True)

    study = relationship("SourceApportionmentStudy", back_populates="profiles")
    category = relationship("SourceCategory", back_populates="profiles")

class InterventionHypothesis(Base):
    __tablename__ = "intervention_hypotheses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    problem_statement = Column(Text, nullable=False)
    target_area = Column(String(150), nullable=False)
    target_pollutant = Column(String(50), default="PM2.5 & PM10")
    suspected_source = Column(String(150), nullable=False)
    supporting_evidence = Column(Text, nullable=False)
    proposed_intervention = Column(Text, nullable=False)
    mechanism_of_action = Column(Text, nullable=False)
    required_resources = Column(Text, nullable=False)
    possible_implementation_partner = Column(String(200), nullable=False)
    measurable_indicators = Column(Text, nullable=False)
    risks_limitations = Column(Text, nullable=False)
    research_confidence = Column(String(30), default="MEDIUM")
    validation_requirements = Column(Text, nullable=False)
    
    feasibility_score = Column(Float, default=7.0)
    potential_reduction_score = Column(Float, default=8.0)
    cost_complexity_score = Column(Float, default=6.0)
    ease_of_verification_score = Column(Float, default=7.5)
    scalability_score = Column(Float, default=8.0)
    
    evaluation_framework = Column(JSON, nullable=True)
    status = Column(String(50), default="DRAFT_HYPOTHESIS")
    data_classification = Column(String(30), default="RESEARCH_HYPOTHESIS")
    created_at = Column(DateTime, default=datetime.utcnow)

class IngestionLog(Base):
    __tablename__ = "ingestion_logs"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("data_providers.id"), nullable=True)
    source_name = Column(String(100), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(30), default="PENDING") # SUCCESS, WARNING, FAILED
    records_processed = Column(Integer, default=0)
    records_flagged = Column(Integer, default=0)
    data_classification = Column(String(30), default="DEMO") # DEMO, IMPORTED, VERIFIED
    message = Column(Text, nullable=True)

    provider_rel = relationship("DataProvider", back_populates="ingestion_logs")
