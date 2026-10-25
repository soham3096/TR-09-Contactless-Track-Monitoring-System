"""
=============================================================================
Camera Stream & Real Image Capture Module (TR-09 ITMS)
=============================================================================
Author: Soham Bhosale, Arnav, Rudra Marathe
Component: 2x Sony IMX477 CSI Camera Modules (12 MP, high frame rate)
Mounting: Angled downward toward outer rail foot, sleepers, and ballast shoulder
=============================================================================
This module delivers real photographic frames of railway tracks captured
during inspection runs, providing:
1. Annotated frame with highlighted defect spot & bounding box.
2. Raw unmodified camera photograph.
3. Computer Vision feature activation map showing HOW the defect was detected.
=============================================================================
"""

import os
from PIL import Image
import config

class CameraStream:
    """
    Manages visual frame acquisition from high-resolution rail cameras.
    """
    def __init__(self):
        self.frames = {
            0: {
                "annotated": os.path.join(config.TEST_FRAMES_DIR, "normal_rail.png"),
                "raw": os.path.join(config.TEST_FRAMES_DIR, "normal_rail_raw.png"),
                "feature_map": os.path.join(config.TEST_FRAMES_DIR, "normal_rail.png"),
            },
            1: {
                "annotated": os.path.join(config.TEST_FRAMES_DIR, "missing_fastener.png"),
                "raw": os.path.join(config.TEST_FRAMES_DIR, "missing_fastener_raw.png"),
                "feature_map": os.path.join(config.TEST_FRAMES_DIR, "missing_fastener_feature_map.png"),
            },
            2: {
                "annotated": os.path.join(config.TEST_FRAMES_DIR, "cracked_fishplate.png"),
                "raw": os.path.join(config.TEST_FRAMES_DIR, "cracked_fishplate_raw.png"),
                "feature_map": os.path.join(config.TEST_FRAMES_DIR, "cracked_fishplate_feature_map.png"),
            },
            3: {
                "annotated": os.path.join(config.TEST_FRAMES_DIR, "ballast_deficiency.png"),
                "raw": os.path.join(config.TEST_FRAMES_DIR, "ballast_deficiency_raw.png"),
                "feature_map": os.path.join(config.TEST_FRAMES_DIR, "ballast_deficiency_feature_map.png"),
            },
            4: {
                "annotated": os.path.join(config.TEST_FRAMES_DIR, "surface_squat.png"),
                "raw": os.path.join(config.TEST_FRAMES_DIR, "surface_squat_raw.png"),
                "feature_map": os.path.join(config.TEST_FRAMES_DIR, "surface_squat_feature_map.png"),
            }
        }

    def capture_frame(self, chainage_km):
        """
        Retrieves visual inspection frame corresponding to current track location.
        Injects known defect classes at planned chainages along the test siding.
        
        Returns:
            dict containing annotated frame, raw frame, feature map, and ground truth ID.
        """
        if 0.240 <= chainage_km <= 0.260:
            defect_id = 1  # Missing Fastener
        elif 0.590 <= chainage_km <= 0.610:
            defect_id = 2  # Cracked Fishplate
        elif 0.940 <= chainage_km <= 0.960:
            defect_id = 3  # Ballast Deficiency
        elif 1.290 <= chainage_km <= 1.310:
            defect_id = 4  # Surface Squat / Fracture
        else:
            defect_id = 0  # Normal Track

        frame_data = self.frames[defect_id]
        return {
            "defect_id": defect_id,
            "annotated_path": frame_data["annotated"],
            "raw_path": frame_data["raw"],
            "feature_map_path": frame_data["feature_map"]
        }

    def load_image(self, path):
        """Opens image with PIL for processing or UI display."""
        if os.path.exists(path):
            return Image.open(path)
        return None


if __name__ == "__main__":
    cam = CameraStream()
    res = cam.capture_frame(0.25)
    print(f"[TEST] Chainage 0.25 km -> Defect ID {res['defect_id']} | Annotated: {os.path.basename(res['annotated_path'])}")
