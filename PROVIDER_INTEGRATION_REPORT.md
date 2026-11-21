# PRANA Research Hub: Provider Integration & Automated Data Collection Report
## Milestone 3: Automated Data Collection & Environmental Analysis

This report documents the architectural implementation, external interface audits, authentication mechanisms, data transformation pipelines, and scientific constraints for all external environmental and meteorological data providers serving the **Kolkata–Howrah airshed**.

---

### Executive Summary

| Provider | Integration Type | Authentication | Real-Time Telemetry Status | Supported Data Formats | Classification Tier |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **OpenAQ v3** | REST API v3 | `X-API-Key` (Header) | **CONNECTED** (17 locations discovered; 36 live records ingested) | JSON (`/locations`, `/sensors`, `/latest`, `/hours`) | `VERIFIED` |
| **Open-Meteo** | Numerical Reanalysis API | Public Open Access | **CONNECTED** (399 hourly records synchronized) | JSON (Hourly Reanalysis & Forecast) | `MODELLED` (Atmospheric Dynamics) |
| **WBPCB** | Researcher-Assisted CSV | N/A (Manual Portal Extract) | **MANUAL_PORTAL_ONLY** (No public unauthenticated REST API) | CSV (Wide & Long Format) | `IMPORTED` |
| **CPCB / CCR** | Data.gov.in API & CCR CSV | `DATAGOV_API_KEY` or Manual CCR | **AUTH_REQUIRED** (API key optional; CCR CSV active) | JSON & Official CCR CSV | `IMPORTED` (Pollutant) & `DERIVED` (AQI) |

---

### 1. OpenAQ API v3 Integration

#### 1.1 Interface Architecture & Authentication
- **Base Endpoint**: `https://api.openaq.org/v3`
- **Authentication**: Secured via `X-API-Key` header loaded from `.env` (`OPENAQ_API_KEY`).
- **Client Implementation**: [backend/services/ingestion/openaq_adapter.py](file:///D:/project-prana/backend/services/ingestion/openaq_adapter.py).

#### 1.2 Location Discovery & Parameter Mapping
- **Spatial Scope**: Discovers monitoring locations using the Kolkata–Howrah conurbation bounding box:
  $$\text{bbox} = 88.15^\circ\text{E}, 22.40^\circ\text{N}, 88.55^\circ\text{E}, 22.70^\circ\text{N}$$
- Discovered 17 monitoring stations, including:
  - Location #910: `Victoria Memorial - WBSPCB` (Coordinates: 22.5726°N, 88.3639°E; 6 sensors)
  - Location #716: `Rabindra Bharati University - WBSPCB` (Coordinates: 22.6279°N, 88.3804°E; 6 sensors)
  - Location #5614: `Padmapukur, Howrah - WBPCB` (Coordinates: 22.5687°N, 88.2797°E; 18 sensors)
  - Location #2460: `US Diplomatic Post: Kolkata` (Coordinates: 22.5471°N, 88.3510°E; 1 sensor)
- **Sensor Discovery**: Dynamically resolves sensor IDs per location (`/v3/locations/{id}/sensors`).
- **Telemetry Ingestion**: Ingests latest observations (`/v3/locations/{id}/latest`) and historical hourly series (`/v3/sensors/{id}/hours`).

#### 1.3 Timezone & Unit Normalization
- **Timezone Conversion**: OpenAQ provides ISO timestamps with UTC and local offsets (`+05:30` Asia/Kolkata). Observations are stored in UTC in the SQLite/PostgreSQL database and rendered in `Asia/Kolkata` for researchers.
- **Unit Normalization**: Gaseous concentrations reported in $\text{ppb}$ or $\text{ppm}$ are converted using ambient standard temperature and pressure ($25^\circ\text{C}, 1\text{ atm}$):
  - $\text{NO}_2: 1\text{ ppb} \times 1.88 = \mu\text{g/m}^3$
  - $\text{SO}_2: 1\text{ ppb} \times 2.62 = \mu\text{g/m}^3$
  - $\text{CO}: 1\text{ ppm} \times 1.145 = \text{mg/m}^3$
  - $\text{PM}_{2.5}$ and $\text{PM}_{10}$ are stored directly in $\mu\text{g/m}^3$.
- **Duplicate Protection**: Unique key constraint on `(station_id, pollutant, observation_timestamp)` prevents duplicate ingestion.
- **Provenance Fingerprint**: Every record is tagged with `data_classification = 'VERIFIED'` and a SHA-256 cryptographic provenance hash.

---

### 2. West Bengal Pollution Control Board (WBPCB) Integration

#### 2.1 Investigation of `https://aqmsdata.wbpcb.gov.in/`
- **Technical Reality**: The official WBPCB Continuous Ambient Air Quality portal is a client-rendered application that does not expose an open, unauthenticated REST API. Automated web scraping of gated state infrastructure is prohibited.
- **Adapter Behavior**: [backend/services/ingestion/wbpcb_adapter.py](file:///D:/project-prana/backend/services/ingestion/wbpcb_adapter.py) transparently reports WBPCB's connection status as `MANUAL_PORTAL_ONLY` and records the institutional limitation.
- **Researcher-Assisted CSV Workflow**:
  - Implemented multi-format CSV parsing for official WBPCB portal data downloads:
    - **Wide Format**: Detects and extracts tabular matrices (`Date`, `Time`, `Station`, `PM2.5`, `PM10`, `NO2`, `SO2`, `CO`, `O3`).
    - **Long Format**: Parses normalized records (`station_code`, `pollutant`, `value`, `unit`, `timestamp`).
  - Automatically matches stations by station code or official name substrings.
  - Generates SHA-256 provenance receipts upon upload.

---

### 3. Central Pollution Control Board (CPCB) Integration

#### 3.1 Investigation of `app.cpcbccr.com` & `data.gov.in`
- **Technical Reality**: CPCB's continuous monitoring portal (`app.cpcbccr.com/ccr_docs`) is session-gated. The national Open Government Data platform (`api.data.gov.in`) exposes the real-time resource `3b01bcb8-0b14-4abf-b6f2-c1bfd384ba69`, but requires an approved institutional `DATAGOV_API_KEY`.
- **Adapter Implementation**: [backend/services/ingestion/cpcb_adapter.py](file:///D:/project-prana/backend/services/ingestion/cpcb_adapter.py) supports automated polling when `DATAGOV_API_KEY` is supplied, and falls back gracefully to `AUTH_REQUIRED` with zero crashes or false live claims.
- **Critical Scientific Separation Rule**:
  - **Individual Pollutant Concentrations**: Stored in `ValidatedObservation` ($\mu\text{g/m}^3$ / $\text{mg/m}^3$) with `data_classification = 'IMPORTED'`.
  - **Official CPCB NAQI Values**: Stored in `StationAQIRecord` (`aqi_value`, `category`, `dominant_pollutant`, `sub_indices`) with `data_classification = 'DERIVED'` and `methodology = 'CPCB_OFFICIAL_CCR_REPORT'`.
  - Official composite AQI numbers are **never** stored in or combined with continuous mass concentration fields.

---

### 4. Open-Meteo High-Resolution Weather Integration

#### 4.1 Atmospheric Reanalysis Pipeline
- **Base Endpoints**:
  - Archive Reanalysis: `https://archive-api.open-meteo.com/v1/archive`
  - Current/Forecast Reanalysis: `https://api.open-meteo.com/v1/forecast`
- **Representative Airshed Coordinates**:
  - Kolkata Urban Core: $22.5726^\circ\text{N}, 88.3639^\circ\text{E}$
  - Howrah Industrial Core: $22.5958^\circ\text{N}, 88.2636^\circ\text{E}$
- **Synchronized Hourly Variables**:
  - Temperature at 2m ($^\circ\text{C}$)
  - Relative Humidity at 2m ($\%$)
  - Wind Speed at 10m ($\text{km/h}$)
  - Wind Direction at 10m (0–360° and 16-point cardinal compass: N, NNE, NE, etc.)
  - Precipitation ($\text{mm}$)
  - Surface Pressure ($\text{hPa}$)
  - Planetary Boundary Layer Height ($\text{m}$)
- **Classification Mandate**: All weather records are explicitly tagged as:
  $$\text{data\_classification} = \text{'MODELLED'}$$
  The platform explicitly notifies researchers that these values originate from numerical atmospheric reanalysis models, not local ground weather stations.

---

### 5. Automated Ingestion Engine Architecture

- **Orchestrator**: [backend/services/ingestion/ingestion_manager.py](file:///D:/project-prana/backend/services/ingestion/ingestion_manager.py).
- **Failure Containment (Isolation)**: Each provider runs inside an isolated execution block. An authentication or network failure in OpenAQ or CPCB **never** halts or blocks Open-Meteo weather synchronization.
- **Exponential Backoff**: Transient errors (HTTP 429, socket timeouts) trigger automated retries ($2.0\text{s}, 4.0\text{s}, 8.0\text{s}$) with jitter.
- **Incremental Sync**: The engine compares incoming timestamps against `MonitoringStation.last_observed_at` to avoid re-fetching historical blocks unnecessarily.
- **Zero Simulation Rule**: When an API fails, the platform records the error in `IngestionLog` and `DataProvider.last_error_message`, and **never** silently swaps in synthetic demo data.

---

### 6. Environmental Analysis Workspace (Reproducibility)

- **Engine**: [backend/services/environmental_analysis_engine.py](file:///D:/project-prana/backend/services/environmental_analysis_engine.py).
- **Workspace UI**: [AnalysisWorkspaceView.tsx](file:///D:/project-prana/frontend/src/components/views/AnalysisWorkspaceView.tsx).
- **Capabilities**:
  1. *Temporal Multi-Station Analysis*: 24-hour diurnal cycle envelopes (mean, median, 10th and 90th percentiles), daily averages, NAAQS exceedance rates, and weekday-to-weekend emission ratios.
  2. *Meteorological Dispersion Analytics*: Bivariate Pearson correlations and OLS linear regression slopes for wind speed, temperature, humidity, rainfall, and boundary layer height.
  3. *Directional Pollution Rose*: 16-sector wind direction distribution isolating upwind industrial plume directions.
  4. *Unmonitored Industrial Void Boundaries*: Explicitly records the 4 major unmonitored zones (Jalan Industrial Complex, Domjur foundry belt, Uluberia casting hub, Khidirpur Port) with high-uncertainty warnings.
  5. *Reproducible Persistence & Export*: Saved analyses store parameter configs, methodology, and citations in `saved_analyses`, and provide one-click CSV export of the underlying dataset.
