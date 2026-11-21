"""
Analytics engine for pollution patterns, diurnal cycles, and statistical correlations
"""
from typing import List, Dict, Any, Optional
import numpy as np
from scipy import stats
import pandas as pd

class AnalyticsEngine:
    @staticmethod
    def calculate_diurnal_profile(observations: List[Dict[str, Any]], pollutant: str) -> List[Dict[str, Any]]:
        """
        Computes 24-hour diurnal profile (0 to 23 hrs) showing mean, min, max, and 25-75 percentiles.
        Reflects Kolkata atmospheric dynamics: morning peak (8-10am), evening/night inversion spike (8-11pm).
        """
        if not observations:
            return []

        df = pd.DataFrame(observations)
        if "pollutant" in df.columns:
            df = df[df["pollutant"] == pollutant]

        if df.empty or "observation_timestamp" not in df.columns or "normalized_value" not in df.columns:
            return []

        df["timestamp"] = pd.to_datetime(df["observation_timestamp"])
        df["hour"] = df["timestamp"].dt.hour

        hourly_stats = []
        for hour in range(24):
            hour_data = df[df["hour"] == hour]["normalized_value"]
            if not hour_data.empty:
                hourly_stats.append({
                    "hour": hour,
                    "hour_label": f"{hour:02d}:00",
                    "mean": round(float(hour_data.mean()), 2),
                    "median": round(float(hour_data.median()), 2),
                    "min": round(float(hour_data.min()), 2),
                    "max": round(float(hour_data.max()), 2),
                    "p25": round(float(hour_data.quantile(0.25)), 2),
                    "p75": round(float(hour_data.quantile(0.75)), 2),
                    "count": int(hour_data.count())
                })
            else:
                hourly_stats.append({
                    "hour": hour,
                    "hour_label": f"{hour:02d}:00",
                    "mean": 0,
                    "median": 0,
                    "min": 0,
                    "max": 0,
                    "p25": 0,
                    "p75": 0,
                    "count": 0
                })

        return hourly_stats

    @staticmethod
    def calculate_day_of_week_profile(observations: List[Dict[str, Any]], pollutant: str) -> List[Dict[str, Any]]:
        """Computes day-of-week profile (Monday to Sunday)"""
        df = pd.DataFrame(observations)
        if "pollutant" in df.columns:
            df = df[df["pollutant"] == pollutant]

        if df.empty or "observation_timestamp" not in df.columns:
            return []

        df["timestamp"] = pd.to_datetime(df["observation_timestamp"])
        df["day_name"] = df["timestamp"].dt.day_name()
        df["day_idx"] = df["timestamp"].dt.dayofweek

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dow_stats = []
        for i, d in enumerate(days):
            day_data = df[df["day_idx"] == i]["normalized_value"]
            if not day_data.empty:
                dow_stats.append({
                    "day": d,
                    "day_idx": i,
                    "mean": round(float(day_data.mean()), 2),
                    "median": round(float(day_data.median()), 2),
                    "count": int(day_data.count())
                })
            else:
                dow_stats.append({
                    "day": d,
                    "day_idx": i,
                    "mean": 0,
                    "median": 0,
                    "count": 0
                })

        return dow_stats

    @staticmethod
    def calculate_bivariate_correlation(
        x_values: List[float],
        y_values: List[float],
        var_x_name: str,
        var_y_name: str
    ) -> Dict[str, Any]:
        """
        Calculates Pearson and Spearman correlation between two continuous environmental variables.
        Returns r, p-value, sample size, and mandatory scientific caveat.
        """
        # Filter matching valid pairs
        pairs = [(x, y) for x, y in zip(x_values, y_values) if x is not None and y is not None and not np.isnan(x) and not np.isnan(y)]
        
        if len(pairs) < 10:
            return {
                "var_x": var_x_name,
                "var_y": var_y_name,
                "sample_size": len(pairs),
                "pearson_r": None,
                "pearson_p_value": None,
                "spearman_rho": None,
                "is_significant": False,
                "error": "Insufficient overlapping data points (minimum 10 required)",
                "scientific_caveat": "Correlation must never be presented as proof of causation."
            }

        xs = [p[0] for p in pairs]
        ys = [p[1] for p in pairs]

        pearson_r, pearson_p = stats.pearsonr(xs, ys)
        spearman_rho, spearman_p = stats.spearmanr(xs, ys)

        # Interpretation label
        strength = "none"
        abs_r = abs(pearson_r)
        if abs_r > 0.7:
            strength = "strong"
        elif abs_r > 0.4:
            strength = "moderate"
        elif abs_r > 0.15:
            strength = "weak"

        direction = "positive" if pearson_r >= 0 else "inverse/negative"

        return {
            "var_x": var_x_name,
            "var_y": var_y_name,
            "sample_size": len(pairs),
            "pearson_r": round(float(pearson_r), 4),
            "pearson_p_value": float(pearson_p),
            "spearman_rho": round(float(spearman_rho), 4),
            "spearman_p_value": float(spearman_p),
            "is_significant": bool(pearson_p < 0.05),
            "relationship_summary": f"{strength.capitalize()} {direction} correlation (r={pearson_r:.2f}, p={pearson_p:.4e})",
            "scientific_caveat": (
                "SCIENTIFIC RULE: Statistical correlation indicates empirical association under shared meteorological or "
                "emission conditions, but DOES NOT prove direct physical or chemical causation. Confounders such as planetary "
                "boundary layer height (PBLH) and ambient humidity frequently induce collinearity."
            ),
            "scatter_points": [{"x": round(x, 2), "y": round(y, 2)} for x, y in pairs[:200]] # capped for lightweight rendering
        }
