# PRANA Research Hub: Kolkata–Howrah Environmental Intelligence

**PRANA Research Hub** is a research-grade environmental intelligence and geospatial analysis web platform built for **PRANA**, an early-stage clean-air technology initiative investigating outdoor air pollution across the **Kolkata–Howrah twin cities of West Bengal, India**.

This platform is engineered to identify scientifically defensible, measurable pollution-reduction opportunities for PRANA's first engineering pilot projects.

---

## Key Questions Answered

1. **Where are concentrations highest, and how do they change over time?**
   - Live telemetry across 9 statutory CAAQM stations in Kolkata and Howrah.
   - Diurnal 24-hour profiles isolating morning commute spikes and nocturnal winter inversion spikes.
2. **What are the likely contributing emission sources?**
   - Grounded in official source-apportionment studies: **TERI (2025)** and **CSIR-NEERI (2020)**.
   - Strict separation between ambient sensor measurements, receptor modeling (PMF/CMB), and bottom-up emissions inventories.
3. **Which areas, pollutants, and sources deserve further investigation?**
   - Spatial coverage gap audit identifying unmonitored zones (e.g., Khidirpur Port, South-West Kolkata, rural Howrah).
   - Hotspot identification with uncertainty estimation (refuses spurious ward-level interpolation).
4. **Which interventions could realistically reduce pollution, and how can they be measured?**
   - **Intervention Lab**: Candidate engineering hypotheses (Howrah foundry divided-blast retrofits, Hooghly ferry electrification, BT Road arterial dust suppression).
   - Counterfactual evaluation framework with control stations and meteorological de-weathering.

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
- **Database**: Zero-setup embedded SQLite (`backend/data/prana.db`), fully compatible with PostgreSQL/PostGIS
- **ORM & Validation**: SQLAlchemy 2.0 & Pydantic
- **Scientific Computing**: Pandas, NumPy, SciPy, Scikit-learn, Shapely

---

## 10 Core Application Modules

| Module | Purpose & Capabilities |
| :--- | :--- |
| **1. Overview** | Regional air quality summary, 6 pollutant NAAQS cards, MapLibre telemetry map, 7-day trend envelope, evidence-backed highlights. |
| **2. Live Air Quality** | CAAQM station list, CPCB NAQI calculation with sub-indices, 48-hour history, raw vs. validated data inspection, CSV export. |
| **3. Pollution Explorer** | Diurnal hourly profiles (24h), Day-of-week patterns, bivariate correlation with Pearson/Spearman and non-causal caveat, multi-station comparison. |
| **4. Geographic Hotspots** | 9 evaluated zones across Kolkata and Howrah, distance to nearest station, uncertainty classification, explicit coverage gap warnings. |
| **5. Source Intelligence** | Published source apportionment (TERI 2025, NEERI 2020), winter/summer sector shares, chemical marker directory, evidence labels. |
| **6. Weather & Atmosphere** | Hourly temperature, relative humidity, wind speed, wind direction, Planetary Boundary Layer Height (PBLH), 16-sector wind rose. |
| **7. Research Library** | Searchable repository of foundational papers (WBPCB, TERI, CPCB, NEERI) with metadata, methodology, findings, and user annotations. |
| **8. Intervention Lab** | Candidate engineering hypotheses, multi-criteria quantitative scoring (feasibility, reduction, verification), counterfactual verification design. |
| **9. Data Sources & Quality** | Ingestion audit logs, 3-sigma outlier inspector, completeness rate (99.8%), manual CSV dataset import with schema validation. |
| **10. Settings** | Air shed geographic bounding box, CPCB NAQI configuration, database and API status. |

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

# Seed database with authentic Kolkata-Howrah research dataset (if not already seeded)
python -m backend.seed.seed_data

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

# Install dependencies (already installed)
pnpm install

# Start Next.js development server (Runs on port 3000)
pnpm run dev
```

Open your browser at:
`http://localhost:3000`

---

## Automated Verification Suite

Run the full end-to-end Python test suite:

```powershell
python -m unittest tests/test_suite.py
```

Tests verify:
- Exact CPCB NAQI breakpoint interpolation and the 3-parameter validity rule.
- Geodesic spatial distance and coverage gap threshold classification.
- Bivariate Pearson & Spearman correlation engine with scientific non-causal disclaimer.
- FastAPI endpoints for all 10 modules.

---

## Production Deployment

### Production Build
```powershell
# Build frontend
cd frontend
pnpm run build

# Start production server
pnpm run start -p 3000
```

### Environment Configuration
Copy `.env.example` to `.env` and set optional variables as desired:
```ini
DATABASE_URL=sqlite:///./backend/data/prana.db
OPENAQ_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```

---

## Scientific Protocols & Limitations

Please read [LIMITATIONS.md](file:///D:/project-prana/LIMITATIONS.md) for full documentation on:
- Non-attribution boundaries of ambient sensor data.
- Spatial coverage voids in South-West Kolkata and outer Howrah.
- Meteorological de-weathering requirements for counterfactual intervention verification.
