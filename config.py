"""
=============================================================================
TR-09 ITMS: Contactless Integrated Track Monitoring System
Configuration & Standard Engineering Parameters
Author: Soham Bhosale, Arnav, Rudra Marathe (MPSTME, NMIMS)
=============================================================================
This file defines all standard railway geometry tolerances, sensor calibration
offsets, defect classification labels, and telemetry parameters in alignment
with Research Designs and Standards Organisation (RDSO) Indian Railways standards.
"""

import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
TEST_FRAMES_DIR = os.path.join(DATA_DIR, "test_frames")
LOGS_DIR = os.path.join(DATA_DIR, "inspection_logs")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Ensure required directories exist
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
# 2. DEFECT CLASSIFICATION CLASSES & THRESHOLDS
# -------------------------------------------------------------------------
DEFECT_CLASSES = {
    0: "Normal Rail (No Defect)",
    1: "Missing Fastener (ERC)",
    2: "Cracked Fishplate",
    3: "Ballast Deficiency",
    4: "Surface Squat / Rail Head Defect"
}

# Edge AI confidence threshold for emitting critical alert (from project brief)
CONFIDENCE_THRESHOLD = 0.91          # Minimum 91% confidence required to emit event

# -------------------------------------------------------------------------
# 3. TROLLEY OPERATIONAL PARAMETERS
# -------------------------------------------------------------------------
DEFAULT_TROLLEY_SPEED_KMH = 4.5      # Typical walking speed (1.25 m/s)
SAMPLING_FREQUENCY_HZ = 5            # Fused event stream rate (5 Hz = 5 samples/sec)
BATTERY_CAPACITY_AH = 18.0           # 12V 18Ah LiFePO4 battery (~7 hours runtime)
TOTAL_POWER_DRAW_W = 26.0            # Total max power consumption (26 Watts)

# -------------------------------------------------------------------------
# 4. TELEMETRY & DATA RETENTION
# -------------------------------------------------------------------------
LOCAL_LOG_FILE = os.path.join(LOGS_DIR, "live_inspection_log.csv")
DEFECT_EVENTS_FILE = os.path.join(LOGS_DIR, "detected_defects.json")
GEO_START_LAT = 21.3112              # Shirpur test siding latitude
GEO_START_LON = 74.8814              # Shirpur test siding longitude
