"""
=============================================================================
Laser Distance Scanner Module (TR-09 ITMS)
=============================================================================
Author: Soham Bhosale, Arnav, Rudra Marathe
Component: 2x Hokuyo-class 1D/2D Laser Triangulation Scanners
Mounting: Under-chassis rigid aluminum-steel cross beam (Width: 1800 mm)

PHYSICS / MEASUREMENT PRINCIPLE (Easy explanation for Faculty Viva):
-------------------------------------------------------------------
1. Two laser sensors are mounted at opposite ends of a rigid trolley crossbar
   separated by a known fixed distance: RIG_FRAME_WIDTH = 1800 mm.
2. Laser 1 fires inward at the gauge face of the Left Rail -> measures distance d_left.
3. Laser 2 fires inward at the gauge face of the Right Rail -> measures distance d_right.
4. Nominal Broad Gauge = 1676 mm.
5. Instantaneous Track Gauge = RIG_FRAME_WIDTH - (d_left + d_right).
   Nominal: 1800 - (62.0 + 62.0) = 1676 mm.
=============================================================================
"""

import random
import config

class LaserScanner:
    """
    Simulates dual high-frequency laser distance scanners measuring
    the distances to the inner gauge faces of both rails.
    """
    def __init__(self, frame_width_mm=config.RIG_FRAME_WIDTH_MM):
        self.frame_width = frame_width_mm
        # Base nominal distance from laser mount to rail head
        self.nominal_distance_each_side = (self.frame_width - config.NOMINAL_GAUGE_MM) / 2.0  # 62.0 mm

    def read_measurements(self, chainage_km, inject_gauge_defect=False):
        """
        Takes a reading from left and right laser sensors.
        
        Parameters:
            chainage_km (float): Distance along the track in kilometers.
            inject_gauge_defect (bool): Flag to simulate slow gauge widening or pinch.
            
        Returns:
            tuple: (d_left_mm, d_right_mm)
        """
        # Small sensor measurement noise (Gaussian with sigma = 0.25 mm)
        sensor_noise_left = random.gauss(0.0, 0.25)
        sensor_noise_right = random.gauss(0.0, 0.25)
        
        # Natural track alignment micro-variations (±0.5 mm)
        track_variation = random.uniform(-0.5, 0.5)

        gauge_offset = 0.0
        if inject_gauge_defect:
            # Simulate a real-world track defect: gauge widening (+8.5 mm slack gauge)
            gauge_offset = 8.5

        # Distance from rigid trolley frame to inner rail face:
        # As gauge widens, the rail moves closer to the frame edges, so distance decreases.
        d_left = self.nominal_distance_each_side - (gauge_offset / 2.0) + track_variation + sensor_noise_left
        d_right = self.nominal_distance_each_side - (gauge_offset / 2.0) - track_variation + sensor_noise_right

        return round(d_left, 2), round(d_right, 2)

    def compute_gauge(self, d_left_mm, d_right_mm):
        """
        Calculates instantaneous track gauge from laser distance readings.
        Formula: Gauge = Frame_Width - (d_left + d_right)
        """
        gauge = self.frame_width - (d_left_mm + d_right_mm)
        return round(gauge, 2)


if __name__ == "__main__":
    # Self-test block for quick verification
    scanner = LaserScanner()
    d_l, d_r = scanner.read_measurements(chainage_km=0.1)
    g = scanner.compute_gauge(d_l, d_r)
    print(f"[TEST] Left Laser: {d_l} mm, Right Laser: {d_r} mm -> Computed Gauge: {g} mm (Nominal: 1676 mm)")
