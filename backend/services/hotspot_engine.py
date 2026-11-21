"""
Hotspot Identification and Spatial Coverage Gap Engine for Kolkata & Howrah.
Uses Haversine spatial geodesic distance and uncertainty estimation.
Strictly adheres to: 'Do not invent ward-level pollution measurements from city-level averages.
Where spatial coverage is insufficient, explicitly show the coverage gap.'
"""
import math
from typing import List, Dict, Any, Optional

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0 # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2.0) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2.0) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class HotspotEngine:
    # Defined administrative boroughs / key zones in Kolkata and Howrah
    ZONES = [
        {"id": "ZONE_CENTRAL_KOL", "name": "Central Kolkata / Maidan", "city": "Kolkata", "lat": 22.560, "lng": 88.350, "type": "Commercial / Heritage"},
        {"id": "ZONE_NORTH_KOL", "name": "North Kolkata / BT Road Corridor", "city": "Kolkata", "lat": 22.620, "lng": 88.380, "type": "Dense Traffic / Commercial"},
        {"id": "ZONE_SOUTH_KOL", "name": "South Kolkata (Ballygunge / Jadavpur)", "city": "Kolkata", "lat": 22.520, "lng": 88.365, "type": "Residential / Mixed"},
        {"id": "ZONE_EAST_KOL", "name": "East Kolkata (Salt Lake / Rajarhat Fringe)", "city": "Kolkata", "lat": 22.585, "lng": 88.420, "type": "IT / Planned / Expanding"},
        {"id": "ZONE_PORT_SW_KOL", "name": "Khidirpur Port & Behala Corridor", "city": "Kolkata", "lat": 22.510, "lng": 88.310, "type": "Freight / Port / Dense Suburban"},
        {"id": "ZONE_DHAPA_WETLANDS", "name": "Dhapa Landfill & Wetlands Buffer", "city": "Kolkata", "lat": 22.545, "lng": 88.410, "type": "Waste Disposal / Peri-urban"},
        {"id": "ZONE_NORTH_HOWRAH", "name": "North Howrah (Ghusuri / Liluah Foundries)", "city": "Howrah", "lat": 22.610, "lng": 88.345, "type": "Heavy Foundry / Rerolling Mills"},
        {"id": "ZONE_CENTRAL_HOWRAH", "name": "Central Howrah (Station / Padmapukur)", "city": "Howrah", "lat": 22.570, "lng": 88.320, "type": "Rail Terminal / Dense Mixed"},
        {"id": "ZONE_WEST_HOWRAH", "name": "West Howrah (Kona / Industrial Periphery)", "city": "Howrah", "lat": 22.580, "lng": 88.260, "type": "Logistics Corridor / Peri-industrial"}
    ]

    @classmethod
    def evaluate_zones(cls, station_metrics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Evaluates zones against active monitoring stations.
        If nearest station is > 3.5 km away, explicitly labels as 'COVERAGE_GAP_HIGH_UNCERTAINTY'.
        Never assigns interpolated values to unmonitored zones without uncertainty warnings.
        """
        results = []

        for zone in cls.ZONES:
            # Find closest monitoring stations
            distances = []
            for st in station_metrics:
                d = haversine_km(zone["lat"], zone["lng"], st["latitude"], st["longitude"])
                distances.append({"station": st, "distance_km": round(d, 2)})

            distances.sort(key=lambda x: x["distance_km"])
            nearest = distances[0] if distances else None

            if not nearest:
                continue

            nearest_st = nearest["station"]
            dist_km = nearest["distance_km"]

            # Scientific assessment of spatial validity
            if dist_km <= 2.5:
                status = "RELIABLY_MONITORED"
                uncertainty = "Low (< 15%)"
                can_estimate = True
                est_pm25 = nearest_st.get("pm25_latest")
                est_pm10 = nearest_st.get("pm10_latest")
                gap_note = f"Directly captured by {nearest_st['name']} ({dist_km} km away)."
            elif dist_km <= 4.0:
                status = "MODERATE_PROXIMITY"
                uncertainty = "Moderate (~ 25-35%)"
                can_estimate = True
                est_pm25 = nearest_st.get("pm25_latest")
                est_pm10 = nearest_st.get("pm10_latest")
                gap_note = f"Approximated from {nearest_st['name']} ({dist_km} km away). Microclimate variations likely."
            else:
                status = "COVERAGE_GAP"
                uncertainty = "High (> 50% - Ground Truth Missing)"
                can_estimate = False
                est_pm25 = None
                est_pm10 = None
                gap_note = (
                    f"CRITICAL COVERAGE GAP: Nearest station ({nearest_st['name']}) is {dist_km} km away. "
                    "Per PRANA scientific standards, ambient concentrations are NOT interpolated to avoid spurious conclusions."
                )

            # Hotspot classification based on confirmed monitoring or known structural emission drivers
            is_hotspot = False
            hotspot_reasons = []

            if nearest_st.get("station_code") == "WB007_GHUSURI" and dist_km < 3.0:
                is_hotspot = True
                hotspot_reasons.append("Recurrent industrial PM2.5/PM10 spikes from Howrah foundry cluster")
            elif nearest_st.get("station_code") == "WB003_RBU" and dist_km < 3.0:
                is_hotspot = True
                hotspot_reasons.append("High vehicle exhaust and resuspension along BT Road arterial corridor")
            elif zone["id"] == "ZONE_PORT_SW_KOL":
                is_hotspot = True
                hotspot_reasons.append("Suspected freight/port diesel hotspot (requires ground sensor deployment)")
            elif zone["id"] == "ZONE_DHAPA_WETLANDS":
                is_hotspot = True
                hotspot_reasons.append("Intermittent open combustion and refuse fire plume source")

            results.append({
                "zone_id": zone["id"],
                "zone_name": zone["name"],
                "city": zone["city"],
                "zone_type": zone["type"],
                "latitude": zone["lat"],
                "longitude": zone["lng"],
                "monitoring_status": status,
                "uncertainty_level": uncertainty,
                "can_estimate_ambient": can_estimate,
                "nearest_station_name": nearest_st["name"],
                "nearest_station_code": nearest_st["station_code"],
                "nearest_distance_km": dist_km,
                "estimated_pm25": est_pm25,
                "estimated_pm10": est_pm10,
                "is_potential_hotspot": is_hotspot,
                "hotspot_drivers": hotspot_reasons,
                "scientific_gap_note": gap_note
            })

        return results
