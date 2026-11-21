# PRANA Research Hub: Documented Unresolved Issues & Scientific Gaps
## Milestone 2: Data Integrity, Provenance & Scientific Verification

This document catalogs known systemic constraints, institutional boundaries, external API barriers, and spatial voids identified during the Milestone 2 forensic audit and verification implementation.

In compliance with PRANA's scientific defensibility mandate, these issues are explicitly documented rather than masked through simulated or synthetic approximations.

---

### 1. External Data Integration Realities

#### 1.1 OpenAQ API v3 Authentication Barrier
- **Status**: `AUTH_REQUIRED` (Connection Suspended)
- **Technical Barrier**: OpenAQ deprecated its open unauthenticated v2 endpoints. Version 3 requires an `X-API-Key` header with registered institutional credentials. Automated requests without a key return `HTTP 401 Unauthorized`.
- **System Behavior**: The source reliability monitor correctly classifies OpenAQ as `AUTH_REQUIRED` and displays the exact HTTP 401 error message. It refuses to pretend live telemetry is arriving.
- **Resolution Path**: PRANA infrastructure administrators must register at [OpenAQ Console](https://explore.openaq.org/) and supply `OPENAQ_API_KEY` in the server environment.

#### 1.2 State & National Environmental Portals Lack Public REST APIs
- **Status**: `MANUAL_PORTAL_ONLY`
- **Technical Barrier**: Neither the West Bengal Pollution Control Board (WBPCB) nor the Central Pollution Control Board (CPCB) continuous portals (`cpcbccr.com`) expose open, unauthenticated REST APIs for automated programmatic polling. Access is gated behind session-based web viewers or periodic Open Government Data (`data.gov.in`) bulk releases.
- **System Behavior**: Both WBPCB and CPCB are classified as `MANUAL_PORTAL_ONLY`. The platform provides an automated cryptographic CSV ingestion engine with SHA-256 provenance hashing and schema validation so researchers can import official portal extracts with full audit trails.
- **Resolution Path**: Establish an institutional MoU with WBPCB/CPCB for automated API access tokens, or maintain scheduled researcher ingestions.

---

### 2. Spatial Coverage Voids & Unmonitored Hotspots

The Kolkata–Howrah metropolitan air basin contains only **9 continuous statutory CAAQM stations** across an urban agglomeration of over 14 million people.

#### 2.1 Howrah Industrial Heavy-Casting Belt
- **Unmonitored Areas**: Jalan Industrial Complex (Sankrail), Domjur cupola foundry belt, Uluberia engineering clusters, Baltikuri metalworking zone.
- **Nearest Station**: Ghusuri (`site_5008`) or Padmapukur (`site_5010`), situated 6 km to 18 km upwind or crosswind.
- **Scientific Consequence**: Stationary ambient monitors at Ghusuri and Padmapukur register elevated regional background, but cannot resolve localized plume dynamics or fugitive emissions from untagged foundry stacks.
- **PRANA Policy**: Spatial interpolation heatmaps across these voids are prohibited without explicitly displaying high-uncertainty warnings.

#### 2.2 Kolkata Port & South-West Industrial Corridor
- **Unmonitored Areas**: Khidirpur Dock area, Taratala warehousing and transport terminals, Garden Reach shipbuilders, Budge Budge oil refineries and petroleum depot.
- **Nearest Station**: Fort William (`site_5003`) or Ballygunge (`site_5005`), located 5 km to 14 km distant across high-density residential fabric.
- **Scientific Consequence**: Heavy port diesel emissions, marine bunkering fuel combustion, and freight truck congestion are entirely unmeasured by ground statutory monitors.

---

### 3. Speciation & Real-Time Source Apportionment Gaps

#### 3.1 Bulk Mass vs. Chemical Speciation
- **Constraint**: Statutory CAAQM stations report bulk mass concentrations ($\mu\text{g/m}^3$) of criteria pollutants (PM2.5, PM10, $\text{NO}_2$, $\text{SO}_2$, $\text{CO}$, $\text{O}_3$, $\text{NH}_3$).
- **Scientific Limit**: Bulk monitors **cannot** measure chemical speciation (elemental carbon, organic carbon, sulfate, nitrate, trace metals) in real-time.
- **Resolution**: PRANA grounds source attribution in peer-reviewed Positive Matrix Factorization (PMF) and Chemical Mass Balance (CMB) studies:
  - **TERI (2025)**: *Comprehensive Air Pollution Source Apportionment Study for Kolkata and Howrah* (Table 4.5, Table 4.6, pp. 84–92).
  - **CSIR-NEERI (2020)**: *Clean Air Action Plan Source Apportionment Baseline for Kolkata City* (Table 5.2, p. 112).
- **Transparency Policy**: The platform forbids attributing a raw spike at any ground station to a specific source without referencing speciation or synoptic wind-backtrajectory evidence.

---

### 4. Database Engine Scalability & PostGIS Path

- **Current Architecture**: Zero-setup embedded SQLite (`backend/data/prana.db`) with geodesic Haversine distance algorithms implemented in Python/NumPy.
- **Constraint**: Sufficient for 100,000+ hourly observation records and instantaneous spatial filtering. However, high-concurrency multi-user write operations and complex GIS polygon clipping (e.g., PostGIS `ST_Contains`) require PostgreSQL + PostGIS.
- **Resolution Path**: The SQLAlchemy schema and Pydantic models are 100% PostGIS compatible. Switching to PostgreSQL requires changing only the `DATABASE_URL` environment variable.

---

### 5. Summary of Data Integrity Audit Findings

| Audit Component | Finding | Action Implemented in Milestone 2 |
| :--- | :--- | :--- |
| **Seeded Observations** | 10,647 records are synthetic diurnal models | Reclassified 100% of seed data as `DEMO` to eliminate false claims of live telemetry. |
| **Completeness Figure** | Previous 99.8% was valid/total existing | Implemented statutory formula: $\frac{\text{Received Valid}}{\text{Expected Hours} \times \text{Pollutants}}$ with explicit numerator and denominator. |
| **Station Identifiers** | Stations used generic codes (`WB001`) | Cross-referenced all 9 stations against CPCB NCAP registry; assigned statutory Site IDs (`site_5002`–`site_5010`). |
| **External Providers** | Simulated feeds implied live scraping | Classified OpenAQ as `AUTH_REQUIRED` (HTTP 401) and WBPCB/CPCB as `MANUAL_PORTAL_ONLY`. |
| **Research Claims** | Generic apportionment summaries | Linked every finding and sector share to exact published tables and pages in TERI (2025) and NEERI (2020). |
| **Data Ingestion** | No provenance hash on CSV imports | Implemented SHA-256 cryptographic provenance fingerprinting and classification selection (`IMPORTED` vs `VERIFIED`). |
