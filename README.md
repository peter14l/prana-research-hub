# PRANA Research Hub: Kolkata–Howrah Environmental Intelligence
## Milestone 4: Pollution Opportunity Discovery & Engineering Prioritisation

**PRANA Research Hub** is a research-grade environmental intelligence, geospatial analysis, and engineering opportunity discovery platform engineered for **PRANA**, an early-stage clean-air technology initiative investigating outdoor air pollution across the **Kolkata–Howrah metropolitan airshed of West Bengal, India**.

The platform is designed to identify scientifically defensible, measurable pollution-reduction opportunities for PRANA's initial engineering pilot projects.

---

## What's New in Milestone 4: Opportunity Discovery & Prioritisation

Milestone 4 establishes an **evidence-driven opportunity discovery and engineering prioritisation system** that identifies, scores, and governs candidate hardware and monitoring interventions grounded strictly in Kolkata–Howrah data:

1. **Evidence Inventory & Sectoral Evaluations**:
   - Comprehensive forensic cataloging of over **10,900 observations**, 9 statutory CAAQM stations (`site_5002`–`site_5010`), Open-Meteo atmospheric reanalysis, and peer-reviewed literature (TERI 2025, CSIR-NEERI 2020).
   - Independent empirical evaluations for **all 8 pollution sectors**: Industrial emissions, Road transport, Waste burning, River transport, Construction dust, Domestic combustion, Regional transport, and Other documented sources.

2. **Multi-Criteria Opportunity Evaluation Engine**:
   - Scores candidate projects across **8 transparent criteria**:
     - *Pollution Impact* (0.20)
     - *Evidence Strength* (0.15)
     - *Technical Feasibility* (0.15)
     - *Financial Feasibility* (0.10)
     - *Verification Credibility* (0.15)
     - *Scalability* (0.10)
     - *Innovation & IP* (0.05)
     - *Partnership Feasibility* (0.10)
   - Dynamic weight adjustment sliders with real-time score recalculation and ranking.
   - **Statutory Non-Measurement Disclosure**: Explicitly discloses that composite priority scores are structured prioritization heuristics, not empirical physical air quality measurements.

3. **Grounded Candidate Engineering Dossiers (4 Evaluated Projects)**:
   - Formulates 4 detailed engineering candidate dossiers featuring all **14 mandatory technical fields**:
     1. **Howrah Foundry Cupola Multi-Cyclone & Dry Sorbent Off-Gas Scrubbing Retrofit** (`howrah-foundry-cupola-retrofit`) — Direct source control targeting the single largest local stationary particulate driver (34% winter $\text{PM}_{2.5}$ in Ghusuri per NEERI 2020).
     2. **Optical & Thermal Fence-Line Micro-Plume Attribution Network** (`industrial-fence-line-attribution`) — Low-cost sensing and edge triangulation network resolving the 7 km monitoring void over the Jalan Industrial Complex (2,000+ units).
     3. **Autonomous Thermal Edge-Detection & Rapid-Suppression for Landfill Refuse Fires** (`landfill-fire-thermal-suppression`) — Subterranean pneumatic foam suppression addressing 14% of winter $\text{PM}_{2.5}$ and episodic toxic plumes at Dhapa Dump.
     4. **Hooghly River Passenger Ferry Exhaust Aftertreatment (SiC DPF & SCR) Retrofit Kit** (`hooghly-ferry-exhaust-retrofit`) — Marine exhaust aftertreatment targeting acute commuter exposure at enclosed passenger ghats.

4. **Empirical Research Gap Detector & Action Matrix**:
   - Catalogs **5 critical research gaps** across geographic voids, uninventoried sources, and speciation absences.
   - Prioritizes the **cheapest credible resolution methods**, favoring remote satellite sensing (Sentinel-5P $\text{NO}_2$, Landsat-9/ECOSTRESS thermal infrared) and open AIS marine telemetry prior to physical field mobilization.

5. **Stage-Gate Engineering Lifecycle Governance**:
   - Manages candidate progression across 8 formal lifecycle stages:
     `Discovered` $\rightarrow$ `Under research` $\rightarrow$ `Evidence reviewed` $\rightarrow$ `Feasibility assessed` $\rightarrow$ `Prototype proposed` $\rightarrow$ `Prototype developed` $\rightarrow$ `Pilot ready` $\rightarrow$ `Pilot validated`.
   - **Strict Gating Rules**:
     - *Gate 1*: Progression to `Evidence reviewed` is blocked without verifiable statutory citations.
     - *Gate 2*: Progression to `Pilot validated` is blocked without an empirical verification dataset. A prototype's physical existence does not constitute validation.

6. **Dedicated Opportunity Explorer Interface**:
   - Full workstation UI accessible from the primary sidebar with 5 dedicated interactive tabs:
     - **Tab A: Candidate Prioritization & Scoring**: Sortable candidate table with live 8-criteria weight sliders and heuristic disclaimers.
     - **Tab B: Engineering Dossier**: Comprehensive 14-field specification, radar breakdown, Bill of Materials, risks, and IP opportunities.
     - **Tab C: Stage-Gate Pipeline & Shortlist**: Visual Kanban board with stage transition modals and shortlisting decision governance.
     - **Tab D: Research Gap Detector**: Filterable gap catalog by severity with remote resolution indicators.
     - **Tab E: Evidence Inventory & Sectors**: Dataset provenance metrics and 8 independent sector cards.

7. **AI-Assisted Opportunity Analysis**:
   - Extended AI Assistant drawer with candidate comparison tools, ranking explanations, contradictory evidence resolution (e.g. TERI road transport vs. NEERI foundry industrial share), and technical pilot research question generation.

---

## 12 Core Application Modules

| Module | Purpose & Capabilities | Milestone 4 Enhancements |
| :--- | :--- | :--- |
| **1. Overview** | Regional air quality summary, 6 pollutant NAAQS cards, MapLibre telemetry map, 7-day trend envelope. | Live provider connection pills (OpenAQ, Open-Meteo, WBPCB, CPCB) and ground vs. modelled weather banner. |
| **2. Live Air Quality** | CAAQM station list, CPCB NAQI calculation with sub-indices, 48-hour history, raw vs. validated data inspection. | Live observation updates from OpenAQ v3 with original station identifiers. |
| **3. Pollution Explorer** | Diurnal hourly profiles (24h), Day-of-week patterns, bivariate correlation with Pearson/Spearman and non-causal caveat. | Direct connection to the real-time Environmental Analysis Engine. |
| **4. Geographic Hotspots** | 9 evaluated zones across Kolkata and Howrah, distance to nearest station, uncertainty classification. | Spatial coverage void alerts for unmonitored foundry and port industrial belts. |
| **5. Source Intelligence** | Published source apportionment (TERI 2025, NEERI 2020), winter/summer sector shares, chemical marker directory. | Verifiable research findings with exact publication citations, page numbers, and table references. |
| **6. Weather & Atmosphere** | Hourly temperature, relative humidity, wind speed, wind direction, Planetary Boundary Layer Height (PBLH), 16-sector wind rose. | Synoptic reanalysis telemetry from Open-Meteo High-Resolution models classified as `MODELLED`. |
| **7. Research Library** | Searchable repository of foundational papers (WBPCB, TERI, CPCB, NEERI) with metadata, methodology, findings. | Full methodological metadata and limitation disclosures for every paper. |
| **8. Intervention Lab** | Candidate engineering hypotheses, multi-criteria quantitative scoring, counterfactual verification design. | Counterfactual evaluation frameworks with control stations and de-weathering requirements. |
| **9. Analysis Workspace** | Multi-station researcher workbench for custom diurnal, scatter, daily, and pollution rose investigations. | Save named research configurations, persistent SQLite storage, and direct CSV dataset download. |
| **10. Opportunity Explorer** *(New)* | Multi-criteria opportunity scoring, 14-field engineering dossiers, stage-gate governance, and research gap detector. | 5 dedicated interactive tabs for candidate evaluation, dynamic weight customizer, gap resolution matrix, and shortlisting. |
| **11. Data Sources & Quality** | Ingestion audit logs, 3-sigma outlier inspector, completeness rate, multi-format CSV import selector. | Live "Trigger Ingestion Refresh" button, multi-format CSV import (PRANA, CPCB CCR, WBPCB), and live status telemetry. |
| **12. Settings** | Air shed geographic bounding box, CPCB NAQI configuration, database and API status. | Live status of internal SQLite engine, external API credentials, and boundary configs. |

---

## Technology Stack

### Frontend
- **Framework**: Next.js 15 (App Router) with React 19 & TypeScript
- **Styling**: Tailwind CSS (Dark research workstation palette: `#0C0F14`, `#FFE547`, `#8A9A8F`)
- **Visualizations**: Recharts (diurnal cycles with confidence envelopes, day-of-week, bivariate scatter with regression trendlines, 16-sector roses)
- **Geospatial Mapping**: MapLibre GL JS with Carto Dark Matter raster tiles (zero API key required)
- **Icons**: Lucide React

### Backend
- **Framework**: Python 3.12 FastAPI
- **Database**: Zero-setup embedded SQLite (`backend/data/prana.db`), 100% schema-compatible with PostgreSQL/PostGIS
- **Engines**: Opportunity Evaluation Engine (`backend/services/opportunity_engine.py`), Research Gap Detector (`backend/services/gap_detector.py`), Environmental Analysis Engine (`backend/services/environmental_analysis_engine.py`)
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

# Execute Milestone 4 schema migrations & candidate seeding
python backend/migrate_milestone4.py

# Start FastAPI backend server (Runs on port 8000 with auto-reload)
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

# Start Next.js development server (Runs on port 3000)
npx next dev -p 3000
```

Open your browser at:
`http://localhost:3000`

---

## Automated Verification Suite

Run the full end-to-end Python test suites:

```powershell
# Run all 39 automated tests (Milestones 1, 2, 3, and 4)
python -m unittest discover tests

# Or run Milestone 4 specific verification suite:
python -m unittest tests/test_milestone4.py
```

The automated suite executes **39 integration tests** verifying:
1. **Candidate Opportunity Model Integrity**: All 14 mandatory fields non-empty and validated.
2. **Evidence Inventory Synthesis**: Aggregation of ground observations, stations, and statutory literature.
3. **Independent Sector Evaluations**: Complete coverage across all 8 sectors with chemical markers and shares.
4. **8-Criteria Multi-Metric Scoring**: Normalization of dynamic weights and responsive rank recalculation.
5. **Non-Measurement Heuristic Disclaimer**: Statutory verification that composite scores are labeled as decision heuristics.
6. **Stage-Gate Governance**: Blocking progression to `Evidence reviewed` without literature citations and blocking `Pilot validated` without empirical verification datasets.
7. **Shortlisting Decision Workflow**: Transition audits and justification notes.
8. **Research Gap Detection & Auditing**: Identification of unmonitored zones (Jalan, Uluberia, Khidirpur) and low-cost remote resolution recommendations.
9. **AI Opportunity Assistant**: Grounded candidate comparisons, ranking rationales, and contradiction resolution.

---

## Scientific Documentation & Reports

- [OPPORTUNITY_ASSESSMENT_REPORT.md](file:///D:/project-prana/OPPORTUNITY_ASSESSMENT_REPORT.md): Comprehensive Milestone 4 engineering opportunity assessment synthesizing the evidence inventory, sector evaluations, candidate dossiers, research gaps, and prioritized roadmap.
- [LIMITATIONS.md](file:///D:/project-prana/LIMITATIONS.md): Scientific protocols, non-attribution boundaries of ambient sensor data, modelled weather caveats, stage-gate governance rules, and counterfactual intervention guidelines.
- [PROVIDER_INTEGRATION_REPORT.md](file:///D:/project-prana/PROVIDER_INTEGRATION_REPORT.md): Comprehensive architectural analysis of external providers, endpoints, authentication barriers, data schemas, and reliability matrix.
- [DATA_INTEGRITY_AUDIT.md](file:///D:/project-prana/DATA_INTEGRITY_AUDIT.md): Forensic audit analyzing seeded observations, data classifications, completeness formulas, and provider connectivity.
- [STATION_VERIFICATION_REPORT.md](file:///D:/project-prana/STATION_VERIFICATION_REPORT.md): Dossier for all statutory CAAQM stations with CPCB Site IDs, coordinates, verified parameters, and spatial coverage voids.
