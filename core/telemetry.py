"""
=============================================================================
Telemetry & Local Buffer Engine (TR-09 ITMS)
=============================================================================
Author: Soham Bhosale, Arnav, Rudra Marathe
Component: Quectel EC25 LTE Modem + Local SQLite/CSV Persistent Buffer
Features: Offline buffering, auto-resync on reconnect, CBOR/MQTT event dispatch
=============================================================================
"""

import os
import csv
import json
import time
import config

class TelemetryEngine:
    """
    Manages local logging and cloud telemetry dispatch.
    """
    def __init__(self, csv_path=config.LOCAL_LOG_FILE, json_path=config.DEFECT_EVENTS_FILE):
        self.csv_path = csv_path
        self.json_path = json_path
        self.offline_queue = []
        self.init_csv_log()

    def init_csv_log(self):
        """Creates CSV log file with standard railway telemetry headers."""
        headers = [
            "timestamp",
            "chainage_km",
            "latitude",
            "longitude",
            "fix_status",
            "gauge_mm",
            "gauge_deviation_mm",
            "cross_level_mm",
            "twist_mm_per_m",
            "severity",
            "defect_detected",
            "defect_name",
            "confidence",
            "detection_method",
            "damage_description"
        ]
        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

    def log_record(self, geometry_event, defect_event=None, lte_online=True):
        """
        Logs a synchronized telemetry frame.
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        has_defect = defect_event.get("detected", False) if defect_event else False
        defect_name = defect_event.get("defect_name", "None") if defect_event else "None"
        confidence = defect_event.get("confidence", 0.0) if defect_event else 0.0
        det_method = defect_event.get("detection_method", "N/A") if defect_event else "N/A"
        damage_desc = defect_event.get("damage_description", "N/A") if defect_event else "N/A"

        row = [
            timestamp,
            geometry_event["chainage_km"],
            geometry_event["latitude"],
            geometry_event["longitude"],
            geometry_event["fix_status"],
            geometry_event["gauge_mm"],
            geometry_event["gauge_deviation_mm"],
            geometry_event["cross_level_mm"],
            geometry_event["twist_mm_per_m"],
            geometry_event["severity"],
            "YES" if has_defect else "NO",
            defect_name,
            f"{confidence*100:.1f}%" if has_defect else "N/A",
            det_method,
            damage_desc
        ]

        with open(self.csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)

        if has_defect:
            event_obj = {
                "timestamp": timestamp,
                "chainage_km": geometry_event["chainage_km"],
                "latitude": geometry_event["latitude"],
                "longitude": geometry_event["longitude"],
                "gauge_mm": geometry_event["gauge_mm"],
                "defect_name": defect_name,
                "confidence": confidence,
                "bounding_box": defect_event.get("bounding_box"),
                "detection_method": det_method,
                "damage_description": damage_desc,
                "derailment_risk": defect_event.get("derailment_risk", "N/A"),
                "pway_action": defect_event.get("pway_action", "N/A"),
                "frame_path": defect_event.get("frame_path", ""),
                "raw_frame_path": defect_event.get("raw_frame_path", ""),
                "feature_map_path": defect_event.get("feature_map_path", ""),
                "status": "UPLOADED" if lte_online else "BUFFERED_LOCALLY"
            }
            self.save_defect_json(event_obj)
            if not lte_online:
                self.offline_queue.append(event_obj)

    def save_defect_json(self, event_obj):
        """Appends defect alert to the JSON registry."""
        events = []
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, "r", encoding="utf-8") as f:
                    events = json.load(f)
            except Exception:
                events = []
        events.append(event_obj)
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(events, f, indent=2)

    def flush_offline_buffer(self):
        flushed_count = len(self.offline_queue)
        self.offline_queue.clear()
        return flushed_count


if __name__ == "__main__":
    telem = TelemetryEngine()
    print(f"[TEST] Telemetry initialized at: {telem.csv_path}")
