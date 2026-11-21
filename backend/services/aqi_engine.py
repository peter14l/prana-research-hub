"""
Indian Central Pollution Control Board (CPCB) National Air Quality Index (NAQI) Engine.

Reference:
Central Pollution Control Board (CPCB), Ministry of Environment, Forest & Climate Change,
Government of India: 'National Air Quality Index' Technical Report (2014/2015).

Rule 1: Calculation requires at least 3 pollutants, with at least ONE of them being PM2.5 or PM10.
Rule 2: Sub-index for each pollutant is calculated by linear interpolation across standard breakpoint ranges.
Rule 3: Overall AQI = max(sub_indices).
Rule 4: Dominant pollutant = pollutant with the highest sub-index.
"""
from typing import Dict, Optional, Tuple, Any

# CPCB Sub-Index Breakpoint Tables: (C_low, C_high, I_low, I_high)
# Concentrations:
# PM2.5, PM10, NO2, SO2, O3, NH3, Pb in ug/m3 (24-hr avg, except O3 8-hr/1-hr)
# CO in mg/m3 (8-hr avg)
BREAKPOINTS = {
    "PM2.5": [
        (0.0, 30.0, 0, 50),
        (30.1, 60.0, 51, 100),
        (60.1, 90.0, 101, 200),
        (90.1, 120.0, 201, 300),
        (120.1, 250.0, 301, 400),
        (250.1, 500.0, 401, 500),
    ],
    "PM10": [
        (0.0, 50.0, 0, 50),
        (50.1, 100.0, 51, 100),
        (100.1, 250.0, 101, 200),
        (250.1, 350.0, 201, 300),
        (350.1, 430.0, 301, 400),
        (430.1, 600.0, 401, 500),
    ],
    "NO2": [
        (0.0, 40.0, 0, 50),
        (40.1, 80.0, 51, 100),
        (80.1, 180.0, 101, 200),
        (180.1, 280.0, 201, 300),
        (280.1, 400.0, 301, 400),
        (400.1, 800.0, 401, 500),
    ],
    "SO2": [
        (0.0, 40.0, 0, 50),
        (40.1, 80.0, 51, 100),
        (80.1, 380.0, 101, 200),
        (380.1, 800.0, 201, 300),
        (800.1, 1600.0, 301, 400),
        (1600.1, 2000.0, 401, 500),
    ],
    "CO": [ # mg/m3
        (0.0, 1.0, 0, 50),
        (1.01, 2.0, 51, 100),
        (2.01, 10.0, 101, 200),
        (10.01, 17.0, 201, 300),
        (17.01, 34.0, 301, 400),
        (34.01, 50.0, 401, 500),
    ],
    "O3": [
        (0.0, 50.0, 0, 50),
        (50.1, 100.0, 51, 100),
        (100.1, 168.0, 101, 200),
        (168.1, 208.0, 201, 300),
        (208.1, 748.0, 301, 400),
        (748.1, 1000.0, 401, 500),
    ],
    "NH3": [
        (0.0, 200.0, 0, 50),
        (200.1, 400.0, 51, 100),
        (400.1, 800.0, 101, 200),
        (800.1, 1200.0, 201, 300),
        (1200.1, 1800.0, 301, 400),
        (1800.1, 2400.0, 401, 500),
    ]
}

def calculate_sub_index(pollutant: str, concentration: float) -> Optional[int]:
    """Calculate single pollutant sub-index via CPCB linear interpolation."""
    if pollutant not in BREAKPOINTS or concentration is None or concentration < 0:
        return None
    
    ranges = BREAKPOINTS[pollutant]
    # Check bounds
    if concentration <= 0:
        return 0

    for c_low, c_high, i_low, i_high in ranges:
        if c_low <= concentration <= c_high:
            # Linear interpolation formula: Ip = ((I_hi - I_lo) / (B_hi - B_lo)) * (Cp - B_lo) + I_lo
            sub_index = ((i_high - i_low) / (c_high - c_low)) * (concentration - c_low) + i_low
            return round(sub_index)
            
    # If concentration exceeds highest breakpoint, extrapolate based on highest category
    c_low, c_high, i_low, i_high = ranges[-1]
    if concentration > c_high:
        slope = (i_high - i_low) / (c_high - c_low)
        return round(min(500, i_low + slope * (concentration - c_low)))
        
    return None

def get_cpcb_category(aqi: int) -> Tuple[str, str]:
    """Returns Category label and color hex code per CPCB standard."""
    if aqi <= 50:
        return "Good", "#00B050"
    elif aqi <= 100:
        return "Satisfactory", "#92D050"
    elif aqi <= 200:
        return "Moderate", "#FFFF00"
    elif aqi <= 300:
        return "Poor", "#FF9900"
    elif aqi <= 400:
        return "Very Poor", "#FF0000"
    else:
        return "Severe", "#C00000"

def calculate_cpcb_aqi(pollutant_values: Dict[str, float]) -> Dict[str, Any]:
    """
    Computes official CPCB AQI from dictionary of pollutant concentrations.
    e.g. {"PM2.5": 82.4, "PM10": 164.0, "NO2": 42.1, "SO2": 14.0}
    """
    sub_indices: Dict[str, int] = {}
    
    for pollutant, value in pollutant_values.items():
        if value is not None and value >= 0:
            si = calculate_sub_index(pollutant, value)
            if si is not None:
                sub_indices[pollutant] = si
                
    # Validate CPCB minimum criteria:
    # 1. Total reporting pollutants with valid sub-index >= 3
    # 2. At least one of PM2.5 or PM10 must be present
    has_particulate = ("PM2.5" in sub_indices) or ("PM10" in sub_indices)
    valid_count = len(sub_indices)
    is_valid = (valid_count >= 3) and has_particulate
    
    if not is_valid:
        # Cannot calculate official AQI per CPCB regulations
        missing_reasons = []
        if valid_count < 3:
            missing_reasons.append(f"Requires >= 3 pollutants (found {valid_count})")
        if not has_particulate:
            missing_reasons.append("Missing required particulate matter (PM2.5 or PM10)")
            
        return {
            "aqi": None,
            "category": "Insufficient Data for Official AQI",
            "dominant_pollutant": None,
            "sub_indices": sub_indices,
            "is_valid_cpcb": False,
            "reason": "; ".join(missing_reasons),
            "methodology": "CPCB 2014 Guidelines"
        }
        
    dominant_pollutant = max(sub_indices, key=sub_indices.get)
    aqi_value = sub_indices[dominant_pollutant]
    category, color = get_cpcb_category(aqi_value)
    
    return {
        "aqi": aqi_value,
        "category": category,
        "category_color": color,
        "dominant_pollutant": dominant_pollutant,
        "sub_indices": sub_indices,
        "is_valid_cpcb": True,
        "reason": "Meets CPCB criteria (>=3 parameters including PM)",
        "methodology": "CPCB 2014 Guidelines"
    }
