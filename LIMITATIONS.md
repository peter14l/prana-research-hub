# PRANA Research Hub: Scientific Protocols, Boundaries & Technical Limitations
## Updated for Milestone 3: Automated Data Collection & Environmental Analysis

This document governs the scientific boundaries, institutional access realities, spatial coverage voids, and methodological protocols implemented across the **PRANA Research Hub** for the Kolkata–Howrah conurbation of West Bengal, India.

---

### 1. Ambient Sensor Telemetry vs. Source Attribution

* **Fundamental Rule**: Ambient particulate matter ($\text{PM}_{2.5}$ and $\text{PM}_{10}$) measured at ground monitoring stations represents a complex, thoroughly mixed atmospheric cocktail of multiple primary emissions and secondary chemical reaction products.
* **Non-Attribution Boundary**: A sensor reading at a specific station (e.g., Victoria Memorial or Ghusuri) **does not identify the source responsible for that concentration**.
* **Methodological Separation**: The platform strictly enforces visual and conceptual separation across:
  1. **Ambient Concentrations** (Ground sensor telemetry)
  2. **Published Source Apportionment** (Receptor modeling: PMF 5.0, CMB 8.2)
  3. **Emissions Inventory Estimates** (Bottom-up activity data $\times$ emission factors)
  4. **Satellite Observations** (Atmospheric column totals, not ground breathing level)
  5. **Statistical Associations** (Empirical correlations under shared meteorology)
  6. **Research Hypotheses** (Unverified intervention proposals)

---

### 2. External Provider Telemetry & Institutional Realities

#### 2.1 OpenAQ API v3 Authentication
* **Status**: `CONNECTED` (Authenticated via `X-API-Key`)
* **Coverage Scope**: OpenAQ aggregates statutory data from available public feeds. In the Kolkata–Howrah bounding box ($88.15^\circ\text{E}, 22.40^\circ\text{N}$ to $88.55^\circ\text{E}, 22.70^\circ\text{N}$), OpenAQ indexes 17 monitoring stations.
* **Important Caveat**: OpenAQ coverage **does not equal 100% of official monitoring coverage**. Certain state and central stations experience delayed or intermittent indexing. A station appearing in OpenAQ does not automatically make it a verified statutory site without CPCB NCAP cross-referencing.

#### 2.2 West Bengal Pollution Control Board (WBPCB)
* **Status**: `MANUAL_PORTAL_ONLY`
* **Limitation**: The state portal (`https://aqmsdata.wbpcb.gov.in/`) is a client-rendered application that **does not provide an unauthenticated public REST API**. Automated scraping of gated government web infrastructure is prohibited.
* **Supported Access**: PRANA supports researcher-assisted CSV imports of official portal downloads with automated column mapping and SHA-256 cryptographic provenance hashing.

#### 2.3 Central Pollution Control Board (CPCB)
* **Status**: `AUTH_REQUIRED` / Official CCR CSV
* **Limitation**: Real-time programmatic queries via Open Government Data (`api.data.gov.in`) require an institutional `DATAGOV_API_KEY`.
* **Scientific Protocol**: CPCB official National Air Quality Index (NAQI) values are **strictly separated** into `StationAQIRecord` and are never mixed with continuous mass concentrations in `ValidatedObservation`.

---

### 3. Modelled Reanalysis vs. Ground Weather Stations

* **Data Classification**: All weather variables (Temperature, Relative Humidity, Wind Speed, Wind Direction, Precipitation, Surface Pressure, Boundary Layer Height) ingested via Open-Meteo are strictly classified as:
  $$\text{data\_classification} = \text{'MODELLED'}$$
* **Scientific Disclosure**: Reanalysis data is generated from high-resolution numerical weather prediction models (ECMWF ERA5 / IFS reanalysis), **not physical local weather anemometers or thermometers** mounted at monitoring stations.
* **Microclimate Limitations**: Localized street-canyon wind eddies, rooftop thermal anomalies, and building wake effects are not resolved by synoptic numerical reanalysis.

---

### 4. Non-Causality of Meteorological Correlations

* **Planetary Boundary Layer Dynamics**: During winter (November–February), nocturnal Planetary Boundary Layer Height (PBLH) collapses from $>1,500\text{ m}$ to $<200\text{ m}$ under calm conditions ($<5\text{ km/h}$). This traps pollutants regardless of whether local emissions increased.
* **Dispersion vs. Emission**: An inverse correlation between wind speed and $\text{PM}_{2.5}$ reflects atmospheric dispersion dilution physics, **not a reduction in source emissions**.
* **Wind Direction Caveat**: North-North-Westerly (NNW) wind flow aligns with the regional Indo-Gangetic Plain transport corridor. Wind blowing from the direction of a known factory **does not prove that factory is the primary or sole emitter**.

---

### 5. Spatial Coverage Voids & Prohibition of Spurious Interpolation

* **Monitoring Density**: Kolkata and Howrah operate only 9 continuous statutory CAAQM stations across a conurbation of over 14 million residents.
* **Documented Coverage Voids**:
  1. **Jalan Industrial Complex & Domjur Foundry Belt**: Cupola iron foundries and heavy casting clusters have zero continuous ambient monitors within an 8.4 km radius.
  2. **Khidirpur Docks & Kolkata Port Terminal**: Heavy marine bunker combustion and freight idling occur in a 4.2 km monitoring void.
  3. **Uluberia Industrial & Engineering Cluster**: Located 18.5 km from the nearest statutory monitor, far exceeding urban station representativeness limits.
  4. **Budge Budge Petroleum Refining & Storage Fringe**: Located 14.8 km from the nearest particulate monitor.
* **PRANA Scientific Standard**: The platform **strictly refuses to interpolate or extrapolate ward-level pollution heatmaps** across these voids. When distance to the nearest station exceeds 3.5 km, the zone is explicitly classified as a **Coverage Gap with High Uncertainty**.

---

### 6. Engineering Intervention Verification Protocols

* **Hypothesis Status**: Candidate engineering interventions proposed in the Intervention Lab (e.g., Howrah foundry divided-blast retrofits, Hooghly ferry electrification, BT Road arterial dust suppression) are research hypotheses.
* **Counterfactual Requirements**: Proving emission reduction requires:
  1. Minimum 60-day pre-intervention verified baseline.
  2. Concurrent observation at an unaffected control station (e.g., Victoria Memorial).
  3. Meteorological de-weathering (e.g., machine learning GAM / Random Forest models) to decouple weather fluctuations from engineering impact.
  4. Never claiming an intervention reduced pollution based solely on historical correlation.

---

### 7. Turnkey Architecture & PostGIS Path

* **Embedded SQLite**: Per requirements avoiding external database daemons or Docker, the platform runs on zero-daemon embedded SQLite (`backend/data/prana.db`).
* **PostGIS Compatibility**: Geodesic Haversine spatial calculations and SQLAlchemy models are 100% schema-compatible with PostgreSQL + PostGIS for cloud scaling.

---

### 8. Opportunity Prioritization Heuristics & Engineering Boundaries (Milestone 4)

* **Composite Scores as Prioritization Heuristics, Not Physical Measurements**:
  - The multi-criteria **Weighted Priority Score** generated in the Opportunity Explorer is a structured decision-support heuristic designed to guide engineering allocation.
  - It is **never a scientific measurement** of particulate mass, ambient air quality index, or guaranteed venture success.
  - Scores must always be presented alongside their underlying 8 criteria breakdown, active weights, and qualitative score rationales.

* **Stage-Gate Lifecycle Governance**:
  - A candidate opportunity cannot advance to `Evidence reviewed` without a non-empty, verifiable citation linking to statutory literature (e.g. TERI 2025, NEERI 2020) or verified CAAQM telemetry.
  - **Prototype Existence Does Not Equal Validation**: A candidate project cannot be marked as `Pilot validated` merely because a physical prototype or benchtop rig exists. Progression to `Pilot validated` strictly requires an empirical verification dataset demonstrating counterfactual mass reduction under de-weathered conditions.

* **Engineering Assumptions vs. Operating Realities**:
  - *Howrah Foundry Retrofit*: Flue gas temperature fluctuations (spiking from 350°C to 800°C) during cupola burndown cycles require active thermal decoupling. Space constraints inside century-old Howrah foundry sheds may prevent standard baghouse installation without structural redesign.
  - *Industrial Fence-Line Network*: Optical particle counters experience severe hygroscopic growth drift when relative humidity exceeds 80% during Kolkata winter mornings. Dynamic heated inlet de-humidification must be balanced against solar-battery power budgets.
  - *Landfill Refuse Fire Suppression*: Subsurface anaerobic decomposition produces aggressive corrosive atmospheres ($H_2S$, volatile organic acids, leachate aerosols) that attack optical sensors and pneumatic probes.
  - *River Ferry Aftertreatment*: Exhaust backpressure on aging marine mechanical diesel engines must remain within strict manufacturer limits to avoid voiding inland maritime safety certifications.

* **Non-Guarantee of Intellectual Property (IP) Novelty**:
  - IP opportunities identified in candidate dossiers represent exploratory technical pathways (e.g., small-footprint artisanal cupola thermal decouplers, low-temp electrically assisted marine DPF cassettes).
  - They **do not constitute legal patentability claims** without exhaustive formal prior-art searches and patent attorney freedom-to-operate analyses.
