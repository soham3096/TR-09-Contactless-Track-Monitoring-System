"""
=============================================================================
Camera Stream & Image Capture Module (TR-09 ITMS)
=============================================================================
Author: Soham Bhosale, Arnav, Rudra Marathe
Component: 2x Sony IMX477 CSI Camera Modules (12 MP, high frame rate)
Mounting: Angled downward toward outer rail foot and sleeper fasteners

PURPOSE (Easy explanation for Faculty Viva):
-------------------------------------------
1. Captures continuous video frames of rail surface and sleeper fasteners.
2. In real operation on Jetson Orin Nano, frames are captured via OpenCV GStreamer.
3. In this reference implementation, it delivers high-resolution visual frames
   mapped to track chainages for defect classification.
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
        self.frame_files = {
            "normal": os.path.join(config.TEST_FRAMES_DIR, "normal_rail.png"),
            "missing_fastener": os.path.join(config.TEST_FRAMES_DIR, "missing_fastener.png"),
            "cracked_fishplate": os.path.join(config.TEST_FRAMES_DIR, "cracked_fishplate.png"),
            "ballast_deficiency": os.path.join(config.TEST_FRAMES_DIR, "ballast_deficiency.png"),
            "surface_squat": os.path.join(config.TEST_FRAMES_DIR, "surface_squat.png"),
        }

    def capture_frame(self, chainage_km):
        """
        Retrieves visual inspection frame corresponding to current track location.
        Injects known defect classes at planned chainages along the test siding.
        
        Returns:
            tuple: (frame_path, simulated_ground_truth_label)
        """
        # Planned defect zones along 1.5 km test track
        if 0.240 <= chainage_km <= 0.260:
            return self.frame_files["missing_fastener"], 1
        elif 0.590 <= chainage_km <= 0.610:
            return self.frame_files["cracked_fishplate"], 2
        elif 0.940 <= chainage_km <= 0.960:
            return self.frame_files["ballast_deficiency"], 3
        elif 1.290 <= chainage_km <= 1.310:
            return self.frame_files["surface_squat"], 4
        else:
            return self.frame_files["normal"], 0

    def load_image(self, path):
        """Opens image with PIL for processing or UI display."""
        if os.path.exists(path):
            return Image.open(path)
        return None


if __name__ == "__main__":
    cam = CameraStream()
    p, label = cam.capture_frame(0.25)
    print(f"[TEST] Chainage 0.25 km -> Frame: {os.path.basename(p)}, Target Class: {config.DEFECT_CLASSES[label]}")
