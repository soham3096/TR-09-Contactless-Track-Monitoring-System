"""
=============================================================================
Synthetic Rail Defect Image Generator (TR-09 ITMS)
=============================================================================
Author: Soham Bhosale, Arnav, Rudra Marathe
Purpose: Generates annotated visual frames representing the 4 target defect
classes + normal rail condition for simulation and faculty viva demonstrations.
=============================================================================
"""

import os
from PIL import Image, ImageDraw, ImageFont
import config

def create_synthetic_frames():
    """Generates synthetic high-contrast rail defect images."""
    os.makedirs(config.TEST_FRAMES_DIR, exist_ok=True)
    
    # Common canvas settings
    w, h = 640, 480

    # 1. NORMAL RAIL
    img = Image.new("RGB", (w, h), color=(140, 135, 125))  # Ballast background
    draw = ImageDraw.Draw(img)
    # Ballast stones texture
    for x in range(0, w, 20):
        for y in range(0, h, 20):
            draw.ellipse([x, y, x + 16, y + 14], fill=(110, 105, 95), outline=(90, 85, 80))
    # Concrete Sleeper (horizontal slab)
    draw.rectangle([60, 160, 580, 320], fill=(195, 195, 190), outline=(130, 130, 125), width=3)
    # Steel Rail (vertical band across sleeper)
    draw.rectangle([250, 0, 370, h], fill=(160, 168, 175), outline=(80, 85, 90), width=4)
    # Running head highlight
    draw.rectangle([285, 0, 335, h], fill=(215, 225, 230))
    # Elastic Rail Clip (Fastener) - intact on both sides
    draw.ellipse([215, 220, 245, 260], fill=(210, 120, 30), outline=(120, 60, 10), width=3) # Left clip
    draw.ellipse([375, 220, 405, 260], fill=(210, 120, 30), outline=(120, 60, 10), width=3) # Right clip
    # Label Banner
    draw.rectangle([0, 0, w, 40], fill=(30, 120, 30))
    draw.text((15, 10), "CLASS 0: NORMAL RAILWAY TRACK (ALL FASTENERS SECURE)", fill=(255, 255, 255))
    img.save(os.path.join(config.TEST_FRAMES_DIR, "normal_rail.png"))

    # 2. MISSING FASTENER
    img = Image.new("RGB", (w, h), color=(140, 135, 125))
    draw = ImageDraw.Draw(img)
    for x in range(0, w, 20):
        for y in range(0, h, 20):
            draw.ellipse([x, y, x + 16, y + 14], fill=(110, 105, 95), outline=(90, 85, 80))
    draw.rectangle([60, 160, 580, 320], fill=(195, 195, 190), outline=(130, 130, 125), width=3)
    draw.rectangle([250, 0, 370, h], fill=(160, 168, 175), outline=(80, 85, 90), width=4)
    draw.rectangle([285, 0, 335, h], fill=(215, 225, 230))
    # Only right clip present, left clip is MISSING (empty hole/seat)
    draw.ellipse([375, 220, 405, 260], fill=(210, 120, 30), outline=(120, 60, 10), width=3)
    # Empty fastener seat with red bounding box
    draw.rectangle([210, 215, 248, 265], outline=(255, 0, 0), width=4)
    draw.rectangle([218, 225, 240, 255], fill=(70, 70, 70))  # Empty bolt hole
    draw.rectangle([0, 0, w, 40], fill=(180, 20, 20))
    draw.text((15, 10), "CLASS 1 DEFECT: MISSING FASTENER / CLIP DETECTED (CONF: 94.6%)", fill=(255, 255, 255))
    img.save(os.path.join(config.TEST_FRAMES_DIR, "missing_fastener.png"))

    # 3. CRACKED FISHPLATE
    img = Image.new("RGB", (w, h), color=(130, 125, 120))
    draw = ImageDraw.Draw(img)
    # Rail Joint Section with heavy Steel Fishplate bar
    draw.rectangle([100, 140, 540, 340], fill=(150, 155, 160), outline=(60, 65, 70), width=4)
    # Bolts
    for bx in [150, 230, 410, 490]:
        draw.ellipse([bx, 220, bx + 35, 255], fill=(70, 75, 80), outline=(20, 20, 20), width=3)
    # Center Rail Gap (Joint expansion gap)
    draw.line([320, 100, 320, 380], fill=(20, 20, 20), width=5)
    # Fatigue Crack propagating across fishplate body
    draw.line([305, 170, 335, 215], fill=(255, 20, 20), width=4)
    draw.line([335, 215, 310, 280], fill=(255, 20, 20), width=4)
    draw.rectangle([290, 160, 350, 290], outline=(255, 0, 0), width=3)
    draw.rectangle([0, 0, w, 40], fill=(180, 20, 20))
    draw.text((15, 10), "CLASS 2 DEFECT: CRACKED FISHPLATE AT JOINT (CONF: 92.4%)", fill=(255, 255, 255))
    img.save(os.path.join(config.TEST_FRAMES_DIR, "cracked_fishplate.png"))

    # 4. BALLAST DEFICIENCY
    img = Image.new("RGB", (w, h), color=(110, 95, 80))
    draw = ImageDraw.Draw(img)
    # Sleeper unsupported by ballast (void pocket / erosion cavity)
    draw.rectangle([80, 180, 560, 300], fill=(180, 180, 175), outline=(100, 100, 95), width=3)
    draw.rectangle([260, 0, 360, h], fill=(155, 160, 165), outline=(70, 75, 80), width=4)
    # Large washed out erosion hole (dark void under rail bed)
    draw.ellipse([140, 290, 480, 450], fill=(45, 35, 25), outline=(255, 140, 0), width=4)
    draw.text((210, 360), "[BALLAST CAVITY / EROSION]", fill=(255, 200, 50))
    draw.rectangle([0, 0, w, 40], fill=(200, 90, 10))
    draw.text((15, 10), "CLASS 3 DEFECT: BALLAST DEFICIENCY NEAR CULVERT (CONF: 93.8%)", fill=(255, 255, 255))
    img.save(os.path.join(config.TEST_FRAMES_DIR, "ballast_deficiency.png"))

    # 5. SURFACE SQUAT / HEAD DEFECT
    img = Image.new("RGB", (w, h), color=(140, 135, 125))
    draw = ImageDraw.Draw(img)
    draw.rectangle([200, 0, 440, h], fill=(185, 192, 198), outline=(70, 75, 80), width=4)
    # Polished contact band
    draw.rectangle([250, 0, 390, h], fill=(225, 235, 240))
    # Rolling contact fatigue "Squat" - dark crescent indentation with microcracks
    draw.ellipse([280, 200, 360, 270], fill=(50, 45, 45), outline=(255, 0, 0), width=3)
    draw.line([270, 210, 370, 260], fill=(20, 20, 20), width=3)
    draw.rectangle([265, 185, 375, 285], outline=(255, 0, 0), width=3)
    draw.rectangle([0, 0, w, 40], fill=(180, 20, 20))
    draw.text((15, 10), "CLASS 4 DEFECT: RAIL SURFACE SQUAT / RCF INDENTATION (CONF: 95.1%)", fill=(255, 255, 255))
    img.save(os.path.join(config.TEST_FRAMES_DIR, "surface_squat.png"))

    print(f"[OK] Generated 5 synthetic rail frames in: {config.TEST_FRAMES_DIR}")

if __name__ == "__main__":
    create_synthetic_frames()
