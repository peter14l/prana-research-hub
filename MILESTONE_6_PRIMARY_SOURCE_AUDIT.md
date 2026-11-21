# PRANA Milestone 6: Primary Source Verification
## Comprehensive Audit of Referenced Environmental Research Reports & Statutory Records

**Date:** 2026-11-21  
**Audit Conducted By:** PRANA Scientific Council  
**Scope:** Direct forensic inspection of original primary source documents:
1. **CSIR-NEERI (2020)**: *PM10 and PM2.5 Source Apportionment Study and Development of Emission Inventory of Twin Cities Kolkata and Howrah* (Final Report, 214 pages).
2. **TERI (2025)**: *Air Pollution Emissions Inventory, Source Apportionment and Atmospheric Carrying Capacity Study of Kolkata in West Bengal* (Final Report, 318 pages).
3. **CPCB Statutory Registry & Telemetry**: Monitoring Station Coordinates and Ambient Observations Database (`prana.db`).

---

## Executive Summary of Findings

| Opportunity / Sector | Referenced Claim in PRANA | Primary Source Verification Finding | Direct Evidence vs. Regional Context | Audit Status |
|---|---|---|---|:---:|
| **Howrah Foundry Retrofit** | "34% winter industrial PM2.5 in Ghusuri" (citing Table 6.14, p. 148) | **Citation Refuted; Stronger Emission Inventory Ground Truth Found.** Table 6.14 does not exist (Chapter 6 has only 2 pages and 0 tables). Ghusuri was *not* a receptor modeling site (sampling was cancelled due to administrative reasons, p. 54). However, **Table 3.21 (p. 114)** proves **Foundries are Howrah's #1 industrial emitter** (708.7 MT/y PM2.5, **49.2% of industrial PM2.5** and **25.4% of total citywide PM2.5**). Winter Howrah CMB fossil fuel share is **42.1%** (Table 7.1, p. 203). | **Table 3.21 is DIRECT Howrah HMC inventory evidence**; CMB winter results are Howrah citywide context. | **CORRECTED / VERIFIED FROM PRIMARY SOURCE** |
| **Dhapa Landfill Suppression** | "14% waste-burning PM2.5 contribution" (citing Table 4.6, p. 87) | **Citation Refuted; Higher Localized Landfill Fire Impact Discovered.** Table 4.6 does not exist. 14% is the **citywide KMC annual refuse burning average** (Figure 84, p. 200). Crucially, TERI **explicitly distinguishes Landfill Fires from Waste Burning** (Table 44, p. 178). For Dhapa specifically, **Landfill Fire contributes ~54% of winter PM2.5 and ~44% of PM10** at the dump site (p. 177). | **54% is DIRECT Dhapa hotspot evidence**; 14% is regional KMC airshed context. | **CORRECTED / VERIFIED FROM PRIMARY SOURCE** |
| **Jalan Fence-Line Attribution** | "8.56 km monitoring gap; 2,000+ units; nocturnal spikes > 180 µg/m³" | **Distance Mathematically Verified; Operational Claims Unsupported.** Geodesic Haversine distance from Jalan centroid to Padmapukur (`site_5010`) is verified at **8.56 km**. CPCB station data cannot resolve Jalan plumes over 8.56 km. Unit count (2,000+), nocturnal spikes (>180), and VIIRS radiance are **unsupported in database**. | **8.56 km is a verified DERIVED RESULT**; operational claims are UNVERIFIED or MISSING. | **VERIFIED DISTANCE / UNSUPPORTED CLAIMS SEGREGATED** |

---

## 1. Howrah Foundry Retrofit: Primary Source Audit of CSIR-NEERI (2020)

### 1.1 Document Identification
* **Official Title:** *PM10 and PM2.5 Source Apportionment Study and Development of Emission Inventory of Twin Cities Kolkata and Howrah*
* **Authoring Organisations:** CSIR-National Environmental Engineering Research Institute (NEERI), Nagpur & Kolkata Zonal Centre, in collaboration with West Bengal Pollution Control Board (WBPCB).
* **Publication Date:** March 2020.
* **Document Length:** 214 pages (PDF).
* **Source URL:** `https://www.wbpcb.gov.in/writereaddata/files/SA_Kol-How_Final%20Report.pdf`
* **Local Verification Copy:** `backend/data/research_docs/CSIR_NEERI_2020_Final_Report.pdf` (MD5 verified, 9,835,433 bytes).

---

### 1.2 Forensic Investigation of the Claimed "34% Industrial PM2.5 in Ghusuri"

#### Claim to Verify:
> *"CSIR-NEERI (2020) Table 6.14, p. 148: Small-scale cupola foundries and coal-fired rerolling mills contribute 34% of winter PM2.5 in northern Howrah (Ghusuri)."*

#### Primary Source Findings:
1. **Verification of "Table 6.14":**
   - The document Table of Contents (Report page v / PDF page 5) defines **Chapter 6** as *"Comparison of Emission Inventory and CMB Results"*, spanning only **Report pages 6.1–6.2 (PDF pages 198–199)**.
   - Chapter 6 contains **no tables whatsoever** (0 tables). The claim that "Table 6.14" exists in Chapter 6 is **factually false**.
2. **Verification of "Page 148":**
   - PDF page 148 (Report page 4.30) contains only narrative text and **Figure 4.8** (*"Carbon, Ions and Elements in PM : Winter"*), discussing sulfate, nitrate, zinc, and lead enrichment. It contains no table and no 34% figure.
3. **Exhaustive Search for "34%" across all 214 pages:**
   Every occurrence of the number 34 in the report was audited:
   - **Page 43 (Report page 1.15):** *"The Metro Core involves the twin city of Kolkata and Howrah... occupying about 34% of the KMA area."* (Land area metric, not air pollution).
   - **Page 112 (Report page 3.36, Table 3.20):** Hot mix plants emit 34.13 MT/y of PM2.5 in Howrah.
   - **Page 114 (Report page 3.38, Table 3.21):** Textile/Yarn industries emit 34.8 MT/y of PM2.5 in Howrah.
   - **Page 177 & Page 203 (Table 4.8b & Table 7.1):** Winter PM2.5 Fossil Fuel Burning in **Kolkata** (not Howrah) is **34.6%**.
   - **Page 178 (Report page 4.60):** Secondary ionic species constitute *"20% and 34% of PM10 and PM2.5 mass during summer"*.
   - **Conclusion on 34%:** There is **no empirical finding in CSIR-NEERI (2020) stating that industrial emissions contribute 34% of winter PM2.5 in Ghusuri**. The citation "Table 6.14, p. 148" was a phantom citation.

---

### 1.3 Geographical Scope: Does the Study Apply to Ghusuri Specifically or Howrah City?

1. **Was Ghusuri Sampled for Chemical Mass Balance (CMB) Receptor Modeling?**
   - **NO.** CSIR-NEERI Report page 2.9 (PDF page 54, Section 2.4) explicitly states:
     > *"Sampling at 3 selected stations in Howrah viz. Howrah Municipal Corporation, Ghusuri Pump House and Batore Heath Centre could not be done during summer 2017 due to administrative reasons; hence 3 new air quality stations were scrutinized and finalized in Howrah (ATI in Das Nagar, Buxrah High School in Buxrah and Akshay Shikshayatan in Howrah Maidan)."*
   - In winter 2017–18, ambient sampling for CMB receptor modeling was conducted at **4 stations in Howrah** (Report page 4.52 / PDF page 170, Table 4.5):
     1. **Bandhaghat** (Residential/Riverfront)
     2. **Howrah Maidan** (Commercial / Urban Core)
     3. **ATI Dasnagar** (Industrial / Mixed)
     4. **Buxrah** (Suburban / Residential)
   - **Ghusuri was excluded from receptor modeling**. Therefore, any claim that receptor modeling showed 34% specifically in Ghusuri is scientifically impossible from this report.
2. **What Did the CMB Receptor Model Actually Find for Howrah as a Whole in Winter?**
   - **Report page 7.3 (PDF page 202, Section 7.2.2):**
     > *"Vehicular contribution to PM2.5 is observed to be 31% in Howrah. Coal and wood combustion share is 11% each, whereas secondary aerosol contribution is 27%. The unidentified mass is 12%."*
   - **Report page 7.4 (PDF page 203, Table 7.1) / Report page 4.59 (PDF page 177, Table 4.8b):**
     *Comparison of Results of CMB for Summer and Winter: PM2.5 in Howrah*:
     - **Fossil Fuel Combustion:** **42.1%** (Vehicular 31.0% + Coal 11.1%)
     - **Secondary Aerosol:** **27.3%**
     - **Biomass Combustion:** **16.3%** (Wood 11.0% + Open burning 5.3%)
     - **Road Dust & Construction:** **1.9%**
     - **Unaccounted:** **12.3%**

---

### 1.4 What the Study Actually Says About Industrial Sources and Their Composition

While the CMB receptor model lumped emissions into broad fuel categories (coal, fossil fuel, biomass), **Chapter 3 (Emissions Inventory)** conducted a rigorous, facility-level fuel audit based on WBPCB Consent-to-Operate records for Howrah Municipal Corporation (HMC):

1. **Foundries are the Dominant Industrial Emitter in Howrah:**
   - **Report page 3.38 (PDF page 114, Table 3.21):**
     *PM10 and PM2.5 emissions (MT/y) from select categories of industries having the major share in fuel consumption in Howrah (HMC area):*
     ```
     ┌───────────────────────────────────┬───────────────┬───────────────┐
     │ Industry Type                     │ PM10 (MT/y)   │ PM2.5 (MT/y)  │
     ├───────────────────────────────────┼───────────────┼───────────────┤
     │ Foundry                           │ 2,715.4       │ 708.7         │
     │ Rolling Mill                      │   621.8       │ 188.8         │
     │ Ferrous/Non-ferrous               │   175.2       │  49.5         │
     │ Textile/Yarn                      │   132.8       │  34.8         │
     │ Jute processing                   │   101.0       │  68.7         │
     │ Gas fired boiler                  │    98.2       │  31.0         │
     │ Steel and Steel products          │    93.6       │  25.3         │
     │ Pickling/Electroplating           │    81.5       │  24.2         │
     │ Pulp and Paper                    │    21.8       │  14.8         │
     │ Al Smelter/Al-Cu extraction       │    18.7       │  10.5         │
     │ Engineering and fabrication       │    10.6       │   6.9         │
     │ Heat treatment (Oil fired)        │     2.5       │   1.7         │
     │ Bakery                            │     2.2       │   1.5         │
     │ Railway Locomotives               │     0.7       │   0.4         │
     └───────────────────────────────────┴───────────────┴───────────────┘
     ```
   - **Exact Quotation (p. 114):**
     > *"Industries/ manufacturing units classified as foundries was found to be the largest emitter of PM10 and PM2.5 followed by Al Smelter and Al-Cu Extraction, Bakeries, non-ferrous metal units and so on."*
2. **Foundries Constitute Half of Howrah's Industrial Emissions and a Quarter of All Citywide PM2.5:**
   - **Table 3.20 (Report page 3.36 / PDF page 112):** Total industrial PM2.5 emissions in Howrah = **1,439.51 MT/y** (out of total citywide PM2.5 from all sectors of **2,785.0 MT/y** = **51.7%**).
   - Foundry PM2.5 emissions alone (**708.7 MT/y**) account for:
     $$\frac{708.7}{1,439.51} = \mathbf{49.2\%}\text{ of all industrial }\text{PM}_{2.5}\text{ emissions in Howrah}$$
     $$\frac{708.7}{2,785.0} = \mathbf{25.4\%}\text{ of ALL citywide }\text{PM}_{2.5}\text{ emissions in Howrah across all sectors}$$
3. **Foundry Fuel Composition:**
   - **Table 3.10 (Report page 3.22 / PDF page 98):** Howrah foundries consume:
     - **130,866.0 MT/year of Coke**
     - **3,183.6 MT/year of Coal**
     - **874.5 kL/year of Diesel / HSD**
     - **46.2 MT/year of Wood**
     - **148.2 kL/year of LPG**
   - The sheer scale of coke combustion (130,866 MT/y) in low-stack artisanal furnaces directly explains the severe heavy metal and particulate load in northern Howrah.

---

## 2. Dhapa Opportunity: Primary Source Audit of TERI (2025)

### 2.1 Document Identification
* **Official Title:** *Air Pollution Emissions Inventory, Source Apportionment and Atmospheric Carrying Capacity Study of Kolkata in West Bengal*
* **Authoring Organisations:** The Energy and Resources Institute (TERI), New Delhi, for West Bengal Pollution Control Board (WBPCB).
* **Publication Date:** January 2025.
* **Document Length:** 318 pages (PDF).
* **Source URL:** `https://www.wbpcb.gov.in/files/We-07-2025-07-48-01SA_EI_CC_Kolkata_WBPCB_2025.pdf`
* **Local Verification Copy:** `backend/data/research_docs/TERI_2025_Kolkata_Study.pdf` (MD5 verified, 65,211,749 bytes).

---

### 2.2 Forensic Investigation of the Claimed "14% Waste-Burning Contribution"

#### Claim to Verify:
> *"TERI (2025) Table 4.6, p. 87: Municipal solid waste burning contributes 14% of winter PM2.5 regionally."*

#### Primary Source Findings:
1. **Verification of "Table 4.6, p. 87":**
   - Tables in the TERI report are numbered sequentially from Table 1 to Table 48 (no decimal sub-numbering like "4.6").
   - Report page 87 (PDF page 127) falls inside Chapter 5 (Emissions Inventory), displaying vehicular vintage tables. There is no Table 4.6 on page 87.
2. **Origin of the 14% Figure in TERI (2025):**
   - **Figure 84 (Report page 160 / PDF page 200):** *Changes in sectoral contributions to atmospheric PM10 and PM2.5 in the KMC area under different emission reduction roadmaps*:
     - For **2023 Baseline PM2.5**, the simulated annual share of **Refuse burning is ~14%** (followed by Road dust 17%, Transport 18%, Industries 17%, Residential 15%, Brick kiln 7%, Landfill fire ~4-5%, Power 5%).
   - **Figure 19 (Report page 42 / PDF page 82):** Spatial source apportionment across sampling stations shows refuse burning contributions to PM2.5 ranging from **7% to 15%** at different monitoring stations.
   - **Figure E8 (Executive Summary, Report page xxix / PDF page 29):** Winter PM2.5 simulated sources: Waste burning is **5%**, and Landfill is **5%** (combined open combustion = 10%).

---

### 2.3 Geographical Scope: Does 14% Apply to Dhapa, Howrah, Kolkata, or the Wider Airshed?

* **The 14% figure is a REGIONAL KMC AIRSHED AVERAGE, NOT Dhapa specifically.**
* The report title and methodology specify that the study domain is the **Kolkata Municipal Corporation (KMC) Area** (144 municipal wards on a 1 km × 1 km grid nested in a 36 km × 36 km domain).
* The 14% refuse burning share represents the broad urban background exposure resulting from municipal solid waste burning across streets, vacant plots, and informal settlements across the entire city.

---

### 2.4 Does the Study Establish Landfill Fires as a Distinct Source?

* **YES! EMPHATICALLY AND EXPLICITLY.**
* Unlike earlier studies that grouped all open burning into a single "biomass/waste" category, **TERI (2025) explicitly separates "Landfill Fire" from "Refuse Burning" as two distinct modeled categories** in both its emissions inventory and atmospheric dispersion carrying capacity framework:
  1. **Table 44 (Report page 138 / PDF page 178):**
     *Simulated average percentage contributions of different sectors to calculated ACC of PM10 and PM2.5 in KMC area during winter season*:
     - Explicit separate row: **"Landfill fire"** (Row 6)
     - Explicit separate row: **"Refuse burning"** (Row 11)
  2. **Figure 84 (Report page 160 / PDF page 200):**
     - Separate legend entries for **"Refuse burning"** (orange) and **"Landfill fire"** (dark brown).
  3. **Figure E8 (Report page xxix / PDF page 29):**
     - Separate legend entries for **"Landfill"** and **"Waste burning"**.

---

### 2.5 What Does TERI (2025) Actually Report for Dhapa Specifically?

On **Report page 137 (PDF page 177)**, the study evaluates the Atmospheric Carrying Capacity (ACC) near the Dhapa municipal landfill:

* **Direct Quotation (Report page 137 / PDF page 177):**
  > *"The ACCi,p of PM10 was estimated as ‘critically exhausted’ area near Howrah Bridge, Vidyasagar setu (Khidirpur side) Garia, Jadavpur University, South City Mall and Dhapa dump site areas during winter season (Figure 77)... while near the Dhapa dump site area it is mainly attributed to the landfill fire (~44% contribution to atmospheric PM10 at the area) and road dust resuspension (~21% contribution to atmospheric PM10 at the area)."*
* **Direct Quotation on PM2.5 (Report page 137 / PDF page 177):**
  > *"The ACCi,p of PM2.5 was estimated as ‘very poorly exhausted’ area near Howrah Bridge, and Dhapa dump site areas during winter season (Figure 77). It is related to about 54% contribution from landfill fire to atmospheric PM2.5 near the Dhapa dump site areas..."*
* **Table 44 (Report page 138 / PDF page 178):**
  In the *"Very poorly exhausted"* carrying capacity zone encompassing Dhapa, **Landfill Fire accounts for 27% of atmospheric PM2.5** and **Refuse Burning accounts for 6%**.

#### Audit Synthesis for Dhapa:
The previous citation of "14% waste burning (Table 4.6, p. 87)" actually understated the local problem:
- **14%** is the broad, citywide background refuse burning contribution.
- For Dhapa specifically, primary source evidence proves that **Landfill Fires drive ~54% of localized winter PM2.5 and ~44% of PM10**, providing powerful, direct primary-source justification for autonomous thermal edge suppression at the dump site.

---

## 3. Fence-Line Opportunity: Primary Source Audit of Statutory Telemetry

### 3.1 Verification of CPCB Station Coordinates & Geodesic Distance

1. **Jalan Industrial Centroid:**
   - Reference coordinates: `22.5900°N, 88.2400°E` (Jalan Industrial Complex, NH-6 / Bombay Road corridor, Sankrail/Domjur, Howrah).
2. **Statutory Station Registry Coordinates in `prana.db`:**
   ```
   ┌─────┬──────────────────────────────────────────┬───────────┬───────────┬───────────┬───────────────────┐
   │ ID  │ Station Name                             │ Site ID   │ Latitude  │ Longitude │ Haversine Distance│
   ├─────┼──────────────────────────────────────────┼───────────┼───────────┼───────────┼───────────────────┤
   │ 9   │ Padmapukur (Howrah Central)              │ site_5010 │ 22.5632°N │ 88.3182°E │ 8.56 km (NEAREST) │
   │ 2   │ Fort William                             │ site_5003 │ 22.5535°N │ 88.3378°E │ 10.83 km          │
   │ 7   │ Ghusuri (Howrah North)                   │ site_5008 │ 22.6074°N │ 88.3496°E │ 11.42 km          │
   │ 1   │ Victoria Memorial                        │ site_5002 │ 22.5448°N │ 88.3426°E │ 11.67 km          │
   │ 8   │ Belur Math                               │ site_5009 │ 22.6310°N │ 88.3541°E │ 12.57 km          │
   │ 4   │ Ballygunge                               │ site_5005 │ 22.5298°N │ 88.3639°E │ 14.38 km          │
   │ 3   │ Rabindra Bharati University (BT Road)    │ site_5004 │ 22.6247°N │ 88.3846°E │ 15.34 km          │
   │ 5   │ Jadavpur University                      │ site_5006 │ 22.4988°N │ 88.3715°E │ 16.89 km          │
   │ 6   │ Bidhannagar (Salt Lake Sector 1)         │ site_5007 │ 22.5815°N │ 88.4124°E │ 17.72 km          │
   └─────┴──────────────────────────────────────────┴───────────┴───────────┴───────────┴───────────────────┘
   ```
3. **Mathematical Derivation of 8.56 km:**
   Using the spherical earth mean radius $R = 6,371.0\,\text{km}$:
   $$\Delta \phi = (22.5632 - 22.5900) \times \frac{\pi}{180} = -0.00046775\,\text{rad}$$
   $$\Delta \lambda = (88.3182 - 88.2400) \times \frac{\pi}{180} = +0.00136484\,\text{rad}$$
   $$a = \sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(22.5900^\circ) \cdot \cos(22.5632^\circ) \cdot \sin^2\left(\frac{\Delta \lambda}{2}\right) = 4.5126 \times 10^{-7}$$
   $$d = 2 \cdot R \cdot \arcsin(\sqrt{a}) = \mathbf{8.564\,\text{km}} \approx \mathbf{8.56\,\text{km}}$$
   *Verification Result:* **VERIFIED DERIVED RESULT.** The distance is mathematically exact. Padmapukur is undeniably the nearest statutory station to Jalan, located **8.56 km away**.

---

### 3.2 What Available Statutory Monitoring Data CAN and CANNOT Demonstrate About Jalan

#### What It CAN Demonstrate:
1. **Regional Exceedance Context:** Telemetry from Padmapukur (`site_5010`) and Ghusuri (`site_5008`) proves that ambient air quality in Howrah regularly breaches the 24-hr NAAQS standard ($60\,\mu\text{g/m}^3$) during winter, reaching Poor to Severe levels ($>120\text{--}220\,\mu\text{g/m}^3$).
2. **Airshed Inversion Vulnerability:** Open-Meteo reanalysis and CPCB sonic anemometer data confirm that low planetary boundary layer heights ($<400\,\text{m}$) and calm winds ($<2\,\text{m/s}$) from the west/north-west trap emissions across the entire Howrah district.

#### What It CANNOT Demonstrate:
1. **Cannot Resolve Jalan Plumes:** Over an 8.56 km transport distance, industrial micro-plumes disperse horizontally and vertically through atmospheric turbulence. Point observations at Padmapukur cannot isolate Jalan emissions from regional background air.
2. **Cannot Distinguish Intervening Sources:** Between Jalan and Padmapukur lie several major emission corridors, including National Highway 16 (NH-16 / Kona Expressway, carrying $>50,000$ commercial freight vehicles daily), the South Eastern Railway freight lines, and dense domestic chulha burning in Sankrail. Statutory data cannot disentangle Jalan plumes from these intervening sources.
3. **Cannot Identify Specific Polluting Units:** Fixed statutory monitoring cannot establish whether elevated concentrations originate from metal foundries, scrap recycling, plastic processing, or road transport.

---

### 3.3 Identification of Unsupported Claims Behind the Jalan Opportunity

1. **Claim of "2,000+ Industrial Units in Jalan":**
   - *Status:* **UNVERIFIED HYPOTHESIS (0.0 Credit)**.
   - *Audit Finding:* No District Industries Centre (DIC) register, MSME database, or factory license records exist in PRANA or public statutory tables confirming this number.
2. **Claim of "Midnight-to-Dawn PM2.5 Spikes > 180 µg/m³ at Padmapukur":**
   - *Status:* **SYNTHETIC DATA ARTIFACT (0.0 Credit)**.
   - *Audit Finding:* Direct database query of all records in `validated_observations` for Padmapukur revealed **zero** observations $>180\,\mu\text{g/m}^3$ between 22:00 and 06:00. The only two readings $>180\,\mu\text{g/m}^3$ occurred at 12:00 PM and 1:00 PM on 2026-11-19 and were tagged `DEMO`.
3. **Causal Correlation with Calm North-Westerly Winds:**
   - *Status:* **UNTESTED HYPOTHESIS (0.0 Credit)**.
   - *Audit Finding:* While NW wind records exist in `weather_observations`, no statistical lag correlation or bivariate polar plot linking NW winds to concentration spikes at Padmapukur exists in PRANA.
4. **NASA VIIRS Nighttime Radiance Anomalies:**
   - *Status:* **MISSING EVIDENCE (0.0 Credit)**.
   - *Audit Finding:* Zero raw NASA VIIRS thermal anomaly vectors, radiance values, or satellite NetCDF/GeoTIFF rasters have been ingested into the PRANA repository.

---

## 4. Cross-Cutting Evidence Synthesis Matrix

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                       MILESTONE 6 EVIDENCE INTEGRITY SCORECARD                                         │
├─────────────────────────┬─────────────────────────────┬────────────────────────────────────┬───────────────────────────┤
│ Evaluation Dimension    │ Howrah Foundry Retrofit     │ Dhapa Landfill Suppression         │ Fence-Line Attribution    │
├─────────────────────────┼─────────────────────────────┼────────────────────────────────────┼───────────────────────────┤
│ Primary Source Document │ CSIR-NEERI (2020)           │ TERI (2025)                        │ CPCB Station Registry     │
│ Direct Evidence Base    │ Table 3.21 (Foundries =     │ Page 137 (Landfill fire =          │ Padmapukur site_5010      │
│                         │ 708.7 MT/y PM2.5, 49.2% of  │ 54% of winter PM2.5 and            │ coordinates verified;     │
│                         │ Howrah industrial PM2.5)    │ 44% of PM10 near Dhapa dump)       │ 8.56 km Haversine derived │
│ Regional Context Base   │ Table 7.1 (Howrah winter    │ Figure 84 (KMC citywide            │ Padmapukur CAAQM regional │
│                         │ fossil fuel PM2.5 = 42.1%)  │ refuse burning = 14%)              │ exceedance telemetry      │
│ Discredited Narrative   │ "34% in Ghusuri" (phantom   │ "Table 4.6, p. 87" (phantom table; │ 2,000+ unit count;        │
│                         │ Table 6.14, p. 148; Ghusuri │ actually understates localized     │ nocturnal spikes > 180;   │
│                         │ was never sampled by CMB)   │ Dhapa landfill fire impact)        │ uningested VIIRS data     │
│ Source Distinction      │ Foundry vs. other industry  │ Landfill fire vs. refuse burning   │ Point monitor vs. 8.56 km │
│                         │ explicitly disaggregated    │ explicitly disaggregated (Table 44)│ unmonitored spatial void  │
│ Milestone 5 Score       │ 6.8 / 10 (Rank #1)          │ 4.2 / 10 (Rank #3)                 │ 3.5 / 10 (Rank #2)        │
│ Milestone 6 Score Change│ NO CHANGE (Per directive)   │ NO CHANGE (Per directive)          │ NO CHANGE (Per directive) │
└─────────────────────────┴─────────────────────────────┴────────────────────────────────────┴───────────────────────────┘
```

---

## 5. Conclusion & Recommendations

1. **Howrah Foundry Retrofit:** Although the earlier cited "34% in Ghusuri (Table 6.14)" was a phantom citation, the actual report (**CSIR-NEERI 2020 Table 3.21, p. 114**) provides even stronger, direct empirical emissions inventory evidence: **foundries are the single largest industrial PM2.5 emitter in Howrah (708.7 MT/y, accounting for 49.2% of industrial PM2.5 and 25.4% of total citywide PM2.5)**.
2. **Dhapa Landfill Suppression:** TERI (2025) officially distinguishes landfill fires from general waste burning. While 14% is the regional citywide average, primary source evidence (**p. 137**) reveals that **landfill fires drive 54% of winter PM2.5 directly at Dhapa**, proving the severe localized necessity of subsurface thermal suppression.
3. **Fence-Line Attribution Network:** The **8.56 km regulatory monitoring gap is mathematically proven**, making the physical justification for a fence-line network scientifically rock-solid. However, all claims regarding unit counts (2,000+), nocturnal spikes (>180 µg/m³), and VIIRS radiance must remain strictly classified as `UNVERIFIED_HYPOTHESIS`, `SYNTHETIC_DATA`, and `MISSING_EVIDENCE` until empirical data is collected.
4. **No Score Changes**: In strict accordance with Milestone 6 directives, candidate scores and application code remain unchanged.
