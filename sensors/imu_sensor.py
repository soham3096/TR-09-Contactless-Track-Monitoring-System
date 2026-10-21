"""
=============================================================================
Inertial Measurement Unit (IMU) Module (TR-09 ITMS)
=============================================================================
Author: Soham Bhosale, Arnav, Rudra Marathe
Component: Bosch BMI270 (6-axis Accel/Gyro) + BMM150 (3-axis Magnetometer)
Mounting: Center of trolley frame, rigidly coupled with vibration damping pads

PHYSICS / MEASUREMENT PRINCIPLE (Easy explanation for Faculty Viva):
-------------------------------------------------------------------
1. Cross-Level (Cant / Super-elevation):
   On a straight track, both rails should be at the exact same height (0 mm difference).
   When one rail sinks or rises, the trolley tilts at an angle (roll angle theta).
   Cross-Level (h) = Gauge * sin(theta).
   For small angles: h (in mm) ≈ 1676 * radians(theta).

2. Track Vibration & Roughness:
   The Z-axis accelerometer detects dynamic vertical acceleration (G-forces).
   High spikes indicate loose ballast, joint dips, or missing sleeper support.
=============================================================================
"""

import math
import random
import config

class IMUSensor:
    """
    Simulates a 9-axis Bosch BMI270 MEMS IMU sampling roll, pitch,
    and vertical acceleration along the track.
    """
    def __init__(self):
        self.sampling_rate_hz = 200     # Hardware IMU sampling frequency
        self.gyro_bias = 0.02           # Residual drift offset (deg)

    def read_motion(self, chainage_km, inject_cant_defect=False):
        """
        Reads instantaneous IMU telemetry.
        
        Parameters:
            chainage_km (float): Track position.
            inject_cant_defect (bool): Simulate an un-level track or dip in one rail.
            
        Returns:
            dict: {
                'roll_deg': float,
                'pitch_deg': float,
                'accel_z_ms2': float,
                'cross_level_mm': float
            }
        """
        # Base track roll angle (normally close to 0 degrees on straight sections)
        base_roll = 0.0
        if inject_cant_defect:
            # Simulate a 6.5 mm elevation difference (approx 0.22 degrees tilt)
            base_roll = 0.222

        # Small MEMS noise (sigma = 0.015 degrees)
        roll_noise = random.gauss(0.0, 0.015)
        roll_deg = base_roll + roll_noise

        # Pitch (track gradient, typically ±0.1 deg on flat sidings)
        pitch_deg = round(random.gauss(0.02, 0.02), 3)

        # Vertical acceleration (gravity 9.81 m/s^2 + trolley rolling vibration)
        vibration = random.gauss(0.0, 0.15) if not inject_cant_defect else random.gauss(0.6, 0.25)
        accel_z = round(9.806 + vibration, 3)

        # Cross-level formula: h = Gauge * sin(radians(roll))
        roll_rad = math.radians(roll_deg)
        cross_level_mm = config.NOMINAL_GAUGE_MM * math.sin(roll_rad)

        return {
            "roll_deg": round(roll_deg, 4),
            "pitch_deg": pitch_deg,
            "accel_z_ms2": accel_z,
            "cross_level_mm": round(cross_level_mm, 2)
        }


if __name__ == "__main__":
    imu = IMUSensor()
    data = imu.read_motion(chainage_km=0.05)
    print(f"[TEST] IMU Roll: {data['roll_deg']}°, Cross-Level: {data['cross_level_mm']} mm, Accel-Z: {data['accel_z_ms2']} m/s²")
