"""
Export and Reporting Service (Milestone 2 - Data Provenance & Integrity Aware)
Generates downloadable CSV datasets and comprehensive Research Brief documents with provenance.
"""
import io
import csv
from datetime import datetime
from typing import List, Dict, Any, Optional

class ExportService:
    @staticmethod
    def export_observations_csv(records: List[Dict[str, Any]]) -> str:
        """Exports validated observations as formatted CSV string with full provenance attribution."""
        output = io.StringIO()
        fieldnames = [
            "station_code", "station_name", "city", "pollutant",
            "normalized_value", "unit", "observation_timestamp",
            "data_classification", "quality_status", "provenance", "provenance_hash"
        ]
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for r in records:
            writer.writerow(r)
        return output.getvalue()

    @staticmethod
    def generate_research_brief_markdown(
        summary: Dict[str, Any],
        hypotheses: List[Dict[str, Any]],
        hotspots: List[Dict[str, Any]],
        audit: Optional[Dict[str, Any]] = None
    ) -> str:
        """Generates a structured, printable Research Brief in Markdown format with explicit integrity stats."""
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        integrity = summary.get("data_integrity", {})
        counts = integrity.get("counts", {})
        total_recs = integrity.get("total_records", 0)
        
        md = []
        md.append("# PRANA Research Hub: Environmental Intelligence & Data Integrity Brief")
        md.append(f"**Region**: Kolkata–Howrah Urban Air Shed, West Bengal, India")
        md.append(f"**Generated**: {now}")
        md.append(f"**Methodological Standard**: Indian CPCB AQI Protocols & Peer-Reviewed Source Apportionment")
        md.append("\n---\n")

        md.append("## 1. Global Data Integrity & Provenance Audit")
        md.append("| Classification | Record Count | Percentage | Definition |")
        md.append("| :--- | :---: | :---: | :--- |")
        md.append(f"| **VERIFIED** | {counts.get('VERIFIED', 0):,} | {integrity.get('verified_pct', 0.0)}% | Traceable to official accessible statutory stream |")
        md.append(f"| **IMPORTED** | {counts.get('IMPORTED', 0):,} | {integrity.get('imported_pct', 0.0)}% | Researcher-uploaded dataset with provenance hash |")
        md.append(f"| **DERIVED** | {counts.get('DERIVED', 0):,} | — | Algorithmic calculations (CPCB NAQI sub-indices) |")
        md.append(f"| **DEMO** | {counts.get('DEMO', 0):,} | {integrity.get('demo_pct', 0.0)}% | Synthetic baseline model used for system testing |")
        md.append(f"| **UNVERIFIED** | {counts.get('UNVERIFIED', 0):,} | — | Telemetry origin unverified |")
        md.append("\n")
        
        md.append("## 2. Regional Air Quality Status")
        md.append(f"- **PM2.5 Regional Mean**: {summary.get('pm25_avg', 'N/A')} µg/m³")
        md.append(f"- **PM10 Regional Mean**: {summary.get('pm10_avg', 'N/A')} µg/m³")
        md.append(f"- **NO2 Regional Mean**: {summary.get('no2_avg', 'N/A')} µg/m³")
        md.append(f"- **SO2 Regional Mean**: {summary.get('so2_avg', 'N/A')} µg/m³")
        md.append(f"- **Reporting Stations**: {summary.get('reporting_stations', 0)} / {summary.get('total_stations', 0)}")
        md.append(f"- **Dominant Regional Category**: {summary.get('dominant_category', 'N/A')}")
        md.append("\n")

        md.append("## 3. Verified Hotspots & Spatial Coverage Gaps")
        md.append("| Zone / Station | Monitoring Status | Uncertainty | Primary Driver / Gap Note |")
        md.append("| :--- | :--- | :--- | :--- |")
        for h in hotspots:
            md.append(f"| {h['zone_name']} | {h['monitoring_status']} | {h['uncertainty_level']} | {h['scientific_gap_note']} |")
        md.append("\n")

        md.append("## 4. Recommended Engineering Intervention Candidates")
        for h in hypotheses:
            md.append(f"### {h['title']}")
            md.append(f"- **Target Area**: {h['target_area']}")
            md.append(f"- **Target Pollutants**: {h['target_pollutant']}")
            md.append(f"- **Suspected Source**: {h['suspected_source']}")
            md.append(f"- **Proposed Action**: {h['proposed_intervention']}")
            md.append(f"- **Measurable Indicators**: {h['measurable_indicators']}")
            md.append(f"- **Feasibility Score**: {h.get('feasibility_score')}/10 | **Potential Reduction**: {h.get('potential_reduction_score')}/10")
            md.append("\n")

        md.append("## 5. Scientific Assumptions & Limitations")
        md.append("1. Ground telemetry reflects ambient breathing-level concentrations, not direct stack or tailpipe contributions.")
        md.append("2. Source attribution is cited from TERI (2025) Table 4.5 and CSIR-NEERI (2020) Table 6.14 statutory reports.")
        md.append("3. Interventions require formal baseline monitoring and counterfactual meteorological de-weathering before attributing emission reductions.")
        
        return "\n".join(md)
