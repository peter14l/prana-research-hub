# PRANA Research Hub: Kolkata–Howrah Environmental Intelligence
## Milestone 3: Automated Data Collection & Environmental Analysis

**PRANA Research Hub** is a research-grade environmental intelligence and geospatial analysis platform engineered for **PRANA**, an early-stage clean-air technology initiative investigating outdoor air pollution across the **Kolkata–Howrah metropolitan airshed of West Bengal, India**.

The platform is designed to identify scientifically defensible, measurable pollution-reduction opportunities for PRANA's initial engineering pilot projects.

---

## What's New in Milestone 3

Milestone 3 transforms PRANA into an **automatically updated environmental research platform** with direct external data provider adapters, automated scheduled & manual sync, scientific meteorological correlation, and a dedicated **Analysis Workspace**:

1. **OpenAQ API v3 Live Ingestion**:
   - Authenticated integration using `OPENAQ_API_KEY`.
   - Dynamic location and sensor discovery within the Kolkata–Howrah bounding box (`88.15,22.40,88.55,22.70`).
   - Hourly and latest measurement retrieval with automatic unit standardization (e.g. converting NO₂ ppb to $\mu\text{g/m}^3$ $\times 1.88$) and timezone normalization (UTC naive DB storage with `Asia/Kolkata` `+05:30` offsets).
   - Zero-duplicate protection and cryptographic SHA-256 fingerprinting. All ingested ground records tagged as `VERIFIED`.

2. **WBPCB & CPCB Institutional Ingestion Adapters**:
   - **WBPCB**: Documents lack of an unauthenticated public REST API; provides a researcher-assisted CSV import workflow for official portal exports (`https://aqmsdata.wbpcb.gov.in/`).
   - **CPCB / Data.gov.in**: Connects to Data.gov.in real-time API via `DATAGOV_API_KEY` and supports official CPCB Central Control Room (CCR) multi-station CSV exports.
   - **Strict AQI Separation**: In accordance with scientific protocols, composite official AQI values are strictly routed to `StationAQIRecord` tables, completely segregated from physical mass concentrations in `ValidatedObservation`.

3. **Open-Meteo Synoptic Atmospheric Integration**:
   - Automated ingestion of hourly meteorological variables for Kolkata and Howrah coordinates: Temperature, Relative Humidity, Wind Speed, Wind Direction (with 16-point cardinal compass), Precipitation, Surface Pressure, and Planetary Boundary Layer Height (PBLH).
   - **Strict Scientific Labeling**: All synoptic weather records are explicitly tagged as `MODELLED` reanalysis data, clearly distinguished from local ground-level air quality observations.

4. **Modular Ingestion Framework**:
   - Provider failure isolation: an outage or rate-limit on one provider never halts other adapters.
   - Exponential backoff with random jitter retry policy.
   - Incremental sync tracking via `last_synced_at` timestamps.
   - Webhook / UI manual refresh trigger via `/api/ingestion/refresh`.

5. **Environmental Analysis Engine**:
   - **Temporal Diurnal Cycles**: 24-hour diurnal profiles computed with mean, median, 10th percentile, and 90th percentile envelopes.
   - **NAAQS Statutory Exceedance Tracking**: Exceedance rates calculated against Indian CPCB 24-hour statutory standards ($60\,\mu\text{g/m}^3$ for $\text{PM}_{2.5}$, $100\,\mu\text{g/m}^3$ for $\text{PM}_{10}$, $80\,\mu\text{g/m}^3$ for $\text{NO}_2$, $80\,\mu\text{g/m}^3$ for $\text{SO}_2$, $2\,\text{mg/m}^3$ for $\text{CO}$, $100\,\mu\text{g/m}^3$ for $\text{O}_3$).
   - **Weekday vs. Weekend Ratios**: Traffic and industrial signature analysis.
   - **Meteorological Dispersion Regressions**: Ordinary Least Squares (OLS) regression slopes, Pearson correlation coefficients ($r$), and two-tailed $p$-values.
   - **16-Sector Pollution Rose**: Directional pollution frequency and intensity distributions.
   - **Hotspot Rankings & Spatial Void Disclosures**: Ranks monitored locations while enforcing strict non-extrapolation warnings for unmonitored industrial corridors (Jalan Complex, Domjur, Uluberia, Khidirpur Docklands, Budge Budge).

6. **Dedicated Analysis Workspace**:
   - Interactive researcher workbench accessible from the primary navigation sidebar.
   - Multi-parameter and multi-station filtering with provenance tier toggles (`VERIFIED`, `IMPORTED`).
   - Interactive charts: Diurnal curves with confidence bands, daily exceedance bars, bivariate scatter plots with regression trendlines, and 16-sector pollution roses.
   - Save analysis sessions with researcher notes, methodology, and citations to SQLite.
   - Export analysis datasets as CSV directly from the UI.

---

## 11 Core Application Modules

| Module | Purpose & Capabilities | Milestone 3 Enhancements |
| :--- | :--- | :--- |
| **1. Overview** | Regional air quality summary, 6 pollutant NAAQS cards, MapLibre telemetry map, 7-day trend envelope. | Live provider connection pills (OpenAQ, Open-Meteo, WBPCB, CPCB), total active sensors count (54 sensors), and statutory ground vs. modelled weather notice banner. |
| **2. Live Air Quality** | CAAQM station list, CPCB NAQI calculation with sub-indices, 48-hour history, raw vs. validated data inspection, CSV export. | Live observation updates from OpenAQ v3 with original station identifiers. |
| **3. Pollution Explorer** | Diurnal hourly profiles (24h), Day-of-week patterns, bivariate correlation with Pearson/Spearman and non-causal caveat, multi-station comparison. | Direct connection to the real-time Environmental Analysis Engine. |
| **4. Geographic Hotspots** | 9 evaluated zones across Kolkata and Howrah, distance to nearest station, uncertainty classification, explicit coverage gap warnings. | Spatial coverage void alerts for unmonitored foundry and port industrial belts. |
| **5. Source Intelligence** | Published source apportionment (TERI 2025, NEERI 2020), winter/summer sector shares, chemical marker directory, evidence labels. | Verifiable research findings with exact publication citations, page numbers, and table references. |
| **6. Weather & Atmosphere** | Hourly temperature, relative humidity, wind speed, wind direction, Planetary Boundary Layer Height (PBLH), 16-sector wind rose. | Synoptic reanalysis telemetry from Open-Meteo High-Resolution models classified as `MODELLED`. |
| **7. Research Library** | Searchable repository of foundational papers (WBPCB, TERI, CPCB, NEERI) with metadata, methodology, findings, and user annotations. | Full methodological metadata and limitation disclosures for every paper. |
| **8. Intervention Lab** | Candidate engineering hypotheses, multi-criteria quantitative scoring (feasibility, reduction, verification), counterfactual verification design. | Counterfactual evaluation frameworks with control stations and de-weathering requirements. |
| **9. Data Sources & Quality** | Ingestion audit logs, 3-sigma outlier inspector, completeness rate, manual CSV dataset import with schema validation. | Live "Trigger Ingestion Refresh" button, multi-format CSV import selector (PRANA Standard, CPCB CCR, WBPCB Portal), and live status telemetry. |
| **10. Analysis Workspace** *(New)* | Multi-station researcher workbench for custom diurnal, scatter, daily, and pollution rose investigations. | Save named research configurations, persistent SQLite storage, and direct CSV dataset download. |
| **11. Settings** | Air shed geographic bounding box, CPCB NAQI configuration, database and API status. | Live status of internal SQLite engine, external API credentials, and boundary configs. |

---

## Technology Stack

### Frontend
- **Framework**: Next.js 15 (App Router) with React 19 & TypeScript
- **Styling**: Tailwind CSS (Dark research workstation palette: `#0C0F14`, `#FFE547`, `#8A9A8F`)
- **Visualizations**: Recharts (diurnal cycles with p10–p90 envelopes, day-of-week, bivariate scatter with regression trendlines, 16-sector directional roses)
- **Geospatial Mapping**: MapLibre GL JS with Carto Dark Matter raster tiles (zero API key required)
- **Icons**: Lucide React

### Backend
- **Framework**: Python 3.12 FastAPI
- **Database**: Zero-setup embedded SQLite (`backend/data/prana.db`), 100% schema-compatible with PostgreSQL/PostGIS
- **Adapters**: OpenAQ v3 REST client, Open-Meteo Archive/Forecast client, CPCB CCR parser, WBPCB portal parser
- **ORM & Validation**: SQLAlchemy 2.0 & Pydantic
- **Scientific Computing**: Pandas, NumPy, SciPy, Scikit-learn, Shapely
- **Security & Integrity**: SHA-256 cryptographic provenance hashing for dataset ingestion

---

## Quickstart Guide

### 1. Prerequisites
- **Python**: 3.10+ (Python 3.12 recommended)
- **Node.js**: v18+ (Node v22 / v26 supported)
- **Package Manager**: pnpm, npm, or yarn

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
OPENAQ_API_KEY="your-openaq-api-key"
DATAGOV_API_KEY="your-datagov-in-key"  # Optional
```

### 3. Backend Setup & Startup

From the project root:

```powershell
# Navigate to project root
cd D:\project-prana

# Execute Milestone 3 schema migrations
python backend/migrate_milestone3.py

# Optional: Trigger an immediate live ingestion sync from OpenAQ and Open-Meteo
python -c "from backend.database import SessionLocal; from backend.services.ingestion.ingestion_manager import IngestionManager; db = SessionLocal(); res = IngestionManager(db).run_all_ingestions(); print(res); db.close()"

# Start FastAPI backend server (Runs on port 8000)
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

The API will be available at:
- Interactive Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### 4. Frontend Setup & Startup

In a separate terminal:

```powershell
# Navigate to frontend directory
cd D:\project-prana\frontend

# Install dependencies (if not already installed)
npm install

# Start Next.js development server (Runs on port 3000)
npx next dev -p 3000
```

Open your browser at:
`http://localhost:3000`

---

## Automated Verification Suite

Run the full end-to-end Python test suites:

```powershell
# Run all automated tests (Milestone 1 + Milestone 2 + Milestone 3)
python -m unittest discover tests

# Or run Milestone 3 specific verification suite:
python -m unittest tests/test_milestone3.py
```

The automated suite executes **26 integration tests** verifying:
1. **OpenAQ v3 Ingestion**: Location discovery, coordinate bbox filtering, parameter standardization, timezone normalization, and duplicate prevention.
2. **Open-Meteo Weather Ingestion**: Reanalysis synoptic weather ingestion and strict `MODELLED` classification enforcement.
3. **WBPCB & CPCB Adapters**: Parser resilience, format identification, and strict separation of official AQI from raw concentrations.
4. **Resilience & Fault Isolation**: Exponential backoff, jitter calculation, 401 unauthenticated handling, and provider outage isolation.
5. **Environmental Analysis Engine**: Diurnal hourly aggregations, NAAQS statutory exceedance calculation, OLS meteorological regressions, and unmonitored coverage void boundaries.
6. **Analysis Workspace Persistence**: Storing analysis configurations and generating tabular CSV dataset downloads.

---

## Scientific Documentation & Reports

- [PROVIDER_INTEGRATION_REPORT.md](file:///D:/project-prana/PROVIDER_INTEGRATION_REPORT.md): Comprehensive architectural analysis of external providers, endpoints, authentication barriers, data schemas, and reliability matrix.
- [LIMITATIONS.md](file:///D:/project-prana/LIMITATIONS.md): Scientific protocols, non-attribution boundaries of ambient sensor data, modelled weather caveats, and counterfactual intervention guidelines.
- [DATA_INTEGRITY_AUDIT.md](file:///D:/project-prana/DATA_INTEGRITY_AUDIT.md): Forensic audit analyzing seeded observations, data classifications, completeness formulas, and provider connectivity.
- [STATION_VERIFICATION_REPORT.md](file:///D:/project-prana/STATION_VERIFICATION_REPORT.md): Dossier for all statutory CAAQM stations with CPCB Site IDs, coordinates, verified parameters, and spatial coverage voids.
- [UNRESOLVED_ISSUES.md](file:///D:/project-prana/UNRESOLVED_ISSUES.md): Institutional API boundaries, WBPCB portal workflow, speciation limitations, and PostGIS scaling roadmap.
