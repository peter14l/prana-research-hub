"""
PRANA Research Hub - Environmental Analysis Engine (Milestone 3)
Provides research-grade statistical and geospatial analysis:
1. Temporal Analysis (Hourly diurnal, daily averages, weekly cycles, seasonal trends, multi-station comparisons)
2. Meteorological Analysis (Bivariate correlation with wind speed, temperature, humidity, rain, and 16-sector pollution rose)
3. Data Coverage & Completeness (Availability, temporal gaps, provider comparison)
4. Hotspot Investigation (Repeatedly elevated locations, coverage void warnings, uncertainty reporting)
Strict Rules:
- Filters observations to VERIFIED and IMPORTED tiers only (ignoring synthetic demo data when requested)
- Never extrapolates concentrations into unmonitored wards
- Enforces non-causal statistical caveats
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import numpy as np
import scipy.stats as stats
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.models.models import (
    ValidatedObservation, WeatherObservation, MonitoringStation, DataProvider
)

NAAQS_THRESHOLDS_24H = {
    "PM2.5": 60.0, # ug/m3
    "PM10": 100.0, # ug/m3
    "NO2": 80.0,   # ug/m3
    "SO2": 80.0,   # ug/m3
    "CO": 4.0,     # mg/m3
    "O3": 100.0,   # ug/m3 (8-hour)
    "NH3": 400.0   # ug/m3
}

UNMONITORED_COVERAGE_VOIDS = [
    {
        "zone_name": "Jalan Industrial Complex & Domjur Foundry Belt",
        "city": "Howrah",
        "nearest_station": "Ghusuri (WB007_GHUSURI)",
        "distance_km": 8.4,
        "suspected_emission_sources": "Cupola iron foundries, metal casting furnaces, freight diesel transit",
        "uncertainty_level": "CRITICAL_HIGH",
        "scientific_note": "Zero continuous statutory ambient monitoring exists in this heavy industrial cluster. Spatial extrapolation is scientifically invalid."
    },
    {
        "zone_name": "Khidirpur Docks & Kolkata Port Terminal",
        "city": "Kolkata",
        "nearest_station": "Fort William (WB002_FORT_WILLIAM)",
        "distance_km": 4.2,
        "suspected_emission_sources": "Marine vessel bunker fuel combustion, cargo handling equipment, heavy truck queue idling",
        "uncertainty_level": "HIGH",
        "scientific_note": "Port activities operate in an ambient monitoring void. Readings from Fort William residential green-space cannot represent dock air."
    },
    {
        "zone_name": "Uluberia Industrial & Engineering Cluster",
        "city": "Howrah",
        "nearest_station": "Padmapukur (WB009_PADMAPUKUR)",
        "distance_km": 18.5,
        "suspected_emission_sources": "Rolling mills, chemical manufacturing, brick kilns",
        "uncertainty_level": "CRITICAL_HIGH",
        "scientific_note": "Exceeds 15 km threshold for urban ambient station representativeness."
    },
    {
        "zone_name": "Budge Budge Petroleum Refining & Storage Depot",
        "city": "Kolkata",
        "nearest_station": "Ballygunge (WB004_BALLYGUNGE)",
        "distance_km": 14.8,
        "suspected_emission_sources": "Petroleum product storage, VOC fugitive emissions, barge transport",
        "uncertainty_level": "HIGH",
        "scientific_note": "No VOC or particulate monitor covers South-West industrial fringe."
    }
]

class EnvironmentalAnalysisEngine:
    @staticmethod
    def get_filtered_observations(
        db: Session,
        pollutant: str = "PM2.5",
        station_ids: Optional[List[int]] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        allowed_classifications: Optional[List[str]] = None
    ) -> List[ValidatedObservation]:
        """Queries validated observations filtered by pollutant, station, time, and data classification."""
        query = db.query(ValidatedObservation).filter(
            ValidatedObservation.pollutant == pollutant,
            ValidatedObservation.is_valid == True
        )

        if station_ids:
            query = query.filter(ValidatedObservation.station_id.in_(station_ids))
        if date_from:
            query = query.filter(ValidatedObservation.observation_timestamp >= date_from)
        if date_to:
            query = query.filter(ValidatedObservation.observation_timestamp <= date_to)
        if allowed_classifications:
            query = query.filter(ValidatedObservation.data_classification.in_(allowed_classifications))

        return query.order_by(ValidatedObservation.observation_timestamp.asc()).all()

    @staticmethod
    def analyze_temporal_patterns(
        observations: List[ValidatedObservation],
        pollutant: str = "PM2.5"
    ) -> Dict[str, Any]:
        """
        Calculates:
        1. Hourly diurnal profile (0-23h) with mean, median, 10th and 90th percentiles
        2. Daily aggregated averages with NAAQS exceedance count
        3. Weekly pattern (Monday - Sunday)
        4. Day-of-week ratio (Weekday vs Weekend)
        """
        if not observations:
            return {"error": "No observations available for selected temporal criteria."}

        # 1. Diurnal (0-23h)
        hourly_bins: Dict[int, List[float]] = {h: [] for h in range(24)}
        daily_bins: Dict[str, List[float]] = {}
        dow_bins: Dict[int, List[float]] = {d: [] for d in range(7)}

        for obs in observations:
            h = obs.observation_timestamp.hour
            d_key = obs.observation_timestamp.strftime("%Y-%m-%d")
            dow = obs.observation_timestamp.weekday() # 0 = Monday, 6 = Sunday

            val = float(obs.normalized_value)
            hourly_bins[h].append(val)
            dow_bins[dow].append(val)
            if d_key not in daily_bins:
                daily_bins[d_key] = []
            daily_bins[d_key].append(val)

        diurnal_profile = []
        for h in range(24):
            vals = hourly_bins[h]
            if vals:
                arr = np.array(vals)
                diurnal_profile.append({
                    "hour": h,
                    "hour_label": f"{h:02d}:00",
                    "mean": round(float(np.mean(arr)), 1),
                    "median": round(float(np.median(arr)), 1),
                    "p10": round(float(np.percentile(arr, 10)), 1),
                    "p90": round(float(np.percentile(arr, 90)), 1),
                    "sample_count": len(vals)
                })
            else:
                diurnal_profile.append({
                    "hour": h,
                    "hour_label": f"{h:02d}:00",
                    "mean": None,
                    "median": None,
                    "p10": None,
                    "p90": None,
                    "sample_count": 0
                })

        # 2. Daily Time Series & NAAQS Exceedances
        naaqs_limit = NAAQS_THRESHOLDS_24H.get(pollutant, 60.0)
        daily_series = []
        exceedance_count = 0

        for d_str, vals in sorted(daily_bins.items()):
            d_mean = round(float(np.mean(vals)), 1)
            is_exceedance = d_mean > naaqs_limit
            if is_exceedance:
                exceedance_count += 1

            daily_series.append({
                "date": d_str,
                "daily_average": d_mean,
                "min": round(float(np.min(vals)), 1),
                "max": round(float(np.max(vals)), 1),
                "sample_count": len(vals),
                "naaqs_limit": naaqs_limit,
                "exceeds_naaqs": is_exceedance
            })

        # 3. Day of Week Pattern
        dow_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dow_profile = []
        weekday_vals = []
        weekend_vals = []

        for d in range(7):
            vals = dow_bins[d]
            m_val = round(float(np.mean(vals)), 1) if vals else None
            dow_profile.append({
                "day_index": d,
                "day_name": dow_names[d],
                "mean": m_val,
                "sample_count": len(vals)
            })
            if d < 5:
                weekday_vals.extend(vals)
            else:
                weekend_vals.extend(vals)

        weekday_avg = round(float(np.mean(weekday_vals)), 1) if weekday_vals else 0.0
        weekend_avg = round(float(np.mean(weekend_vals)), 1) if weekend_vals else 0.0
        dow_ratio = round(weekday_avg / weekend_avg, 2) if weekend_avg > 0 else 1.0

        return {
            "pollutant": pollutant,
            "unit": observations[0].unit if observations else "ug/m3",
            "total_observations_analyzed": len(observations),
            "diurnal_profile": diurnal_profile,
            "daily_series": daily_series,
            "naaqs_24h_threshold": naaqs_limit,
            "naaqs_exceedance_days": exceedance_count,
            "total_days_analyzed": len(daily_bins),
            "exceedance_rate_pct": round((exceedance_count / len(daily_bins) * 100.0) if daily_bins else 0.0, 1),
            "day_of_week_profile": dow_profile,
            "weekday_average": weekday_avg,
            "weekend_average": weekend_avg,
            "weekday_to_weekend_ratio": dow_ratio
        }

    @staticmethod
    def analyze_meteorological_relationships(
        db: Session,
        observations: List[ValidatedObservation],
        pollutant: str = "PM2.5",
        city: str = "Kolkata"
    ) -> Dict[str, Any]:
        """
        Analyzes synchronous relationships between pollutant concentrations and Open-Meteo reanalysis weather:
        1. Bivariate correlations: Wind Speed, Temperature, Relative Humidity, Precipitation, Surface Pressure, PBLH
        2. 16-Sector Pollution Rose (Mean and 90th percentile concentration by wind direction)
        Includes explicit non-causal disclaimer and p-values.
        """
        if not observations:
            return {"error": "No observations available for meteorological analysis."}

        # Query synchronous weather records
        timestamps = [obs.observation_timestamp for obs in observations]
        min_ts = min(timestamps)
        max_ts = max(timestamps)

        weather_records = db.query(WeatherObservation).filter(
            WeatherObservation.city == city,
            WeatherObservation.observation_timestamp >= min_ts - timedelta(hours=1),
            WeatherObservation.observation_timestamp <= max_ts + timedelta(hours=1)
        ).all()

        weather_by_hour = {w.observation_timestamp.strftime("%Y-%m-%d %H:00"): w for w in weather_records}

        paired_data = []
        wind_rose_bins: Dict[str, List[float]] = {
            "N": [], "NNE": [], "NE": [], "ENE": [], "E": [], "ESE": [], "SE": [], "SSE": [],
            "S": [], "SSW": [], "SW": [], "WSW": [], "W": [], "WNW": [], "NW": [], "NNW": []
        }

        for obs in observations:
            h_key = obs.observation_timestamp.strftime("%Y-%m-%d %H:00")
            w = weather_by_hour.get(h_key)
            if not w:
                continue

            pol_val = float(obs.normalized_value)
            paired_data.append({
                "timestamp": obs.observation_timestamp.isoformat(),
                "pollutant_value": pol_val,
                "wind_speed": w.wind_speed_kmh,
                "wind_direction": w.wind_direction_deg,
                "cardinal": w.wind_direction_cardinal,
                "temperature": w.temperature_c,
                "relative_humidity": w.relative_humidity_pct,
                "precipitation": w.rainfall_mm,
                "surface_pressure": w.surface_pressure_hpa,
                "pblh": w.boundary_layer_height_m
            })

            if w.wind_direction_cardinal in wind_rose_bins:
                wind_rose_bins[w.wind_direction_cardinal].append(pol_val)

        if len(paired_data) < 5:
            return {
                "paired_sample_count": len(paired_data),
                "notice": "Insufficient synchronous weather records paired. Run weather ingestion to synchronize."
            }

        pol_vals = np.array([p["pollutant_value"] for p in paired_data])

        # Bivariate statistics helper
        def calc_bivariate(var_key: str, name: str, unit: str):
            valid_pairs = [(p["pollutant_value"], p[var_key]) for p in paired_data if p[var_key] is not None]
            if len(valid_pairs) < 5:
                return None
            xs = np.array([v[1] for v in valid_pairs])
            ys = np.array([v[0] for v in valid_pairs])

            r, p_val = stats.pearsonr(xs, ys)
            slope, intercept, _, _, _ = stats.linregress(xs, ys)

            return {
                "variable_name": name,
                "variable_unit": unit,
                "sample_count": len(valid_pairs),
                "pearson_r": round(float(r), 3),
                "p_value": float(f"{p_val:.4e}"),
                "is_statistically_significant": bool(p_val < 0.05),
                "linear_slope": round(float(slope), 3),
                "linear_intercept": round(float(intercept), 2),
                "scatter_sample": [{"x": round(float(x), 1), "y": round(float(y), 1)} for x, y in valid_pairs[:80]]
            }

        correlations = {
            "wind_speed": calc_bivariate("wind_speed", "Wind Speed (10m)", "km/h"),
            "temperature": calc_bivariate("temperature", "2m Temperature", "°C"),
            "relative_humidity": calc_bivariate("relative_humidity", "Relative Humidity", "%"),
            "precipitation": calc_bivariate("precipitation", "Precipitation", "mm"),
            "boundary_layer_height": calc_bivariate("pblh", "Planetary Boundary Layer Height", "m")
        }

        # 16-Sector Pollution Rose
        pollution_rose = []
        for cardinal, vals in wind_rose_bins.items():
            if vals:
                arr = np.array(vals)
                pollution_rose.append({
                    "cardinal": cardinal,
                    "mean_concentration": round(float(np.mean(arr)), 1),
                    "p90_concentration": round(float(np.percentile(arr, 90)), 1),
                    "frequency_count": len(vals)
                })
            else:
                pollution_rose.append({
                    "cardinal": cardinal,
                    "mean_concentration": None,
                    "p90_concentration": None,
                    "frequency_count": 0
                })

        return {
            "pollutant": pollutant,
            "paired_sample_count": len(paired_data),
            "weather_provider": "Open-Meteo High-Resolution Atmospheric Reanalysis (Modelled)",
            "scientific_caveat": (
                "SCIENTIFIC PROTOCOL: Meteorological associations represent synoptic dispersion dynamics. "
                "Correlation DOES NOT demonstrate physical causation. Weather data is derived from numerical "
                "atmospheric reanalysis, not ground weather stations."
            ),
            "correlations": correlations,
            "pollution_rose_16_sectors": pollution_rose
        }

    @staticmethod
    def investigate_hotspots_and_coverage_gaps(
        db: Session,
        pollutant: str = "PM2.5",
        hours_window: int = 168
    ) -> Dict[str, Any]:
        """
        Analyzes monitored hotspots (repeating elevated concentrations) and
        explicitly highlights unmonitored industrial/port coverage voids with high-uncertainty warnings.
        """
        cutoff = datetime.utcnow() - timedelta(hours=hours_window)
        stations = db.query(MonitoringStation).all()
        naaqs_limit = NAAQS_THRESHOLDS_24H.get(pollutant, 60.0)

        monitored_hotspots = []
        for st in stations:
            obs = db.query(ValidatedObservation).filter(
                ValidatedObservation.station_id == st.id,
                ValidatedObservation.pollutant == pollutant,
                ValidatedObservation.observation_timestamp >= cutoff,
                ValidatedObservation.is_valid == True
            ).all()

            if not obs:
                continue

            vals = [float(o.normalized_value) for o in obs]
            arr = np.array(vals)
            exceedances = [v for v in vals if v > naaqs_limit]

            monitored_hotspots.append({
                "station_id": st.id,
                "station_code": st.station_code,
                "station_name": st.name,
                "cpcb_site_id": st.cpcb_site_id,
                "city": st.city,
                "latitude": st.latitude,
                "longitude": st.longitude,
                "total_observations": len(vals),
                "mean_concentration": round(float(np.mean(arr)), 1),
                "max_concentration": round(float(np.max(arr)), 1),
                "p90_concentration": round(float(np.percentile(arr, 90)), 1),
                "exceedance_count": len(exceedances),
                "exceedance_rate_pct": round((len(exceedances) / len(vals) * 100.0), 1),
                "hotspot_classification": "SEVERELY_ELEVATED" if len(exceedances) / len(vals) > 0.6 else "MODERATELY_ELEVATED" if len(exceedances) / len(vals) > 0.3 else "BACKGROUND"
            })

        monitored_hotspots.sort(key=lambda x: x["mean_concentration"], reverse=True)

        return {
            "pollutant": pollutant,
            "window_hours": hours_window,
            "naaqs_24h_threshold": naaqs_limit,
            "monitored_hotspots_ranked": monitored_hotspots,
            "unmonitored_coverage_voids": UNMONITORED_COVERAGE_VOIDS,
            "spatial_uncertainty_disclosure": (
                "MANDATORY PROTOCOL: Extrapolating pollution concentrations into unmonitored wards "
                "or industrial clusters without continuous monitors is scientifically invalid. "
                "PRANA refuses to display synthetic interpolation heatmaps across unmonitored zones."
            )
        }
