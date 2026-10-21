"""
=============================================================================
TR-09 ITMS: Contactless Integrated Track Monitoring System
Primary Project Entry Point
=============================================================================
Course: Design Experience (MBA Tech & B.Tech CE - 2nd Year)
Institute: SVKM's NMIMS MPSTME, Shirpur
Team: Soham Bhosale | Arnav | Rudra Marathe
Mentor: Prof. Chaitali Patil

USAGE:
  python main.py         -> Launches the Native Desktop Inspection GUI Application
  python main.py --cli   -> Runs fast simulation in Terminal CLI mode
=============================================================================
"""

import sys
import time
import os
import config
from sensors.laser_scanner import LaserScanner
from sensors.imu_sensor import IMUSensor
from sensors.gnss_sensor import GNSSReceiver
from sensors.camera_stream import CameraStream
from core.geometry_fusion import GeometryFusionEngine
from core.defect_detector import RailDefectDetector
from core.telemetry import TelemetryEngine

def run_cli_simulation(total_distance_km=1.5, step_meters=25.0, sleep_delay_sec=0.04):
    """Runs a simulated inspection run along 1.5 km railway siding in terminal."""
    print("\n" + "="*75)
    print("  TR-09: INDIGENOUS CONTACTLESS INTEGRATED TRACK MONITORING SYSTEM")
    print("  SVKM's NMIMS MPSTME - Design Experience Course Project")
    print("  Team: Soham Bhosale | Arnav | Rudra Marathe (Guidance: Prof. Chaitali Patil)")
    print("="*75)
    print(f"[*] Initializing Sensor Subsystems on NVIDIA Jetson Edge Platform...")

    laser = LaserScanner()
    imu = IMUSensor()
    gnss = GNSSReceiver()
    camera = CameraStream()
    fusion = GeometryFusionEngine()
    detector = RailDefectDetector()
    telemetry = TelemetryEngine()

    print(f"[+] Laser Scanners calibrated (Base Width: {config.RIG_FRAME_WIDTH_MM} mm)")
    print(f"[+] Bosch BMI270 9-Axis IMU connected (200 Hz Sampling)")
    print(f"[+] u-blox ZED-F9P RTK-GNSS synced (Start GPS: {config.GEO_START_LAT}, {config.GEO_START_LON})")
    print(f"[+] Sony IMX477 CSI Camera ready (Defect Threshold: {config.CONFIDENCE_THRESHOLD*100}%)")
    print(f"[+] Persistent Local Buffer active: {config.LOCAL_LOG_FILE}")
    print("="*75)
    print(f"[*] Starting Trolley Push Inspection: 0.000 km to {total_distance_km:.3f} km")
    print(f"{'KM':<8} | {'GAUGE':<10} | {'DEV':<8} | {'CROSS-LVL':<10} | {'TWIST':<9} | {'GPS STATUS':<16} | {'DEFECT ALERT'}")
    print("-" * 95)

    defects_count = 0
    warnings_count = 0
    current_km = 0.0

    while current_km <= total_distance_km:
        inject_gauge_widening = (0.840 <= current_km <= 0.880)
        inject_cant = (0.420 <= current_km <= 0.450)
        simulate_rtk_loss = (1.100 <= current_km <= 1.180)

        dl, dr = laser.read_measurements(current_km, inject_gauge_defect=inject_gauge_widening)
        imu_data = imu.read_motion(current_km, inject_cant_defect=inject_cant)
        gnss_data = gnss.update_position(step_meters, force_rtk_loss=simulate_rtk_loss)
        current_km = gnss_data["chainage_km"]

        geo_result = fusion.process_sample(dl, dr, imu_data, gnss_data)
        frame_path, simulated_class = camera.capture_frame(current_km)
        defect_result = detector.analyze_frame(frame_path, simulated_class)
        telemetry.log_record(geo_result, defect_result, lte_online=not simulate_rtk_loss)

        gauge_str = f"{geo_result['gauge_mm']:.1f} mm"
        dev_str = f"{geo_result['gauge_deviation_mm']:+.1f} mm"
        cross_str = f"{geo_result['cross_level_mm']:+.1f} mm"
        twist_str = f"{geo_result['twist_mm_per_m']:.1f} mm/m"
        fix_str = "RTK_FIX" if "FIXED" in gnss_data["fix_status"] else "IMU_FALLBACK"

        defect_msg = "CLEAR"
        if defect_result["detected"]:
            defects_count += 1
            defect_msg = f"[!] {defect_result['defect_name']} ({defect_result['confidence']*100:.1f}%)"
        elif geo_result["severity"] != "NORMAL":
            warnings_count += 1
            defect_msg = f"[*] {geo_result['status_description'][:32]}"

        print(f"Km {current_km:<5.3f} | {gauge_str:<10} | {dev_str:<8} | {cross_str:<10} | {twist_str:<9} | {fix_str:<16} | {defect_msg}")
        time.sleep(sleep_delay_sec)

    print("="*95)
    print("  INSPECTION RUN COMPLETE - SUMMARY OF FINDINGS")
    print("="*95)
    print(f"  • Total Track Inspected    : {current_km:.3f} km")
    print(f"  • Total Defects Detected   : {defects_count} visual defects")
    print(f"  • Geometry Warnings Raised : {warnings_count} geometry out-of-tolerance events")
    print(f"  • Output CSV Log File      : {config.LOCAL_LOG_FILE}")
    print(f"  • Defect Database JSON     : {config.DEFECT_EVENTS_FILE}")
    print("="*95 + "\n")


def main():
    if "--cli" in sys.argv or "--headless" in sys.argv:
        run_cli_simulation()
    else:
        # Default behavior: Launch Native Desktop GUI Application
        try:
            from gui_app import main as gui_main
            print("[*] Launching TR-09 Desktop GUI Application...")
            gui_main()
        except Exception as e:
            print(f"[!] GUI failed to launch ({e}). Falling back to CLI mode...")
            run_cli_simulation()


if __name__ == "__main__":
    main()
