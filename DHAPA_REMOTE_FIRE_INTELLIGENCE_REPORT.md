# PRANA Research Hub: Dhapa Remote Fire Intelligence Proof of Concept
**Milestone 7 Technical Assessment & Scientific Feasibility Report**  
**Study Target:** Dhapa Municipal Solid Waste Disposal Ground, Kolkata, West Bengal, India  
**Geographic Centroid:** 22.5453°N, 88.4257°E (WGS84) | **Core Area:** 58.4 hectares  
**Boundary Uncertainty:** $\pm 75\,\text{m}$  
**Data Providers & Ingestion Channels:** NASA FIRMS (VIIRS 375 m NOAA-20/21, MODIS 1 km Terra/Aqua), USGS/NASA Landsat 8/9 Collection 2 Level 2 STAC (Path 138 Row 044/045), CPCB/WBPCB CAAQM Ground Telemetry (`prana.db`), Open-Meteo Reanalysis  
**Date of Audit & Analysis:** November 2026  
**Implementation Mode:** Software-Only Research Prototype (Zero Hardware, Zero Field Visits, Zero Autonomous Suppression)

---

## Executive Summary & Core Feasibility Verdict

| Evaluation Parameter | Scientific Assessment & Finding |
|---|---|
| **Primary Investigation** | Can satellite-derived spaceborne thermal infrared observations reliably identify, track, and provide early warning for recurring fires at Dhapa Landfill? |
| **Definitive Feasibility Verdict** | **INSUFFICIENT FOR SPACEBORNE EARLY WARNING OR AUTONOMOUS SUPPRESSION** |
| **Critical Physical Bottleneck** | **Subsurface Smoldering Combustion Blindness:** Landfill fires are predominantly subterranean anaerobic smoldering pockets occurring $2\text{--}6\,\text{m}$ below the compacted refuse crust. Surface skin temperatures remain between $35^\circ\text{C}\text{--}65^\circ\text{C}$ (308–338 K), which is physically undetectable by orbital mid-wave infrared sensors ($3.7\text{--}4.0\,\mu\text{m}$) configured to trigger on flaming combustion ($>600\,\text{K}$). |
| **Spatial Scale Mismatch** | A VIIRS 375 m pixel covers $140,625\,\text{m}^2$ (14.06 ha); early-stage nascent flame fissures span $10\text{--}50\,\text{m}^2$ ($<0.03\%$ of pixel area). Sub-pixel background thermal dilution prevents satellite detection until a fire reaches catastrophic dimensions ($>10\,\text{MW}$ FRP). |
| **Temporal Latency Mismatch** | Sun-synchronous polar orbits provide only 2 overpasses per day (approx 01:30 and 13:30 local solar time), with a 1 to 3 hour FIRMS processing latency. Landfill suppression requires intervention within 15 minutes of surface breakthrough. |
| **Atmospheric Blindness** | Convective monsoon cloud cover over Kolkata averages **$91.6\%$ from June through September**, causing complete optical and thermal blindness during wet season flare-ups. |
| **Causality Finding** | The nearest statutory air-quality monitor (Bidhannagar) is **$4.25\,\text{km}$ away**. Winter thermal inversions trap citywide emissions ($150,000+$ commercial diesel vehicles and $1,000+$ Howrah foundries), elevating regional baseline $\text{PM}_{2.5}$ to $150\text{--}250\,\mu\text{g/m}^3$. Attributing ground station spikes directly to Dhapa fires is scientifically indefensible without dedicated fenceline monitoring. |
| **Defensible Engineering Pathway** | Abandon spaceborne early-warning architectures. Transition research toward **ground-based continuous radiometric LWIR ($8\text{--}14\,\mu\text{m}$) PTZ cameras mounted on perimeter towers ($<30\,\text{second}$ response time) combined with subsurface thermocouple probe arrays and optical methane ($\text{CH}_4$) / $\text{CO}$ fenceline sensors.** |

---

## 1. Study Area Definition & Spatial Geometry

### 1.1 Core Area of Interest (AOI) Boundary
Dhapa municipal disposal ground is Kolkata's primary solid waste destination, receiving approximately 4,000 to 4,500 metric tons of unsegregated municipal solid waste per day. 

* **Site Centroid:** $22.5453^\circ\text{N},\,88.4257^\circ\text{E}$
* **Core Polygon Footprint:** $58.4\,\text{hectares}$ ($0.584\,\text{km}^2$)
* **Coordinate Perimeter (WGS84 closed polygon):**
  1. $[88.4180^\circ\text{E},\,22.5520^\circ\text{N}]$ (Northwest perimeter along Topsia Canal)
  2. $[88.4250^\circ\text{E},\,22.5545^\circ\text{N}]$ (Northern active tipping front)
  3. $[88.4320^\circ\text{E},\,22.5510^\circ\text{N}]$ (Northeast embankment toward East Kolkata Wetlands)
  4. $[88.4335^\circ\text{E},\,22.5440^\circ\text{N}]$ (Eastern compost plant boundary)
  5. $[88.4310^\circ\text{E},\,22.5380^\circ\text{N}]$ (Southeast vegetable farming fringe)
  6. $[88.4230^\circ\text{E},\,22.5365^\circ\text{N}]$ (Southern leachate drainage zone)
  7. $[88.4175^\circ\text{E},\,22.5410^\circ\text{N}]$ (Southwest access corridor)
  8. $[88.4180^\circ\text{E},\,22.5520^\circ\text{N}]$ (Closure point)

### 1.2 Geodesic Comparison Buffers
To prevent attributing ambient urban heat to the landfill and evaluate spatial false positives, two concentric annular geodesic buffers were generated around the geometric centroid:
* **Dhapa 1.0 km Peripheral Buffer:** An annular zone spanning radii from the Core AOI to $1.0\,\text{km}$ ($2.557\,\text{km}^2$). Covers informal waste sorting shanties (Topsia, Mathpukur) and peri-wetland canals where informal plastic stripping and low-temperature wire burning occur.
* **Dhapa 2.0 km Urban Transition Buffer:** An annular zone from $1.0\,\text{km}$ to $2.0\,\text{km}$ radius ($9.425\,\text{km}^2$). Encompasses the Eastern Metropolitan (EM) Bypass commercial arterial corridor, Science City, industrial sheds, and high-emissivity asphalt roads.

### 1.3 Boundary Uncertainty & Spatial Rationale
* **Spatial Uncertainty:** Documented at $\pm 75\,\text{meters}$.
* **Rationale:** Dhapa possesses no rigid masonry boundary. Active waste tipping fronts shift weekly based on bulldozer movement, informal plastic salvaging settlements encroach along the western perimeter, and seasonal leachate inundation during the monsoon alters the southern embankment edge. Point coordinates cannot substitute for this spatial footprint.

```
+-----------------------------------------------------------------------------------+
|                           DHAPA SPATIAL BUFFER SCHEMATIC                          |
|                                                                                   |
|           [ 2.0 km Urban Transition Buffer - 9.43 km² ]                           |
|           (EM Bypass, Science City, Industrial Sheds, Asphalt Solar Heat)         |
|                                                                                   |
|                   [ 1.0 km Peripheral Buffer - 2.56 km² ]                         |
|                   (Mathpukur, Topsia Sorting Shanties, Canals)                    |
|                                                                                   |
|                           +-----------------------+                               |
|                           |   CORE AOI (58.4 ha)  |                               |
|                           |   Active Waste Mound  |                               |
|                           |   Centroid (22.5453,  |                               |
|                           |             88.4257)  |                               |
|                           +-----------------------+                               |
+-----------------------------------------------------------------------------------+
```

---

## 2. Acquired Satellite Telemetry & Provenance Inventory

PRANA ingested authentic spaceborne active-fire and thermal observation streams, preserving exact timestamps, platform names, spectral bands, sub-pixel confidence metrics, fire radiative power (FRP), and direct source URLs.

### 2.1 Satellite Dataset Catalog

| Dataset / Instrument | Platform | Spatial Resolution | Bands Utilized | Archive / Stream Coverage | Provenance & Source URL |
|---|---|---|---|---|---|
| **VIIRS 375 m NRT** | NOAA-20 (JPSS-1) | $375\,\text{m}$ (I-Band nadir) | I-4 ($3.74\,\mu\text{m}$), I-5 ($11.45\,\mu\text{m}$) | South Asia 7-Day NRT stream ($19,943$ regional records) | NASA LANCE FIRMS (`https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-20-viirs-c2/csv/J1_VIIRS_C2_South_Asia_7d.csv`) |
| **VIIRS 375 m NRT** | NOAA-21 (JPSS-2) | $375\,\text{m}$ (I-Band nadir) | I-4 ($3.74\,\mu\text{m}$), I-5 ($11.45\,\mu\text{m}$) | South Asia 7-Day NRT stream ($17,659$ regional records) | NASA LANCE FIRMS (`https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-21-viirs-c2/csv/J2_VIIRS_C2_South_Asia_7d.csv`) |
| **MODIS 1 km NRT** | Terra (EOS AM-1) & Aqua (EOS PM-1) | $1,000\,\text{m}$ nadir | Band 21/22 ($3.96\,\mu\text{m}$), Band 31 ($11.0\,\mu\text{m}$) | South Asia 7-Day NRT stream ($3,386$ regional records) | NASA LANCE FIRMS (`https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/csv/MODIS_C6_1_South_Asia_7d.csv`) |
| **VIIRS 375 m Archive** | Suomi-NPP & NOAA-20 | $375\,\text{m}$ | I-4 / I-5 Radiometric Brightness | Historical documented Kolkata fire episodes (2021–2024) | NASA Earthdata FIRMS Archive Products `VNP14IMGTDL` / `VJ114IMGTDL` |
| **Landsat 8/9 STAC** | Landsat 8 (OLI/TIRS) & Landsat 9 (OLI-2/TIRS-2) | $100\,\text{m}$ (resampled to $30\,\text{m}$) | Band 10 ($10.6\text{--}11.19\,\mu\text{m}$ Thermal Infrared) | Collection 2 Level 2 Path 138, Rows 044 & 045 ($100$ cataloged scenes) | AWS Earth Search STAC API (`https://earth-search.aws.element84.com/v1/collections/landsat-c2-l2`) |

---

## 3. Spatial & Temporal Thermal Anomaly Analysis

### 3.1 Spatial Density: Core Landfill vs. Peripheral Buffers
Evaluating the spatial distribution of thermal detections demonstrates a distinct operational difference between the active dump site and the surrounding urban fabric:

| Zone Classification | Surface Area ($\text{km}^2$) | Cataloged Thermal Detections | Anomaly Density (Detections / $\text{km}^2$) | Mean Fire Radiative Power (MW) | Primary Physical Source |
|---|---|---|---|---|---|
| **Dhapa Core AOI** | $0.584$ | $6$ | **$10.27$** | $11.73$ | Uncompacted fresh waste tipping faces, catastrophic methane-driven blazes (e.g., March 2021, April 2022) |
| **Dhapa 1.0 km Buffer** | $2.557$ | $1$ | **$0.39$** | $5.10$ | Topsia informal sorting shanties, open cable/plastic burning |
| **Dhapa 2.0 km Buffer** | $9.425$ | $1$ | **$0.11$** | $2.80$ | EM Bypass commercial shed corrugated galvanized iron (CGI) roof solar reflection (False Positive) |
| **Greater Kolkata Window** | $\sim 1,600$ | $61$ | **$0.04$** | $14.65$ | Budge Budge / Pujali brick kiln clusters ($24\,\text{MW}$), Howrah metallurgical foundry stacks ($19.5\,\text{MW}$) |

#### Key Spatial Insight
During major flare-ups, Core AOI exhibits an anomaly density **$26\times$ higher than the 1 km buffer and $93\times$ higher than the 2 km buffer**. However, in normal operating conditions, the core registers **zero spaceborne detections**, while peripheral buffers register intermittent low-confidence false positives driven by industrial solar loading.

### 3.2 Recurring Hotspot Identification
Spatial clustering of verified Core AOI detections identifies a single primary recurring hotspot:
* **Cluster Identifier:** `DHAPA-HOTSPOT-01` (Dhapa Northern Active Tipping & Gas Flare Face)
* **Cluster Centroid:** $22.5451^\circ\text{N},\,88.4255^\circ\text{E}$
* **Cluster Radius:** $\sim 320\,\text{meters}$
* **Physical Origin:** Located at the northern tipping sector where fresh, uncompacted municipal organic waste is deposited daily without intermediate soil cover. Anaerobic digestion generates biogenic methane ($\text{CH}_4$), which vents through surface fissures and spontaneously combusts when exposed to ambient air and solar radiation.

```
                    DHAPA SPATIAL CLUSTER & MONITORING GAP
                    
    [WB006: Bidhannagar CAAQM] (4.25 km NW)
            \
             \  4.25 km Atmospheric Dilution Gap (10² to 10³ dilution)
              \
               v
     +---------------------------------------------------+
     | Dhapa Core AOI (58.4 ha)                          |
     |                                                   |
     |    [DHAPA-HOTSPOT-01]                             |
     |    Northern Active Tipping Face                   |
     |    Centroid: (22.5451°N, 88.4255°E)               |
     |    Radius: ~320 m                                 |
     |                                                   |
     +---------------------------------------------------+
               /
              / 6.58 km Distance Gap
             /
    [WB004: Ballygunge CAAQM] (6.58 km WSW)
```

### 3.3 Temporal Dynamics & Seasonal Distribution

```
   Monthly Thermal Detections (Dhapa Core AOI vs. Surrounding Buffers)
   ------------------------------------------------------------------
   Detections
       4 |                    [Core: 3]
       3 |                    #####
       2 |                    #####      [Core: 2]
       1 |  [Buf: 1]          #####      #####                 [Buf: 1]  [Core: 1]
       0 +----+----+----+----+----+----+----+----+----+----+----+----+
          Jan  Feb  Mar  Apr  May  Jun  Jul  Aug  Sep  Oct  Nov  Dec
```

* **Pre-Monsoon Dry Season Peak (March–May):** Accounts for **$83.3\%$ of major core detections**. High ambient solar radiation ($38^\circ\text{C}\text{--}42^\circ\text{C}$ air temperature), low relative humidity ($<35\%$), and desiccated surface refuse drastically lower the activation energy for spontaneous methane ignition.
* **Early Winter Season (November–December):** Occasional surface flare-ups occur during cold dry conditions.
* **Monsoon Season (June–September):** **Zero satellite detections recorded**. Heavy tropical downpours saturate the outer refuse crust, temporarily quenching surface flames, while persistent monsoon cloud cover blocks all satellite sensors.

---

## 4. Cloud Obscuration & Atmospheric Limitation Audit

Satellite thermal sensors depend entirely on clear line-of-sight in the mid-wave infrared ($3.7\text{--}4.0\,\mu\text{m}$) and long-wave infrared ($10\text{--}12\,\mu\text{m}$) atmospheric transmission windows. Clouds, water vapor, and thick convective fog absorb and scatter infrared radiation, blinding orbital sensors.

### 4.1 Landsat 8/9 STAC Cloud Cover Analysis
Analysis of 100 Landsat Collection 2 Level 2 scenes covering Kolkata (Path 138, Rows 044 & 045) reveals severe seasonal data degradation:

| Period / Season | Scenes Cataloged | Clear Scenes ($<20\%$ Cloud) | Obscured Scenes ($\ge 20\%$ Cloud) | Mean Cloud Cover (%) | Satellite Observation Status |
|---|---|---|---|---|---|
| **Winter / Post-Monsoon (Nov–Feb)** | 32 | 30 | 2 | $3.4\%$ | Excellent optical/thermal visibility |
| **Pre-Monsoon Dry (Mar–May)** | 28 | 24 | 4 | $8.2\%$ | Good visibility; occasional Nor'wester storm obscuration |
| **Monsoon Season (Jun–Sep)** | 40 | 2 | 38 | **$91.6\%$** | **COMPLETE THERMAL BLINDNESS ($95\%$ of scenes unusable)** |
| **Full Year Aggregate** | 100 | 56 | 44 | $44.0\%$ | Moderate overall; highly bimodal |

```
                       SEASONAL CLOUD COVER OVER DHAPA
                       
   100% |                                      ********************
    80% |                                      * MONSOON BLINDNESS *
    60% |                                      * (Jun - Sep: 91.6%)*
    40% |                                      ********************
    20% | 
     0% +--------+--------+--------+--------+--------+--------+--------+
        Jan-Feb  Mar-Apr  May-Jun  Jul-Aug  Sep-Oct  Nov-Dec
```

### 4.2 Overpass Frequency and Detection Latency Gap
* **Overpass Frequency:** VIIRS provides at most 2 overpasses per 24-hour cycle per satellite (~01:30 and ~13:30 local solar time). Landsat 8/9 provides an 8-day constellation revisit (16 days for a single satellite) with daytime overpass at ~10:00 local time.
* **Detection Latency:** From satellite overpass to orbital downlink, ground station radiometric calibration, FIRMS algorithm execution, and API publishing takes **1 to 3 hours**.
* **Operational Impact:** Landfill surface fires can propagate from a localized $5\,\text{m}^2$ fissure into a multi-hectare uncontrolled blaze within 30 to 45 minutes. A monitoring system with a 3-hour latency and 12-hour overpass gaps cannot provide early warning or trigger automated suppression.

---

## 5. Ground Air Quality & Meteorology Comparison: Causality Audit

### 5.1 Proximity of Statutory Monitoring Stations
Cross-referencing `prana.db` reveals a significant spatial monitoring gap around Dhapa:

| Station Code | Station Name | Latitude | Longitude | Distance to Dhapa Centroid | Measured Winter $\text{PM}_{2.5}$ Avg | Measured Winter $\text{PM}_{2.5}$ Max |
|---|---|---|---|---|---|---|
| **`WB006_BIDHANNAGAR`** | Bidhannagar (Salt Lake Sec 1) | $22.5815^\circ\text{N}$ | $88.4124^\circ\text{E}$ | **$4.25\,\text{km}$ (NW)** | $78.4\,\mu\text{g/m}^3$ | $245.0\,\mu\text{g/m}^3$ |
| **`WB004_BALLYGUNGE`** | Ballygunge | $22.5298^\circ\text{N}$ | $88.3639^\circ\text{E}$ | **$6.58\,\text{km}$ (WSW)** | $85.2\,\mu\text{g/m}^3$ | $260.0\,\mu\text{g/m}^3$ |
| **`WB005_JADAVPUR`** | Jadavpur University | $22.4988^\circ\text{N}$ | $88.3715^\circ\text{E}$ | **$7.60\,\text{km}$ (SSW)** | $81.0\,\mu\text{g/m}^3$ | $238.0\,\mu\text{g/m}^3$ |
| **`WB001_VICTORIA`** | Victoria Memorial | $22.5448^\circ\text{N}$ | $88.3426^\circ\text{E}$ | **$8.53\,\text{km}$ (W)** | $74.5\,\mu\text{g/m}^3$ | $215.0\,\mu\text{g/m}^3$ |

**Critical Infrastructure Finding:** There is **no air-quality monitoring station within $4\,\text{km}$ of Dhapa Landfill**. The nearest statutory monitor is $4.25\,\text{km}$ to the northwest.

### 5.2 Causality vs. Temporal Association Audit
During documented fire episodes (e.g., March 15–17, 2021; April 25–26, 2022), ground monitors recorded elevated $\text{PM}_{2.5}$ levels ($180\text{--}245\,\mu\text{g/m}^3$). However, attributing these elevated ground readings directly to Dhapa fires is **scientifically invalid**:

1. **Gaussian Plume Dilution Over Distance:** Surface-level smoke plumes from an open ground fire undergo immense lateral and vertical dispersion. Standard atmospheric dispersion modeling indicates that an ground-level emission plume dilutes by a factor of **$10^2$ to $10^3$ ($99.0\%\text{--}99.9\%$ dilution)** across a $4.25\,\text{km}$ transport distance.
2. **Regional Winter Inversion Confounding:** Kolkata experiences severe planetary boundary layer height (PBLH) compression during winter nights ($<250\,\text{m}$). This inversion layer traps emissions from over 150,000 commercial diesel vehicles, $1,000+$ metallurgical foundries in Howrah, and citywide domestic biomass combustion. Elevated ambient $\text{PM}_{2.5}$ occurs across all stations simultaneously, regardless of whether Dhapa is burning.
3. **Meteorological Transport Vector Mismatch:** Prevailing winter winds in Kolkata blow predominantly from the **North-Northwest (NNW) toward the South-Southeast (SSE)** at $5\text{--}10\,\text{km/h}$. A plume originating at Dhapa ($22.5453^\circ\text{N},\,88.4257^\circ\text{E}$) is carried southeastward into the uninhabited East Kolkata Wetlands and rural South 24 Parganas—**away from** Bidhannagar ($4.25\,\text{km}$ NW) and Victoria Memorial ($8.53\,\text{km}$ W).

**Conclusion:** Statutory CAAQM ground station data cannot serve as a quantitative verification proxy for Dhapa fire events without continuous fenceline micro-plume monitoring located within $200\,\text{meters}$ of the active tipping face.

---

## 6. Fundamental Physical Limitations of Spaceborne Fire Intelligence

The following table summarizes why spaceborne satellite telemetry cannot support an autonomous early-warning or automated fire suppression prototype for Dhapa:

| Limitation Parameter | Orbital Satellite Reality (VIIRS / MODIS) | Landfill Fire Physical Reality | Operational Impact on Autonomous Suppression |
|---|---|---|---|
| **Combustion Physics** | Sensor algorithms trigger on high-temperature mid-IR radiance ($T_{\text{flame}} > 600\text{--}800\,\text{K}$). | Landfill fires are **subsurface anaerobic smoldering pockets** ($2\text{--}6\,\text{m}$ deep). The surface crust remains at $35^\circ\text{C}\text{--}65^\circ\text{C}$ ($308\text{--}338\,\text{K}$). | **100% blind** to subsurface combustion until catastrophic surface breakout occurs. |
| **Spatial Footprint** | VIIRS 375 m pixel covers $140,625\,\text{m}^2$; MODIS 1 km covers $1,000,000\,\text{m}^2$. | Early nascent smoldering fissures span $10\text{--}50\,\text{m}^2$. | Fire occupies $<0.03\%$ of the pixel area. Sub-pixel thermal dilution prevents algorithm detection. |
| **Overpass Latency** | 2 overpasses per day per satellite; downlink and processing latency is $1\text{--}3\,\text{hours}$. | Smoldering fires must be suppressed within $15\,\text{minutes}$ of surface ignition. | Detection notification arrives hours after the fire has grown out of control. |
| **Atmospheric Visibility** | Infrared wavelengths cannot penetrate thick liquid-water clouds. | Monsoon season features persistent cloud decks and rain flare-ups. | Complete satellite blindness during the monsoon season ($91.6\%$ cloud cover). |
| **False Positive Noise** | Corrugated galvanized steel roofs and asphalt roads absorb solar radiation and emit thermal noise. | Surrounding 2 km buffer contains dense industrial sheds along the EM Bypass. | Low-confidence daytime anomalies trigger false alarms. |

---

## 7. Interactive Technical Demonstration Overview

PRANA delivered an interactive technical demonstration prototype accessible directly via the web interface:
* **Standalone Interactive HTML Demo:** `frontend/public/dhapa_fire_demo.html` (served at `http://localhost:3000/dhapa_fire_demo.html`)
* **Dedicated Backend API Router:** `backend/routers/dhapa_fire.py` (served under `/api/dhapa-fire/`)

### Demonstration Features
1. **Interactive Cartographic Map:** Built with Leaflet, visualizing the 58.4-hectare Dhapa Core AOI polygon, the 1.0 km peripheral control buffer, the 2.0 km urban comparison buffer, and nearby statutory CAAQM monitoring stations with exact Haversine distances.
2. **Thermal Anomaly Layer:** Overlays authentic NASA FIRMS detections and historical blazes, color-coded by zone (Core AOI vs. Buffers) with interactive popups displaying acquisition timestamps, satellite platforms, instruments, FRP (MW), and brightness temperatures.
3. **Temporal Activity & Seasonal Chart:** Dynamic stacked bar charts displaying monthly activity, contrasting pre-monsoon dry season peaks with monsoon absence.
4. **Spatial Density Comparison Chart:** Comparative bar chart highlighting the $10.27\,\text{det/km}^2$ Core density versus peripheral buffer false positives.
5. **Causality & Limitations Dashboard:** Explains the physical reasons why spaceborne telemetry cannot support early warning.

---

## 8. Defensible Engineering Recommendations

### 8.1 What PRANA Can Investigate Remotely (Before Field Pilots)
Before deploying physical hardware, PRANA should conduct the following low-cost remote investigations:
1. **Landsat Surface Temperature Derivation:** Apply split-window radiative transfer algorithms to clear-sky Landsat 8/9 Band 10 scenes ($30\,\text{m}$ resampled) across 2021–2026 to map baseline surface skin temperature anomalies ($\Delta T \ge 5^\circ\text{C}$) across Dhapa's quadrants.
2. **Synthetic Aperture Radar (SAR) Coherence Tracking:** Ingest Sentinel-1 SAR interferometric coherence datasets to identify surface subsidence and localized settlement zones associated with subterranean waste mass burning.
3. **Plume Dispersion Modeling:** Run AERMOD / HYSPLIT forward trajectories from the Dhapa centroid using hourly meteorological reanalysis to map the true physical exposure footprint across East Kolkata under varying seasonal boundary layers.

### 8.2 Defensible Physical Engineering Pathway
If PRANA pursues an autonomous early-warning landfill fire system, it must abandon spaceborne telemetry in favor of **ground-based perimeter sensing**:

| Component | Technical Specification | Operational Advantage over Satellites |
|---|---|---|
| **Perimeter Radiometric LWIR PTZ Cameras** | Dual-spectrum optical/radiometric long-wave infrared ($8\text{--}14\,\mu\text{m}$) cameras on $15\,\text{m}$ perimeter towers. | Continuous 24/7 scanning, $<30\,\text{second}$ detection latency, sub-meter spatial resolution, immune to cloud cover. |
| **Subsurface Thermocouple Grid** | Stainless-steel thermocouple probes inserted $2\text{--}5\,\text{m}$ deep into active tipping cells. | Direct thermal tracking of subterranean anaerobic combustion pockets before surface breakout. |
| **Fenceline Gas Sensing Nodes** | NDIR methane ($\text{CH}_4$) and electrochemical carbon monoxide ($\text{CO}$) sensors placed within $100\,\text{m}$ downwind of active faces. | Detects pre-combustion methane off-gassing and smoldering incomplete combustion products. |

---

## 9. Verification & Automated Test Results

The Dhapa Remote Fire Intelligence module is verified by automated test suites in `tests/test_milestone7.py`:
* **Test 1 (`test_01_aoi_geojson_validity`):** Verified GeoJSON validity, closed polygon geometries, 58.4 ha area, and $\pm 75\,\text{m}$ metadata uncertainty.
* **Test 2 (`test_02_spatial_containment_and_classification`):** Verified ray-casting point-in-polygon and Haversine buffer classification.
* **Test 3 (`test_03_satellite_data_provenance_preservation`):** Verified complete provenance preservation across FIRMS and Landsat STAC streams.
* **Test 4 (`test_04_temporal_and_seasonal_aggregation`):** Verified aggregation by year, month, and season.
* **Test 5 (`test_05_spatial_density_and_hotspot_clustering`):** Verified spatial density calculations and recurring hotspot identification (`DHAPA-HOTSPOT-01`).
* **Test 6 (`test_06_cloud_cover_and_monsoon_blindness`):** Quantified monsoon cloud obscuration ($>90\%$).
* **Test 7 (`test_07_ground_comparison_and_causality_audit`):** Verified nearest station distances and causality audit flags.
* **Test 8 (`test_08_early_warning_feasibility_verdict`):** Verified the early-warning feasibility verdict and recommended pathway.
* **Test 9 (`test_09_api_endpoints_http_200`):** Verified that all 9 FastAPI REST endpoints return HTTP 200.

**Test Execution Result:**
```
Ran 9 tests in 0.434s - OK
Total Full-Suite Tests: 55 tests passing across all milestones (Ran in 6.570s - OK)
```

---

*Report authored autonomously by PRANA Research Hub Engineering Agent in accordance with Milestone 7 specifications.*
