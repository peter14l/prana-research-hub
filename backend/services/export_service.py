"""
Export and Reporting Service:
Generates downloadable CSV datasets and comprehensive Research Brief documents.
"""
import io
import csv
from datetime import datetime
from typing import List, Dict, Any

class ExportService:
    @staticmethod
    def export_observations_csv(records: List[Dict[str, Any]]) -> str:
        """Exports validated observations as formatted CSV string."""
        output = io.StringIO()
        fieldnames = [
            "station_code", "station_name", "city", "pollutant",
            "normalized_value", "unit", "observation_timestamp",
            "quality_status", "provenance"
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
        hotspots: List[Dict[str, Any]]
    ) -> str:
        """Generates a structured, printable Research Brief in Markdown format."""
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        
        md = []
        md.append("# PRANA Research Hub: Environmental Intelligence Brief")
        md.append(f"**Region**: Kolkata–Howrah Urban Air Shed, West Bengal, India")
        md.append(f"**Generated**: {now}")
        md.append(f"**Methodological Standard**: Indian CPCB AQI Protocols & Peer-Reviewed Source Apportionment")
        md.append("\n---\n")
        
        md.append("## 1. Regional Air Quality Status")
        md.append(f"- **PM2.5 Regional Mean**: {summary.get('pm25_avg', 'N/A')} µg/m³")
        md.append(f"- **PM10 Regional Mean**: {summary.get('pm10_avg', 'N/A')} µg/m³")
        md.append(f"- **NO2 Regional Mean**: {summary.get('no2_avg', 'N/A')} µg/m³")
        md.append(f"- **SO2 Regional Mean**: {summary.get('so2_avg', 'N/A')} µg/m³")
        md.append(f"- **Reporting Stations**: {summary.get('reporting_stations', 0)} / {summary.get('total_stations', 0)}")
        md.append(f"- **Dominant Regional Category**: {summary.get('dominant_category', 'N/A')}")
        md.append("\n")

        md.append("## 2. Identified Hotspots & Spatial Coverage Gaps")
        md.append("| Zone / Station | Monitoring Status | Uncertainty | Primary Driver / Gap Note |")
        md.append("| :--- | :--- | :--- | :--- |")
        for h in hotspots:
            md.append(f"| {h['zone_name']} | {h['monitoring_status']} | {h['uncertainty_level']} | {h['scientific_gap_note']} |")
        md.append("\n")

        md.append("## 3. Recommended Engineering Intervention Candidates")
        for h in hypotheses:
            md.append(f"### {h['title']}")
            md.append(f"- **Target Area**: {h['target_area']}")
            md.append(f"- **Target Pollutants**: {h['target_pollutant']}")
            md.append(f"- **Suspected Source**: {h['suspected_source']}")
            md.append(f"- **Proposed Action**: {h['proposed_intervention']}")
            md.append(f"- **Measurable Indicators**: {h['measurable_indicators']}")
            md.append(f"- **Feasibility Score**: {h.get('feasibility_score')}/10 | **Potential Reduction**: {h.get('potential_reduction_score')}/10")
            md.append("\n")

        md.append("## 4. Scientific Assumptions & Limitations")
        md.append("1. Ground telemetry reflects ambient breathing-level concentrations, not direct stack or tailpipe contributions.")
        md.append("2. Source attribution is cited from TERI (2025) and CSIR-NEERI (2020) official statutory reports.")
        md.append("3. Interventions require formal baseline monitoring and counterfactual meteorological de-weathering before attributing emission reductions.")
        
        return "\n".join(md)
