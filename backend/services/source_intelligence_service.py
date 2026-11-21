"""
Source Intelligence Service:
Foundational source-apportionment studies, emission inventories, and evidence attribution.

Enforces strict scientific classification:
1. AMBIENT_CONCENTRATION (Measured ground-level station reading)
2. PUBLISHED_SOURCE_APPORTIONMENT (Receptor model / PMF / CMB peer-reviewed output)
3. EMISSION_INVENTORY (Bottom-up activity data x emission factor estimate)
4. SATELLITE_DERIVED (Atmospheric column or proxy observation)
5. STATISTICAL_ASSOCIATION (Empirical regression or correlation)
6. RESEARCH_HYPOTHESIS (Unverified research premise)
"""
from typing import List, Dict, Any

EVIDENCE_TYPES = {
    "AMBIENT_CONCENTRATION": {
        "label": "Ambient Concentration",
        "description": "Direct sensor reading from ground monitoring station. Does NOT identify source.",
        "badge_color": "#3B82F6" # blue
    },
    "PUBLISHED_SOURCE_APPORTIONMENT": {
        "label": "Published Source Apportionment",
        "description": "Scientific receptor modeling (PMF/CMB) from peer-reviewed or statutory study.",
        "badge_color": "#10B981" # emerald
    },
    "EMISSION_INVENTORY": {
        "label": "Emissions Inventory",
        "description": "Bottom-up estimate calculated from fuel, traffic counts and emission factors.",
        "badge_color": "#F59E0B" # amber
    },
    "SATELLITE_DERIVED": {
        "label": "Satellite Observation",
        "description": "Atmospheric column total (e.g. TROPOMI tropospheric NO2), not ground breathing level.",
        "badge_color": "#8B5CF6" # purple
    },
    "STATISTICAL_ASSOCIATION": {
        "label": "Statistical Association",
        "description": "Co-variation observed in datasets; explicitly non-causal without physical validation.",
        "badge_color": "#6B7280" # gray
    },
    "RESEARCH_HYPOTHESIS": {
        "label": "Research Hypothesis",
        "description": "Proposed engineering or policy intervention under scientific investigation.",
        "badge_color": "#FFE547" # yellow/prana accent
    }
}

class SourceIntelligenceService:
    @staticmethod
    def get_source_taxonomy() -> List[Dict[str, Any]]:
        return [
            {
                "code": "ROAD_TRANSPORT",
                "name": "Road Transport & Vehicular Exhaust",
                "sector": "Mobile Sources",
                "primary_pollutants": "PM2.5, NO2, CO, Elemental Carbon (BC)",
                "typical_marker_species": "EC, Hopanes, Steranes, NOx",
                "description": "Tailpipe emissions from diesel freight, heavy commercial vehicles, buses, taxis, two-wheelers, and idling congestion at major river crossings (Howrah Bridge, Vidyasagar Setu) and arterial nodes."
            },
            {
                "code": "ROAD_DUST",
                "name": "Road Dust Resuspension",
                "sector": "Fugitive Dust",
                "primary_pollutants": "PM10 (dominant), PM2.5 (coarse fraction)",
                "typical_marker_species": "Crustal elements (Si, Al, Ca, Fe, Ti)",
                "description": "Mechanical resuspension of silt from unpaved shoulders and heavy vehicular movement along major corridors (EM Bypass, Belgharia Expressway, Kona Expressway)."
            },
            {
                "code": "INDUSTRIAL_FOUNDRY",
                "name": "Industrial Emissions & Howrah Foundries",
                "sector": "Point & Area Industrial",
                "primary_pollutants": "PM2.5, PM10, SO2, Heavy Metals",
                "typical_marker_species": "Fe, Zn, Pb, Mn, Sulfate",
                "description": "Small and medium scale cast-iron foundries, rerolling mills, forging units, and fabrication facilities predominantly concentrated in northern Howrah (Ghusuri, Liluah, Belur, Bally)."
            },
            {
                "code": "SOLID_WASTE_BURNING",
                "name": "Municipal Solid Waste & Biomass Burning",
                "sector": "Open Combustion",
                "primary_pollutants": "PM2.5, CO, VOCs, Polycyclic Aromatic Hydrocarbons",
                "typical_marker_species": "Levoglucosan, Potassium (K+), Dioxins",
                "description": "Spontaneous subsurface landfill combustion at Dhapa dump site, municipal leaf/trash burning, and domestic wood/biomass cooking in peri-urban slums and fringe settlements."
            },
            {
                "code": "CONSTRUCTION_DEMOLITION",
                "name": "Construction & Infrastructure Activity",
                "sector": "Fugitive Dust",
                "primary_pollutants": "PM10, Coarse Particulates",
                "typical_marker_species": "Calcium, Carbonates, Gypsum, Silicates",
                "description": "Metro rail expansion corridors, mega housing developments in New Town/Rajarhat, riverfront redevelopments, and uncovered transit of building materials."
            },
            {
                "code": "REGIONAL_TRANSBOUNDARY",
                "name": "Secondary Aerosols & Regional Inflow",
                "sector": "Transboundary / Regional",
                "primary_pollutants": "PM2.5 (Secondary Sulfate & Nitrate)",
                "typical_marker_species": "Ammonium Sulfate, Ammonium Nitrate",
                "description": "Long-range transport along Indo-Gangetic Plain (IGP) downwind plume, plus regional thermal power plants (Kolaghat, Bandel, Sagardighi) contributing sulfur dioxide converting to secondary sulfates."
            }
        ]

    @staticmethod
    def get_published_studies() -> List[Dict[str, Any]]:
        """Foundational published research studies covering Kolkata and Howrah."""
        return [
            {
                "id": 1,
                "title": "Air Pollution Emissions Inventory, Source Apportionment and Atmospheric Carrying Capacity Study of Kolkata",
                "organisation": "TERI (The Energy and Resources Institute) for WBPCB",
                "publication_year": 2025,
                "methodology": "Receptor Modeling (PMF 5.0) combined with High-Resolution (1km x 1km) Gridded Bottom-Up Emissions Inventory",
                "geographic_scope": "Kolkata Municipal Corporation (KMC) Area",
                "study_period": "2021-2024 Multi-season Intensive Monitoring",
                "key_findings": (
                    "Winter PM2.5 source apportionment revealed: Secondary Inorganic Aerosols (24%), Road Transport (27%), "
                    "Biomass & Waste Burning (14%), Road Dust (12%), Industrial Sources (13%), Domestic Fuel (10%). "
                    "Atmospheric carrying capacity is severely exceeded during December–January due to nocturnal planetary "
                    "boundary layer compression (<400m) and calms."
                ),
                "limitations": "Does not fully capture trans-river industrial plumes originating in northern Howrah entering northern Kolkata under westerly wind regimes.",
                "confidence_tier": "Statutory Authority / Highest Scientific Rigour",
                "original_url": "https://www.wbpcb.gov.in/files/We-07-2025-07-48-01SA_EI_CC_Kolkata_WBPCB_2025.pdf"
            },
            {
                "id": 2,
                "title": "PM10 and PM2.5 Source Apportionment Study and Development of Emission Inventory of Twin Cities Kolkata and Howrah",
                "organisation": "CSIR-NEERI (National Environmental Engineering Research Institute) & WBPCB",
                "publication_year": 2020,
                "methodology": "Chemical Mass Balance (CMB 8.2) & Dispersion Modeling (AERMOD)",
                "geographic_scope": "Kolkata and Howrah Metropolitan Area",
                "study_period": "2018-2020 Field Sampling",
                "key_findings": (
                    "In Howrah, industrial fuel burning and foundries contributed up to 34% of winter PM2.5 at Ghusuri, "
                    "whereas vehicular exhaust accounted for 30% of PM2.5 in central Kolkata. Road dust accounted for 38% "
                    "of summer PM10 across twin cities."
                ),
                "limitations": "Older receptor source profiles; emission factors for non-certified diesel commercial vehicles may have high variance.",
                "confidence_tier": "Statutory / CSIR National Laboratory Study",
                "original_url": "https://www.wbpcb.gov.in/writereaddata/files/SA_Kol-How_Final%20Report.pdf"
            }
        ]
