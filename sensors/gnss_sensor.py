"""
=============================================================================
RTK-GNSS Receiver Module (TR-09 ITMS)
=============================================================================
Author: Soham Bhosale, Arnav, Rudra Marathe
Component: u-blox ZED-F9P High-Precision Multi-band RTK-GNSS Receiver
Antenna: High-gain active helical antenna mounted on high-visibility mast

PURPOSE & DEAD-RECKONING FALLBACK (Easy explanation for Faculty Viva):
---------------------------------------------------------------------
1. Provides centimetre-level geo-tagging (Latitude/Longitude) for every defect.
2. In open sky, RTK achieves fixed solution ("RTK_FIXED") with sub-decimetre accuracy.
3. Fallback Mechanism:
   When moving under dense tree cover or foot overbridges, RTK fix may drop.
   TR-09 uses IMU dead-reckoning for up to 90 seconds to estimate coordinates,
   tagging events with a confidence flag so no defect location is lost.
=============================================================================
"""

import math
import random
import config

class GNSSReceiver:
    """
    Simulates high-precision RTK-GNSS positioning with dead-reckoning fallback.
    """
    def __init__(self, start_lat=config.GEO_START_LAT, start_lon=config.GEO_START_LON):
        self.current_lat = start_lat
        self.current_lon = start_lon
        self.start_lat = start_lat
        self.start_lon = start_lon
        self.chainage_km = 0.0
        self.rtk_loss_counter = 0

    def update_position(self, delta_distance_meters, force_rtk_loss=False):
        """
        Advances the trolley position along the railway line.
        
        Parameters:
            delta_distance_meters (float): Distance moved since last sample (e.g. 0.25 m).
            force_rtk_loss (bool): Simulate canopy / bridge loss.
            
        Returns:
            dict: {
                'latitude': float,
                'longitude': float,
                'chainage_km': float,
                'fix_status': str,  # 'RTK_FIXED' or 'DEAD_RECKONING'
                'satellites': int
            }
        """
        self.chainage_km += (delta_distance_meters / 1000.0)

        # Approximate coordinate shift along North-East railway bearing
        # 1 degree lat ≈ 111,000 meters
        delta_lat = (delta_distance_meters / 111000.0)
        delta_lon = (delta_distance_meters / (111000.0 * math.cos(math.radians(self.start_lat))))

        self.current_lat += delta_lat
        self.current_lon += delta_lon

        if force_rtk_loss:
            self.rtk_loss_counter += 1
            fix_status = "DEAD_RECKONING (IMU-Fallback)"
            satellites = 7
            noise = random.gauss(0.0, 0.000008)  # Slightly higher drift
        else:
            self.rtk_loss_counter = 0
            fix_status = "RTK_FIXED"
            satellites = 22
            noise = random.gauss(0.0, 0.000001)  # Centimeter precision

        return {
            "latitude": round(self.current_lat + noise, 6),
            "longitude": round(self.current_lon + noise, 6),
            "chainage_km": round(self.chainage_km, 3),
            "fix_status": fix_status,
            "satellites": satellites
        }


if __name__ == "__main__":
    gps = GNSSReceiver()
    for _ in range(5):
        pos = gps.update_position(10.0)
        print(f"[TEST] Pos: {pos['latitude']:.6f}, {pos['longitude']:.6f} | Km: {pos['chainage_km']} | Fix: {pos['fix_status']}")
