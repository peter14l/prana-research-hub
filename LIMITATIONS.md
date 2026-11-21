# PRANA Research Hub: Scientific & Technical Limitations

This document outlines the methodological boundaries, spatial coverage gaps, and engineering assumptions governing the **PRANA Research Hub** for the Kolkata–Howrah air shed.

---

## 1. Ambient Sensor Telemetry vs. Source Attribution

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

## 2. Spatial Coverage Gaps & Prohibition of Spurious Interpolation

* **Monitoring Density**: Kolkata and Howrah operate 9 statutory Continuous Ambient Air Quality Monitoring (CAAQM) stations. While these provide high-fidelity temporal observations at specific points, spatial coverage is non-uniform.
* **Identified Coverage Voids**:
  * **South-West Kolkata & Port Area**: Khidirpur Dock System, Taratala, Behala, and Thakurpukur have **zero continuous ambient monitors within a 4–7 km radius**, despite heavy diesel port freight transit.
  * **Howrah Rural/Inland Industrial Periphery**: Kona Expressway interior, Domjur, and outer Liluah lack continuous monitoring.
  * **East Kolkata Wetlands Buffer**: Dhapa municipal landfill fires are monitored distantly from Bidhannagar and Ballygunge.
* **PRANA Scientific Standard**: The platform **strictly refuses to interpolate or extrapolate ward-level pollution estimates** across these voids. When distance to the nearest station exceeds 3.5 km, the zone is explicitly classified as a **Coverage Gap with High Uncertainty**.

---

## 3. National Air Quality Index (NAQI) Validity

* **Statutory CPCB Protocols**: Official Indian National Air Quality Index values require:
  1. At least 3 monitored parameters.
  2. At least one parameter must be either $\text{PM}_{2.5}$ or $\text{PM}_{10}$.
* **Transparent Fallback**: When a station experiences telemetry loss on particulate analyzers, the platform does not fabricate an AQI; it marks the status as **"Insufficient Data for Official AQI"** and presents the available sub-indices independently.

---

## 4. Meteorological Coupling & Non-Causality

* **Boundary Layer Dynamics**: During winter (December–February), nocturnal Planetary Boundary Layer Height (PBLH) collapses from $>1,500\text{ m}$ to $<400\text{ m}$ under calm conditions ($<7\text{ km/h}$). This traps pollutants regardless of whether local emissions increased.
* **Wind Direction Caveat**: North-North-Westerly (NNW) wind flow aligns with the regional Indo-Gangetic Plain transport corridor. Wind direction pointing toward a monitor from a known facility **does not prove that facility is the sole or dominant emitter**.

---

## 5. Engineering Intervention Verification Framework

* **Counterfactual Requirements**: Candidate engineering interventions proposed in the Intervention Lab (e.g., Howrah foundry divided-blast retrofits, river ferry shore electrification) are scientific hypotheses.
* **De-Weathering Necessity**: Proving emission reduction requires:
  * Minimum 60-day pre-intervention baseline.
  * Concurrent observation at an unaffected control station (e.g., Victoria Memorial).
  * Machine learning de-weathering (e.g., Random Forest or GAM) to isolate weather fluctuations from engineering impact.

---

## 6. Architecture & Database Design

* **Zero-Daemon Turnkey SQLite**: Per product requirements to avoid Docker or local database services, the platform uses an embedded, zero-daemon SQLite file (`backend/data/prana.db`).
* **Geospatial Processing**: Spatial distance and gap analyses are executed in-memory using geodesic Haversine algorithms and Shapely geometries, with schemas structured for seamless 1:1 migration to PostgreSQL/PostGIS in production cloud environments.
