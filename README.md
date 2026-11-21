# PRANA Research Hub: Kolkata–Howrah Environmental Intelligence
## Milestone 2: Data Integrity, Provenance & Scientific Verification

**PRANA Research Hub** is a research-grade environmental intelligence and geospatial analysis platform engineered for **PRANA**, an early-stage clean-air technology initiative investigating outdoor air pollution across the **Kolkata–Howrah metropolitan airshed of West Bengal, India**.

The platform is designed to identify scientifically defensible, measurable pollution-reduction opportunities for PRANA's initial engineering pilot projects.

---

## Scientific Integrity Standards (Milestone 2)

Following the Milestone 2 scientific verification audit, every measurement, station dossier, and research claim adheres to strict provenance standards:

1. **Five-Tier Data Provenance System**:
   - `VERIFIED`: Authenticated statutory data traceable to an official portal extract or signed source.
   - `IMPORTED`: Field observations or historical datasets uploaded by researchers.
   - `DERIVED`: Numerically calculated analytics (e.g., CPCB NAQI sub-indices, rolling averages).
   - `DEMO`: Demonstration or synthetic baseline models (clearly identified; never disguised as live data).
   - `UNVERIFIED`: Data whose precise institutional origin cannot currently be established.
2. **Station Verification Dossier**:
   - All 9 statutory Continuous Ambient Air Quality Monitoring (CAAQM) stations in Kolkata and Howrah are cross-referenced with Central Pollution Control Board (CPCB) Site IDs (`site_5002` through `site_5010`).
   - Unmonitored industrial corridors (Jalan, Domjur, Uluberia, Budge Budge) are explicitly documented rather than filled with speculative interpolation heatmaps.
3. **Statutory Completeness Calculation**:
   - Completeness is calculated strictly as:
     $$\text{Completeness (\%)} = \left(\frac{\text{Received Valid Observations}}{\text{Expected Hours} \times \text{Tracked Pollutants}}\right) \times 100$$
   - Every completeness figure displays its exact numerator and denominator (e.g., `10,521 / 10,584 records (99.4%)`).
4. **Zero Silent Deletion Policy**:
   - 3-sigma statistical outliers and physical threshold flags are retained in an inspection queue for scientific review, never deleted silently.
5. **Traceable Research Claims**:
   - Source apportionment contributions link directly to official publications: **TERI (2025)** (Tables 4.5 & 4.6, pp. 84–92) and **CSIR-NEERI (2020)** (Table 5.2, p. 112). Findings lacking supporting references trigger explicit visual warnings.

---

## 10 Core Application Modules

| Module | Purpose & Capabilities | Milestone 2 Provenance Features |
| :--- | :--- | :--- |
| **1. Overview** | Regional air quality summary, 6 pollutant NAAQS cards, MapLibre telemetry map, 7-day trend envelope, evidence-backed highlights. | Global Data Integrity indicator pill displaying verified vs. demo dataset distribution. |
| **2. Live Air Quality** | CAAQM station list, CPCB NAQI calculation with sub-indices, 48-hour history, raw vs. validated data inspection, CSV export. | Statutory CPCB Site ID tagging, station verification status, data classification pill per station. |
| **3. Pollution Explorer** | Diurnal hourly profiles (24h), Day-of-week patterns, bivariate correlation with Pearson/Spearman and non-causal caveat, multi-station comparison. | Transparent flagging of synthetic baseline diurnal models. |
| **4. Geographic Hotspots** | 9 evaluated zones across Kolkata and Howrah, distance to nearest station, uncertainty classification, explicit coverage gap warnings. | Spatial coverage void alerts for unmonitored foundry and port industrial belts. |
| **5. Source Intelligence** | Published source apportionment (TERI 2025, NEERI 2020), winter/summer sector shares, chemical marker directory, evidence labels. | Verifiable research findings with exact publication citations, page numbers, and table references. |
| **6. Weather & Atmosphere** | Hourly temperature, relative humidity, wind speed, wind direction, Planetary Boundary Layer Height (PBLH), 16-sector wind rose. | Synoptic reanalysis telemetry from Open-Meteo High-Resolution models. |
| **7. Research Library** | Searchable repository of foundational papers (WBPCB, TERI, CPCB, NEERI) with metadata, methodology, findings, and user annotations. | Full methodological metadata and limitation disclosures for every paper. |
| **8. Intervention Lab** | Candidate engineering hypotheses, multi-criteria quantitative scoring (feasibility, reduction, verification), counterfactual verification design. | Counterfactual evaluation frameworks with control stations and de-weathering requirements. |
| **9. Data Sources & Quality** | Ingestion audit logs, 3-sigma outlier inspector, completeness rate, manual CSV dataset import with schema validation. | 4 Dedicated Tabs: Integrity & Completeness Audit, Station Verification Dossier, Provider Reliability, Cryptographic CSV Ingestion. |
| **10. Settings** | Air shed geographic bounding box, CPCB NAQI configuration, database and API status. | Live status of internal SQLite engine, external API credentials, and boundary configs. |

---

## Technology Stack

### Frontend
- **Framework**: Next.js 15 (App Router) with React 19 & TypeScript
- **Styling**: Tailwind CSS (Dark research workstation palette: `#0C0F14`, `#FFE547`, `#8A9A8F`)
- **Visualizations**: Recharts (diurnal cycles, day-of-week, bivariate scatter, multi-station time series)
- **Geospatial Mapping**: MapLibre GL JS with Carto Dark Matter raster tiles (zero API key required)
- **Icons**: Lucide React

### Backend
- **Framework**: Python 3.12 FastAPI
- **Database**: Zero-setup embedded SQLite (`backend/data/prana.db`), 100% schema-compatible with PostgreSQL/PostGIS
- **ORM & Validation**: SQLAlchemy 2.0 & Pydantic
- **Scientific Computing**: Pandas, NumPy, SciPy, Scikit-learn, Shapely
- **Security & Integrity**: SHA-256 cryptographic provenance hashing for dataset ingestion

---

## Quickstart Guide

### 1. Prerequisites
- **Python**: 3.10+ (Python 3.12 recommended)
- **Node.js**: v18+ (Node v22 / v26 supported)
- **Package Manager**: pnpm, npm, or yarn

### 2. Backend Setup & Startup

From the project root:

```powershell
# Navigate to project root
cd D:\project-prana

# Execute database migrations (Milestone 2 Schema)
python backend/migrate_milestone2.py

# Start FastAPI backend server (Runs on port 8000)
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

The API will be available at:
- Interactive Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### 3. Frontend Setup & Startup

In a separate terminal:

```powershell
# Navigate to frontend directory
cd D:\project-prana\frontend

# Start Next.js development server (Runs on port 3000)
npx next dev -p 3000
```

Open your browser at:
`http://localhost:3000`

---

## Automated Verification Suite

Run the full end-to-end Python test suites:

```powershell
# Run all automated tests (Milestone 1 + Milestone 2)
python -m unittest discover tests

# Or run Milestone 2 specific verification suite:
python -m unittest tests/test_milestone2.py
```

Tests verify:
1. **Provenance Assignment**: SHA-256 cryptographic fingerprinting, provider tagging, and original source recording.
2. **Data Classification**: Complete representation across `VERIFIED`, `IMPORTED`, `DERIVED`, `DEMO`, and `UNVERIFIED`.
3. **Duplicate Detection**: Zero-collision identification of duplicate timestamps per station/pollutant.
4. **Missing Observation Detection**: Identification of hourly temporal sequence gaps.
5. **Completeness Formula**: Validation of the explicit numerator/denominator ratio.
6. **Station Verification Dossier**: Statutory verification of all 9 CAAQM stations with CPCB Site IDs.
7. **Stale Data Detection**: Dynamic flagging of sensors with no telemetry in >24 hours.
8. **Research Citation Traceability**: Exact publication, page, and table cross-referencing.

---

## Audit Reports & Documentation

- [DATA_INTEGRITY_AUDIT.md](file:///D:/project-prana/DATA_INTEGRITY_AUDIT.md): Forensic audit analyzing seeded observations, data classifications, completeness formulas, and provider connectivity.
- [STATION_VERIFICATION_REPORT.md](file:///D:/project-prana/STATION_VERIFICATION_REPORT.md): Dossier for all 9 statutory CAAQM stations with CPCB Site IDs, coordinates, verified parameters, and spatial coverage voids.
- [UNRESOLVED_ISSUES.md](file:///D:/project-prana/UNRESOLVED_ISSUES.md): Institutional API boundaries (OpenAQ auth, WBPCB manual portals), speciation limitations, and PostGIS scaling roadmap.
- [LIMITATIONS.md](file:///D:/project-prana/LIMITATIONS.md): Scientific protocols, non-attribution boundaries of ambient sensor data, and counterfactual intervention guidelines.
