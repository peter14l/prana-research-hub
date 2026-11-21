"""
Intervention Lab Service:
Translates environmental intelligence into defensible, testable engineering hypotheses.
Includes counterfactual evaluation, meteorological de-weathering specifications, and multi-criteria decision scoring.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime

class InterventionService:
    @staticmethod
    def get_seed_hypotheses() -> List[Dict[str, Any]]:
        return [
            {
                "id": 1,
                "title": "Howrah Foundry Cluster Divided-Blast & Baghouse Retrofit Demonstration",
                "problem_statement": (
                    "Winter PM2.5 in northern Howrah (Ghusuri monitoring station) frequently exceeds 220 µg/m³ (Severe AQI category). "
                    "CSIR-NEERI (2020) and TERI (2025) source-apportionment studies identify metal casting, cupola furnaces, and coal-fired "
                    "rerolling mills as contributing 32–35% of localized winter particulate mass."
                ),
                "target_area": "Ghusuri & Liluah Industrial Cluster, Northern Howrah",
                "target_pollutant": "PM2.5, PM10, SO2, Heavy Metals (Zn, Pb)",
                "suspected_source": "Small-scale cupola furnaces, unscrubbed coal flue gas, and fugitive charging emissions",
                "supporting_evidence": (
                    "1. Ghusuri continuous CPCB station records highest annual mean PM2.5 in West Bengal (108 µg/m³ vs 40 µg/m³ standard).\n"
                    "2. Elemental analysis indicates strong zinc, lead, and elemental carbon enrichment during nocturnal shifts.\n"
                    "3. TERI 2025 Carrying Capacity study marks Howrah foundry cluster as severely exceeding assimilative capacity."
                ),
                "proposed_intervention": (
                    "Engineer and pilot an automated, modular wet-scrubber and pulse-jet baghouse filtration package tailored for "
                    "low-tonnage cupola stacks, coupled with oxygen-enrichment divided blast to achieve complete combustion."
                ),
                "mechanism_of_action": (
                    "High-temperature baghouse filters mechanically capture fine sub-micron metallic aerosols (efficiency >98%). "
                    "Divided blast technology increases furnace flame temperature, reducing unburned carbon and CO emissions by 40%."
                ),
                "required_resources": "Fabrication of 2 prototype skid units; continuous optical particulate sensor array; ₹45 Lakhs (~$55,000 USD).",
                "possible_implementation_partner": "Howrah Foundry Association, WBPCB Regional Office, MSME Technology Centre Kolkata.",
                "measurable_indicators": (
                    "Primary: ≥25% reduction in localized 24-hr PM2.5 at downwind 500m perimeter sensor during winter operational season.\n"
                    "Secondary: Stack particulate concentration reduced from >150 mg/Nm³ to <30 mg/Nm³."
                ),
                "risks_limitations": "Foundry operating margins are tight; capital expenditure resistance; space constraints in cramped century-old industrial alleys.",
                "research_confidence": "HIGH",
                "validation_requirements": (
                    "Rigorous pre-intervention stack and fence-line baseline (60 days); continuous post-retrofit telemetry; "
                    "control comparison against upwind background."
                ),
                "feasibility_score": 7.5,
                "potential_reduction_score": 8.8,
                "cost_complexity_score": 5.8,
                "ease_of_verification_score": 8.2,
                "scalability_score": 9.0,
                "evaluation_framework": {
                    "baseline_period_days": 60,
                    "intervention_period_days": 120,
                    "control_station": "Victoria Memorial (Urban Background)",
                    "impact_station": "Ghusuri (Industrial Hotspot)",
                    "weather_normalization_method": "Random Forest de-weathering model trained on wind speed, direction, temperature inversion, and PBLH",
                    "confounding_factors": ["Diwali festival episodic spikes", "Seasonal crop burning transit", "Brick kiln seasonal starts in Hooghly"]
                },
                "status": "PROPOSAL_READY"
            },
            {
                "id": 2,
                "title": "River Hooghly Ferry Terminal Shore-to-Ship Cold Ironing & Electric Propulsion Pilot",
                "problem_statement": (
                    "Over 40 diesel passenger ferries operate continuously across the Hooghly River between Kolkata and Howrah. "
                    "Older non-compliant marine diesel engines idle at docks, emitting high quantities of raw NO2 and black carbon right at "
                    "breathing height in congested pedestrian corridors (Babughat, Fairlie Place, Howrah Station ghat)."
                ),
                "target_area": "Hooghly Riverfront (Howrah Station to Fairlie Ghat)",
                "target_pollutant": "NO2, PM2.5, Black Carbon (BC)",
                "suspected_source": "Marine diesel engines idling and accelerating during frequent dock-to-dock passenger transit",
                "supporting_evidence": (
                    "1. TERI (2025) emissions inventory estimates commercial water transport contributes significant localized NOx along the river corridor.\n"
                    "2. Ground-level peak NO2 at Howrah Station reaches >95 µg/m³ during peak commuter transit hours (8:00–10:30 AM)."
                ),
                "proposed_intervention": (
                    "Install 3 shore-to-ship charging pedestals ('cold ironing') to eliminate diesel auxiliary idling during berth times, "
                    "and retrofit 2 high-frequency shuttle ferries with modular battery-electric propulsion."
                ),
                "mechanism_of_action": "Eliminates diesel combustion during berthing and passenger loading; zero direct tailpipe emission on river transit transect.",
                "required_resources": "150 kW shore power grid tie-in; battery conversion packs; ₹85 Lakhs.",
                "possible_implementation_partner": "West Bengal Transport Infrastructure Development Corporation (WBTIDC), Syama Prasad Mookerjee Port Kolkata.",
                "measurable_indicators": "Zero NO2 and particulate emissions at ferry berths during 15-minute passenger turnaround times; 70% lower localized BC.",
                "risks_limitations": "High initial battery cost; maritime safety certification protocols under Inland Vessels Act.",
                "research_confidence": "HIGH",
                "validation_requirements": "Install micro-sensors at passenger pontoon and upwind bank to measure dockside NO2 and ultrafine particles.",
                "feasibility_score": 8.0,
                "potential_reduction_score": 7.4,
                "cost_complexity_score": 6.5,
                "ease_of_verification_score": 9.0,
                "scalability_score": 8.5,
                "evaluation_framework": {
                    "baseline_period_days": 45,
                    "intervention_period_days": 90,
                    "control_station": "Fort William",
                    "impact_station": "Riverfront Pontoon Sensor",
                    "weather_normalization_method": "Wind-direction gating to isolate ferry plume from riverbank vehicular traffic",
                    "confounding_factors": ["Strand Road vehicular congestion", "River cargo tugs transit"]
                },
                "status": "UNDER_REVIEW"
            },
            {
                "id": 3,
                "title": "Arterial Road Silt Load Suppression & Night-Sweep Telemetry on BT Road Corridor",
                "problem_statement": (
                    "Rabindra Bharati University (RBU) monitoring station on BT Road consistently records PM10 exceeding 240 µg/m³. "
                    "CSIR-NEERI (2020) confirmed road dust resuspension constitutes 38% of total PM10 mass in northern Kolkata."
                ),
                "target_area": "Barrackpore Trunk (BT) Road (5 km stretch surrounding RBU station)",
                "target_pollutant": "PM10, Coarse Crustal Particulate",
                "suspected_source": "Heavy vehicular entrainment of road silt, unpaved curb deposition, and construction debris transport",
                "supporting_evidence": (
                    "1. RBU station exhibits PM10 to PM2.5 ratio exceeding 2.3:1 (indicating strong coarse mechanical dust dominance).\n"
                    "2. Silt load measurements by NEERI found BT Road median silt loadings exceeding 45 g/m²."
                ),
                "proposed_intervention": (
                    "Deploy IoT-monitored high-efficiency regenerative vacuum sweeping trucks paired with biodegradable dust-binding "
                    "surfactant misting during post-midnight curfew hours (1:00–5:00 AM), combined with curb-to-curb asphalt shoulder sealing."
                ),
                "mechanism_of_action": "Binds loose silt to prevent aerodynamic re-entrainment by high-speed truck traffic.",
                "required_resources": "2 mechanized sweeping vehicles, surface surfactant supply, road dust silt-samplers; ₹30 Lakhs.",
                "possible_implementation_partner": "Kolkata Municipal Corporation (KMC) Solid Waste & Road Dept, PWD West Bengal.",
                "measurable_indicators": "Daily PM10 at RBU station reduced by ≥18% compared to control arterial corridor (EM Bypass). Silt load <10 g/m².",
                "risks_limitations": "Surfactant wash-off during rain; coordination with midnight truck freight movements.",
                "research_confidence": "MEDIUM",
                "validation_requirements": "Standard ASTM C136 silt sampling alongside 24-hr continuous PM10 monitoring at RBU.",
                "feasibility_score": 8.5,
                "potential_reduction_score": 7.0,
                "cost_complexity_score": 4.5,
                "ease_of_verification_score": 8.0,
                "scalability_score": 8.8,
                "evaluation_framework": {
                    "baseline_period_days": 30,
                    "intervention_period_days": 60,
                    "control_station": "Ballygunge (South Mixed)",
                    "impact_station": "Rabindra Bharati University (BT Road)",
                    "weather_normalization_method": "Relative humidity and precipitation filtering; diurnal differencing",
                    "confounding_factors": ["Rainfall events cleansing road", "Construction site spillover"]
                },
                "status": "PROPOSAL_READY"
            }
        ]
