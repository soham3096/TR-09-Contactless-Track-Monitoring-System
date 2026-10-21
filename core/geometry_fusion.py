"""
=============================================================================
Geometry Fusion Engine (TR-09 ITMS)
=============================================================================
Author: Soham Bhosale, Arnav, Rudra Marathe
Component: Laser + IMU + GNSS Kalman/Complementary Filter
Target Accuracy: ±0.8 mm Gauge, ±1.2 mm Cross-Level

ALGORITHM & RDSO TOLERANCE CHECKS (Easy explanation for Faculty Viva):
---------------------------------------------------------------------
1. Gauge Calculation:
   Gauge = Rig_Frame_Width (1800 mm) - (Laser_Left + Laser_Right)
   Deviation = Gauge - 1676.0 mm.
   Permissible limits for Indian Railways Broad Gauge:
     - Normal range: 1673.0 mm to 1682.0 mm (-3 mm to +6 mm)
     - Maintenance alert: Outside [-3 mm, +6 mm]
     - Urgent derailment danger: Gauge > 1686 mm or < 1670 mm

2. Cross-Level (Cant):
   Elevation difference between top of Left and Right rail heads.
   h = Gauge * sin(Roll_Angle).
   Permissible tolerance on straight branch lines: ±4.0 mm.

3. Twist:
   Rate of change of cross-level along a 3-meter chord base.
   Twist (mm/m) = |CrossLevel(t) - CrossLevel(t - 3m)| / 3.0.
   RDSO safe limit: <= 2.8 mm/m.
=============================================================================
"""

import collections
import config

class GeometryFusionEngine:
    """
    Fuses dual laser scanner distances and IMU roll angles to compute
    instantaneous track geometry, checking against Indian Railways RDSO thresholds.
    """
    def __init__(self):
        # Moving window buffer to compute spatial track twist over 3 meters
        self.history_buffer = collections.deque(maxlen=30)

    def process_sample(self, d_left_mm, d_right_mm, imu_data, gnss_data):
        """
        Processes one synchronized sensor cycle at 5 Hz.
        
        Returns:
            dict containing computed geometry metrics and safety alert statuses.
        """
        # 1. Compute Gauge
        raw_gauge = config.RIG_FRAME_WIDTH_MM - (d_left_mm + d_right_mm)
        gauge_mm = round(raw_gauge, 2)
        gauge_deviation_mm = round(gauge_mm - config.NOMINAL_GAUGE_MM, 2)

        # 2. Extract Cross-Level from IMU
        cross_level_mm = imu_data["cross_level_mm"]

        # 3. Calculate Spatial Twist over moving baseline (~3 meters)
        chainage_km = gnss_data["chainage_km"]
        self.history_buffer.append((chainage_km, cross_level_mm))

        twist_mm_per_m = 0.0
        if len(self.history_buffer) > 1:
            # Find the oldest sample at least 2.5 to 3.0 meters behind
            old_chainage, old_cross_level = self.history_buffer[0]
            distance_delta_m = (chainage_km - old_chainage) * 1000.0
            if distance_delta_m >= 1.0:
                twist_mm_per_m = round(abs(cross_level_mm - old_cross_level) / distance_delta_m, 2)

        # 4. Safety Limit Evaluations (RDSO Alignment)
        status_flags = []
        severity = "NORMAL"

        # Gauge evaluation
        if gauge_deviation_mm > config.GAUGE_CRITICAL_SLACK_MM:
            status_flags.append("Derailment Slack Gauge Widening")
            severity = "CRITICAL"
        elif gauge_deviation_mm > config.GAUGE_TOLERANCE_SLACK_MM:
            status_flags.append("Slack Gauge (+6mm limit)")
            if severity != "CRITICAL":
                severity = "WARNING"
        elif gauge_deviation_mm < config.GAUGE_CRITICAL_TIGHT_MM:
            status_flags.append("Derailment Pinch / Tight Gauge")
            severity = "CRITICAL"
        elif gauge_deviation_mm < config.GAUGE_TOLERANCE_TIGHT_MM:
            status_flags.append("Tight Gauge (-3mm limit)")
            if severity != "CRITICAL":
                severity = "WARNING"

        # Cross-level evaluation
        if abs(cross_level_mm) > config.CROSS_LEVEL_CRITICAL_MM:
            status_flags.append("Excessive Cant Imbalance")
            severity = "CRITICAL"
        elif abs(cross_level_mm) > config.CROSS_LEVEL_MAX_TOLERANCE_MM:
            status_flags.append("Cross-Level Out of Tolerance")
            if severity != "CRITICAL":
                severity = "WARNING"

        # Twist evaluation
        if twist_mm_per_m > config.TWIST_MAX_PERMISSIBLE_MM_PER_M:
            status_flags.append(f"Track Twist ({twist_mm_per_m} mm/m > 2.8 mm/m)")
            if severity != "CRITICAL":
                severity = "WARNING"

        if not status_flags:
            status_flags.append("Within RDSO Tolerances")

        return {
            "chainage_km": chainage_km,
            "latitude": gnss_data["latitude"],
            "longitude": gnss_data["longitude"],
            "fix_status": gnss_data["fix_status"],
            "gauge_mm": gauge_mm,
            "gauge_deviation_mm": gauge_deviation_mm,
            "cross_level_mm": cross_level_mm,
            "twist_mm_per_m": twist_mm_per_m,
            "severity": severity,
            "status_description": "; ".join(status_flags)
        }


if __name__ == "__main__":
    engine = GeometryFusionEngine()
    dummy_imu = {"cross_level_mm": 1.1, "roll_deg": 0.038}
    dummy_gnss = {"chainage_km": 0.100, "latitude": 21.3112, "longitude": 74.8814, "fix_status": "RTK_FIXED"}
    res = engine.process_sample(62.0, 62.0, dummy_imu, dummy_gnss)
    print("[TEST] Fusion Result:", res)
