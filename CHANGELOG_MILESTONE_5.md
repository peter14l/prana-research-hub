# PRANA Research Hub: Changelog — Milestone 5
## Evidence Integrity & Opportunity Recalibration

**Release Date:** 2026-11-21  
**Milestone:** Milestone 5: Evidence Integrity & Opportunity Recalibration  
**Platform Status:** Grounded in Statutory Telemetry, Verifiable Peer-Reviewed Research, and Zero-Credit Evidence Integrity  

---

### Executive Overview

Milestone 5 resolves empirical integrity defects in PRANA's Opportunity Discovery system. Previously, candidate opportunities could receive inflated evidence confidence scores based on narrative claims, unfulfilled satellite citations, or synthetic test observations. Under Milestone 5:
1. Every candidate underwent a forensic evidence audit against raw database records.
2. Distinct evidence classifications were established, enforcing a **Zero-Credit Rule** (synthetic records, unverified hypotheses, and missing citations yield 0.0 evidence score credit).
3. The Jalan industrial candidate was corrected to eliminate unsupported unit counts, correct the statutory monitoring gap to a mathematically derived **8.56 km**, remove unverified nocturnal spike claims, and recalibrate its evidence score from **8.8 down to 3.5 / 10**.
4. The opportunity ranking was authentically recalibrated, elevating the **Howrah Foundry Cupola Retrofit** to **Rank #1** (7.93 / 10 priority score, 6.8 / 10 evidence score), while maintaining historical pre-audit scores for transparent auditability.

---

### 1. Jalan Industrial Candidate Corrections (`industrial-fence-line-attribution`)

| Feature / Claim | Pre-Audit Milestone 4 Value | Milestone 5 Audited & Corrected Value | Classification |
|---|---|---|---|
| **Industrial Unit Count** | "2,000+ industrial units" in Jalan | Removed from problem statement & gaps; unreferenced in DB | `UNVERIFIED_HYPOTHESIS` (0 Cr) |
| **Nearest Statutory Station Gap** | 7.0 / 7.2 km monitoring gap | **8.56 km** geodesic distance to Padmapukur CAAQM (`site_5010`) | `DERIVED_RESULT` (Haversine) |
| **Padmapukur Nocturnal PM2.5 Spikes** | "Sharp midnight-to-dawn spikes > 180 µg/m³" | Removed from candidate text. Raw DB inspection proved zero midnight records > 180 µg/m³ exist; only two midday readings (12:00 PM and 1:00 PM on 2026-11-19) exist, both tagged synthetic `DEMO`. | `SYNTHETIC_DATA` (0 Cr) |
| **North-Westerly Wind Association** | Causal association of nocturnal spikes with calm NW winds | Reclassified as an untested meteorological hypothesis; no causal regression is linked in DB. | `UNVERIFIED_HYPOTHESIS` (0 Cr) |
| **NASA VIIRS Night Radiance** | "Dense night combustion signatures" | Removed until raw satellite raster/vector data is ingested into PRANA database. | `MISSING_EVIDENCE` (0 Cr) |
| **Evidence Strength Score** | 8.8 / 10 | **3.5 / 10** (Only the derived 8.56 km monitoring void is authentic) | Recalibrated |
| **Weighted Priority Score** | 8.44 / 10 | **7.64 / 10** (Shifts from Rank #1 to Rank #2) | Recalibrated |

---

### 2. Forensic Audit Across All Candidate Opportunities

Every candidate in `candidate_opportunities` was audited claim-by-claim:

1. **Howrah Foundry Cupola Retrofit (`howrah-foundry-cupola-retrofit`)**:
   - *Verified Evidence*: Directly supported by **CSIR-NEERI (2020) Table 6.14** (34% winter industrial PM2.5 in Ghusuri) [`PUBLISHED_RESEARCH - DIRECT SUPPORT`] and CPCB Ghusuri station `site_5008` telemetry [`VERIFIED_OBSERVATION`].
   - *Audit Deficit*: Cited WBPCB 2022 survey document is not stored in DB [`MISSING_EVIDENCE`]; ~350 cupola count is unreferenced [`UNVERIFIED_HYPOTHESIS`].
   - *Score Recalibration*: Evidence score adjusted from **9.5 to 6.8 / 10**. Takes **Rank #1** (Weighted Priority: **7.93 / 10**).

2. **Optical & Thermal Fence-Line Plume Attribution (`industrial-fence-line-attribution`)**:
   - *Verified Evidence*: Haversine distance from Jalan centroid (22.59°N, 88.24°E) to Padmapukur CAAQM station (22.5632°N, 88.3182°E) is **8.56 km** [`DERIVED_RESULT`].
   - *Audit Deficit*: Unit count unverified, nocturnal spikes absent/synthetic, VIIRS uncataloged.
   - *Score Recalibration*: Evidence score adjusted from **8.8 to 3.5 / 10**. Moves to **Rank #2** (Weighted Priority: **7.64 / 10**).

3. **Autonomous Landfill Thermal Suppression for Dhapa (`landfill-fire-thermal-suppression`)**:
   - *Verified Evidence*: TERI (2025) Table 4.6 documents 14% regional winter PM2.5 from waste burning [`PUBLISHED_RESEARCH - REGIONAL CONTEXT`].
   - *Audit Deficit*: Dhapa-specific VIIRS thermal anomaly files are uningested in DB [`MISSING_EVIDENCE`]; causal link to downwind CO spikes is unproven [`UNVERIFIED_HYPOTHESIS`].
   - *Score Recalibration*: Evidence score adjusted from **8.5 to 4.2 / 10**. Holds **Rank #3** (Weighted Priority: **7.57 / 10**).

4. **Hooghly River Passenger Ferry Exhaust Retrofit (`hooghly-ferry-exhaust-retrofit`)**:
   - *Verified Evidence*: TERI (2025) Section 3.4 identifies marine emissions as an uninventoried research deficit [`PUBLISHED_RESEARCH - GAP ACKNOWLEDGEMENT`].
   - *Audit Deficit*: Near-total absence of empirical ferry engine logs, operating fuel sulfur assays, or tailpipe emission factors [`MISSING_EVIDENCE`].
   - *Score Recalibration*: Evidence score adjusted from **6.8 to 2.0 / 10**. Holds **Rank #4** (Weighted Priority: **6.83 / 10**).

---

### 3. Separation of Evidence from Assumptions

1. **Six Standardized Evidence Classifications**:
   - `VERIFIED_OBSERVATION`: Physical measurement recorded by statutory reference analyzer (e.g. CPCB CAAQM telemetry).
   - `PUBLISHED_RESEARCH`: Peer-reviewed scientific finding or statutory study (e.g. TERI 2025, CSIR-NEERI 2020).
   - `DERIVED_RESULT`: Mathematically derived spatial/geometric calculation from verified coordinates (e.g. 8.56 km Haversine distance).
   - `SYNTHETIC_DATA`: Demonstration or simulated records used for testing; receives **0.0 credit**.
   - `UNVERIFIED_HYPOTHESIS`: Plausible technical narrative lacking linked empirical records in DB; receives **0.0 credit**.
   - `MISSING_EVIDENCE`: Cited document, satellite vector, or survey not present in PRANA repository; receives **0.0 credit**.

2. **Programmatic Zero-Credit Rule**:
   Implemented in `OpportunityEngine.calculate_evidence_score_from_audit()`. Synthetic data, unverified hypotheses, and missing citations cannot increase confidence scores above baseline.

---

### 4. Rebuilt 6-Dimension Evaluation Framework

Evaluation dimensions were formally decoupled from narrative technical claims into 6 independent metrics (`rebuilt_scores`):
1. **Pollution Impact Potential**: Estimated particulate mass reduction potential.
2. **Evidence Strength (Audited)**: Traceable statutory and peer-reviewed scientific support.
3. **Engineering Feasibility**: Technology readiness level (TRL) and operational complexity.
4. **Prototype Affordability**: Bill of materials (BOM) capital requirements.
5. **Measurement & Verification (M&V) Feasibility**: Availability of counterfactual baseline and de-weathering protocols.
6. **Partnership Feasibility**: Institutional willingness and regulatory agency alignment.

---

### 5. Frontend UI Enhancements (`OpportunityExplorerView.tsx`)

1. **Audit Status Badges & Warnings**:
   - Warning badge `⚠️ SYNTHETIC DEP (0 Cr)` appears when a candidate has synthetic dependencies.
   - Warning badge `⚠️ UNVERIFIED CLAIMS` appears when unreferenced narrative claims are present.
   - `Derived Distance [DERIVED]` badge highlights mathematically calculated spatial voids.
2. **Pre-Audit vs. Post-Audit Score Transparency**:
   - Comparison table and dossier header display strikethrough pre-audit scores alongside recalibrated scores (e.g. `Pre-Audit: 8.8 -> Audited: 3.5`).
3. **Claim-by-Claim Forensic Audit Trail**:
   - Dedicated interactive table rendering every audited claim, classification status badge, source citation, support type, and auditor scientific notes.
4. **Verified vs. Missing Evidence Summaries**:
   - Side-by-side green and rose cards displaying authentic evidence vs. disclosed data deficits.

---

### 6. Automated Verification Suite (`tests/test_milestone5.py`)

Added 7 comprehensive unit tests verifying:
- Jalan candidate corrections (8.56 km derived distance, no 2,000+ unit claim, no synthetic spike claims).
- Zero-credit rule prevents synthetic and unverified data from inflating scores.
- All 6 distinct evidence classifications are enforced.
- Recalibrated evidence scores across all 4 candidates.
- Pre-audit scores are preserved for auditability.
- Authentic evidence inverts ranking to place Howrah Foundry Cupola Retrofit at Rank #1.
- Rebuilt 6-dimension scores are present and bounded.
- Entire repository test suite passes with **46 passing tests** across Milestones 1–5.
