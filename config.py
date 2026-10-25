"""
=============================================================================
TR-09 ITMS: Contactless Integrated Track Monitoring System
Configuration & Standard Engineering Parameters
Author: Soham Bhosale, Arnav, Rudra Marathe (MPSTME, NMIMS)
=============================================================================
This file defines all standard railway geometry tolerances, sensor calibration
offsets, defect classification labels, detection mechanisms, and damage models
in alignment with Research Designs and Standards Organisation (RDSO) standards.
"""

import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
TEST_FRAMES_DIR = os.path.join(DATA_DIR, "test_frames")
LOGS_DIR = os.path.join(DATA_DIR, "inspection_logs")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

os.makedirs(TEST_FRAMES_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# -------------------------------------------------------------------------
# 1. TRACK GEOMETRY STANDARDS (Indian Railways Broad Gauge: 1676 mm)
# -------------------------------------------------------------------------
NOMINAL_GAUGE_MM = 1676.0            # Standard Broad Gauge in India
RIG_FRAME_WIDTH_MM = 1800.0          # Distance between the two laser sensor heads

# RDSO Permissible Tolerance Limits (mm)
GAUGE_TOLERANCE_TIGHT_MM = -3.0      # Lower acceptable gauge: 1673.0 mm
GAUGE_TOLERANCE_SLACK_MM = +6.0      # Upper acceptable gauge: 1682.0 mm
GAUGE_CRITICAL_TIGHT_MM = -6.0       # Urgent maintenance required: 1670.0 mm
GAUGE_CRITICAL_SLACK_MM = +10.0      # Derailment risk limit: 1686.0 mm

# Cross-Level (Cant / Super-elevation) Tolerances (mm)
CROSS_LEVEL_TARGET_ACCURACY = 1.2    # Target ITMS measurement accuracy (±1.2 mm)
CROSS_LEVEL_MAX_TOLERANCE_MM = 4.0   # Permissible deviation on straight track
CROSS_LEVEL_CRITICAL_MM = 8.0        # Critical twist/cant warning threshold

# Twist Tolerance (mm per meter over a 3.0-meter chord base)
TWIST_BASE_CHORD_M = 3.0             # Base length for twist calculation
TWIST_MAX_PERMISSIBLE_MM_PER_M = 2.8 # RDSO limit: 2.8 mm/m

# -------------------------------------------------------------------------
# 2. DEFECT CLASSIFICATION, DETECTION MECHANISMS & DAMAGE ANALYSIS
# -------------------------------------------------------------------------
DEFECT_CLASSES = {
    0: "Normal Rail (No Defect)",
    1: "Missing Fastener (ERC)",
    2: "Cracked Fishplate",
    3: "Ballast Deficiency",
    4: "Surface Squat / Rail Head Defect"
}

# Rich Engineering Profiles for each Defect Class
DEFECT_DETAILS = {
    0: {
        "name": "Normal Rail Condition",
        "detection_method": "Edge continuity & template correlation confirm intact Elastic Rail Clips, uniform ballast shoulder, and smooth running crown.",
        "damage_description": "Track is in nominal condition with zero structural degradation.",
        "derailment_risk": "None (Safe operating state under line speed).",
        "pway_action": "Routine periodic inspection per P-Way schedule.",
        "bounding_box": None
    },
    1: {
        "name": "Missing Fastener (Elastic Rail Clip)",
        "detection_method": "Contour Discontinuity & Intensity Gradient: Expected circular loop of Mark-III Elastic Rail Clip absent at coordinates (X: 330-520, Y: 240-440); bare anchor shoulder exposed with high shadow variance.",
        "damage_description": "The elastic clip is missing or dislodged from the concrete sleeper seat, leaving the outer rail foot unclamped with loss of vertical and lateral toe load (nominal 850–1100 kgf missing).",
        "derailment_risk": "High Risk: Progressive dynamic gauge widening under lateral wheel flange thrust during train passage, leading to potential flange-climb derailment.",
        "pway_action": "Immediate replacement with new Mark-III ERC clip and rubber pad within 24 hours.",
        "bounding_box": (330, 240, 520, 440)
    },
    2: {
        "name": "Cracked Fishplate at Rail Joint",
        "detection_method": "High-Frequency Edge Gradient & Line Segment Detection: Transverse fatigue fracture line (aperture width ~2.1 mm) detected propagating across the middle bolt-hole zone at coordinates (X: 280-540, Y: 210-430).",
        "damage_description": "Fatigue fracture propagating through the structural web of the steel joint bar, causing severe loss of flexural stiffness and vertical joint alignment.",
        "derailment_risk": "Critical Derailment Hazard: Complete structural break of fishplate leads to dipped joint, severe dynamic impact, rail end fracture, and wheel derailment at speed.",
        "pway_action": "Impose 30 km/h temporary speed restriction; emergency fishplate replacement and ultrasonic joint testing.",
        "bounding_box": (280, 210, 540, 430)
    },
    3: {
        "name": "Ballast Deficiency / Washout Void",
        "detection_method": "Spatial Texture Granularity & Shadow Mask Analysis: Dark cavity void area (>0.42 m²) detected under sleeper underside at coordinates (X: 220-620, Y: 260-520) with loss of crushed stone interlocking.",
        "damage_description": "Water erosion or settlement has washed away ballast packing beneath the sleeper, creating an unsupported hollow void (sleeper hanging in air).",
        "derailment_risk": "Severe Track Geometry Hazard: Dynamic sleeper pumping under heavy axle loads causes localized differential settlement, excessive cant error, and dangerous track twist (> 2.8 mm/m).",
        "pway_action": "Deploy manual/mechanized tamping gang, ballast stone dumping, and drainage culvert clearance.",
        "bounding_box": (220, 260, 620, 520)
    },
    4: {
        "name": "Rail Head Surface Squat / Fracture",
        "detection_method": "Surface Reflectance Gradient & CNN Defect Activation: Dark crescent-shaped rolling contact fatigue (RCF) indentation (area: ~34 mm²) detected on polished rail running surface at coordinates (X: 300-560, Y: 180-420).",
        "damage_description": "Severe Rolling Contact Fatigue (RCF) resulting in subsurface micro-cracks that propagate downward at ~20° angle into the rail crown with metal shelling and surface depression.",
        "derailment_risk": "Critical Rail Break Hazard: Fatigue crack can turn downward into a transverse fracture, snapping the rail head under heavy freight wheel loads.",
        "pway_action": "Immediate rail testing with dye-penetrant/ultrasonic probe; rail profile grinding or emergency rail renewal.",
        "bounding_box": (300, 180, 560, 420)
    }
}

# Edge AI confidence threshold for emitting critical alert
CONFIDENCE_THRESHOLD = 0.91          # Minimum 91% confidence required to emit event

# -------------------------------------------------------------------------
# 3. TROLLEY OPERATIONAL PARAMETERS
# -------------------------------------------------------------------------
DEFAULT_TROLLEY_SPEED_KMH = 4.5      # Typical walking speed (1.25 m/s)
SAMPLING_FREQUENCY_HZ = 5            # Fused event stream rate (5 Hz = 5 samples/sec)
BATTERY_CAPACITY_AH = 18.0           # 12V 18Ah LiFePO4 battery (~7 hours runtime)
TOTAL_POWER_DRAW_W = 24.8            # Total max power consumption (24.8 Watts)

# -------------------------------------------------------------------------
# 4. TELEMETRY & DATA RETENTION
# -------------------------------------------------------------------------
LOCAL_LOG_FILE = os.path.join(LOGS_DIR, "live_inspection_log.csv")
DEFECT_EVENTS_FILE = os.path.join(LOGS_DIR, "detected_defects.json")
GEO_START_LAT = 21.3112              # Shirpur test siding latitude
GEO_START_LON = 74.8814              # Shirpur test siding longitude
