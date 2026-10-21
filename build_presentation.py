"""
=============================================================================
Professional Engineering Presentation Generator (.pptx)
TR-09: Development of Indigenous Contactless Integrated Track Monitoring Systems
SVKM's NMIMS MPSTME, Shirpur • Design Experience Course Project
Authors: Soham Bhosale, Arnav, Rudra Marathe | Mentor: Prof. Chaitali Patil
=============================================================================
"""

import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Color Palette Constants
NAVY = RGBColor(0x1B, 0x36, 0x5D)
SLATE_BLUE = RGBColor(0x2B, 0x6C, 0xB0)
DARK_TEXT = RGBColor(0x2D, 0x37, 0x48)
MUTED_TEXT = RGBColor(0x71, 0x80, 0x96)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_BG = RGBColor(0xF8, 0xFA, 0xFC)
CARD_BG = RGBColor(0xED, 0xF2, 0xF7)
CARD_BORDER = RGBColor(0xCB, 0xD5, 0xE0)
RED_ACCENT = RGBColor(0xC6, 0x28, 0x28)
GREEN_ACCENT = RGBColor(0x2E, 0x7D, 0x32)

def create_header(slide, title_text, category_text="TR-09 ITMS | MPSTME NMIMS"):
    """Adds a standard professional header banner to content slides."""
    # Top banner bar
    banner = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
    banner.fill.solid()
    banner.fill.fore_color.rgb = NAVY
    banner.line.color.rgb = NAVY

    # Category / breadcrumb text
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.5), Inches(0.3))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.name = "Calibri"
    p_cat.font.size = Pt(9.5)
    p_cat.font.bold = True
    p_cat.font.color.rgb = RGBColor(0x63, 0xB3, 0xED)

    # Main slide title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.5), Inches(0.6))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = "Calibri"
    p_title.font.size = Pt(20)
    p_title.font.bold = True
    p_title.font.color.rgb = WHITE

def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
    """Draws a rounded rectangular background card for structured layout."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1)
    return card

def build_presentation(output_filename="TR-09_ITMS_Presentation.pptx"):
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.color.rgb = NAVY

    # Institute Logo
    logo_path = os.path.join("assets", "nmims_logo.png")
    if os.path.exists(logo_path):
        s1.shapes.add_picture(logo_path, Inches(0.8), Inches(0.8), width=Inches(1.8))

    # Institute Text
    inst_box = s1.shapes.add_textbox(Inches(2.8), Inches(0.85), Inches(9.5), Inches(1.0))
    tf_inst = inst_box.text_frame
    p_i1 = tf_inst.paragraphs[0]
    p_i1.text = "SVKM'S Narsee Monjee Institute of Management Studies"
    p_i1.font.name = "Calibri"
    p_i1.font.size = Pt(15)
    p_i1.font.bold = True
    p_i1.font.color.rgb = RGBColor(0xEB, 0xF8, 0xFF)

    p_i2 = tf_inst.add_paragraph()
    p_i2.text = "Mukesh Patel School of Technology Management & Engineering (Shirpur Campus)"
    p_i2.font.name = "Calibri"
    p_i2.font.size = Pt(12)
    p_i2.font.color.rgb = RGBColor(0xCB, 0xD5, 0xE0)

    # Title & Subtitle Card
    title_card = add_card(s1, Inches(0.8), Inches(2.2), Inches(11.733), Inches(2.4), bg_color=RGBColor(0x23, 0x44, 0x76), border_color=RGBColor(0x31, 0x82, 0xCE))
    t_box = s1.shapes.add_textbox(Inches(1.1), Inches(2.35), Inches(11.1), Inches(2.0))
    tf_t = t_box.text_frame
    p_t = tf_t.paragraphs[0]
    p_t.text = "Development of Indigenous Contactless Integrated\nTrack Monitoring Systems (ITMS)"
    p_t.font.name = "Calibri"
    p_t.font.size = Pt(26)
    p_t.font.bold = True
    p_t.font.color.rgb = WHITE

    p_sub = tf_t.add_paragraph()
    p_sub.text = "TR-09 Prototype: Architecture, Working Principle, and Technical Validation"
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(15)
    p_sub.font.bold = True
    p_sub.font.color.rgb = RGBColor(0x63, 0xB3, 0xED)

    # Metadata Row (Course & Authors)
    m_box = s1.shapes.add_textbox(Inches(0.8), Inches(4.8), Inches(11.733), Inches(2.2))
    tf_m = m_box.text_frame
    
    p_c = tf_m.paragraphs[0]
    p_c.text = "Course: Design Experience  |  Programme: MBA Tech & B.Tech Computer Engineering (2nd Year)  |  Batch: 2024–2029"
    p_c.font.name = "Calibri"
    p_c.font.size = Pt(12)
    p_c.font.bold = True
    p_c.font.color.rgb = RGBColor(0xEB, 0xF8, 0xFF)

    p_auth = tf_m.add_paragraph()
    p_auth.text = "Project Team:  Soham Bhosale  •  Arnav  •  Rudra Marathe"
    p_auth.font.name = "Calibri"
    p_auth.font.size = Pt(13)
    p_auth.font.bold = True
    p_auth.font.color.rgb = WHITE

    p_guide = tf_m.add_paragraph()
    p_guide.text = "Under the Guidance of: Prof. Chaitali Patil (Department of Computer Engineering, MPSTME)"
    p_guide.font.name = "Calibri"
    p_guide.font.size = Pt(12)
    p_guide.font.color.rgb = RGBColor(0x90, 0xCD, 0xF4)

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    create_header(s2, "Problem Statement & Project Motivation", "01. Introduction")

    # 3 Stat Cards Across Top
    stat_data = [
        ("68,000+ km", "Operational Track Network", "Carrying 24 million passengers and 3.5 million tonnes freight daily."),
        ("19% Derailments", "Track Geometry Cause", "Linked directly to gauge widening, twist, and loose fasteners (2019–2024)."),
        ("35% Branch Lines", "Un-Instrumented Gap", "Over 24,000 km rarely visited by ₹38-Crore imported recording coaches.")
    ]
    for idx, (stat, title, desc) in enumerate(stat_data):
        cx = Inches(0.8 + idx * 4.0)
        add_card(s2, cx, Inches(1.4), Inches(3.7), Inches(2.2), bg_color=CARD_BG, border_color=CARD_BORDER)
        c_box = s2.shapes.add_textbox(cx + Inches(0.2), Inches(1.5), Inches(3.3), Inches(2.0))
        tf = c_box.text_frame
        p1 = tf.paragraphs[0]
        p1.text = stat
        p1.font.name = "Calibri"
        p1.font.size = Pt(24)
        p1.font.bold = True
        p1.font.color.rgb = RED_ACCENT if idx == 1 else NAVY

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.name = "Calibri"
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = DARK_TEXT

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.name = "Calibri"
        p3.font.size = Pt(10)
        p3.font.color.rgb = MUTED_TEXT

    # Lower Card: The Critical Gap
    gap_card = add_card(s2, Inches(0.8), Inches(3.9), Inches(11.733), Inches(3.1), bg_color=WHITE, border_color=SLATE_BLUE)
    g_box = s2.shapes.add_textbox(Inches(1.1), Inches(4.1), Inches(11.1), Inches(2.7))
    tf_g = g_box.text_frame
    
    p_gt = tf_g.paragraphs[0]
    p_gt.text = "The Real-World Challenge on Indian Railways Branch Lines:"
    p_gt.font.name = "Calibri"
    p_gt.font.size = Pt(14)
    p_gt.font.bold = True
    p_gt.font.color.rgb = NAVY

    bullets = [
        "Prohibitive Import Costs: Imported Track Recording Cars (Plasser EM-120) cost ≈ ₹38 Crore each and depend on foreign spares.",
        "Manual Foot Patrol Limitations: P-Way gangs walk 8–10 km sections every 8–9 days using manual gauge sticks and physical registers.",
        "Invisible Failure Modes: Progressive track widening (1–2 mm/year) and microscopic fatigue cracks cannot be seen by walking inspectors.",
        "The TR-09 Solution: An indigenous, contactless inspector bolted onto existing manual push trolleys for under ₹1.35 Lakhs."
    ]
    for b in bullets:
        pb = tf_g.add_paragraph()
        pb.text = "• " + b
        pb.font.name = "Calibri"
        pb.font.size = Pt(11)
        pb.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 3: OBJECTIVES & TARGET BENCHMARKS
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    create_header(s3, "Project Objectives & Engineering Benchmarks", "02. Project Scope")

    objs = [
        ("Sub-Millimetre Geometry Accuracy", "±0.8 mm Gauge Accuracy\n±1.2 mm Cross-Level Accuracy", "Continuous broad gauge (1676 mm) profiling using dual optical laser triangulation without physical rail contact."),
        ("Deep Learning Defect Detection", "≥ 91% Precision Gate\n≥ 87% Defect Recall", "Real-time edge detection of 4 primary defect classes: Missing Fasteners, Cracked Fishplates, Ballast Voids, and Squats."),
        ("Budget Hard Cap (< ₹1.35 L)", "₹1,35,500 Total Cost\n100% Indian Components", "Full bill of materials sourced strictly through Indian electronics distributors with zero dependency on foreign spares."),
        ("Local-First Resilient Telemetry", "32 GB On-Device Buffer\n90s Dead-Reckoning Fallback", "Zero telemetry loss in rural cutting blackouts with automatic FIFO cloud sync when 4G LTE connection restores.")
    ]
    for i, (title, highlight, desc) in enumerate(objs):
        row = i // 2
        col = i % 2
        bx = Inches(0.8 + col * 6.0)
        by = Inches(1.5 + row * 2.8)
        add_card(s3, bx, by, Inches(5.7), Inches(2.5), bg_color=WHITE, border_color=SLATE_BLUE)
        
        box = s3.shapes.add_textbox(bx + Inches(0.2), by + Inches(0.15), Inches(5.3), Inches(2.2))
        tf = box.text_frame
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Calibri"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = NAVY

        p2 = tf.add_paragraph()
        p2.text = highlight
        p2.font.name = "Calibri"
        p2.font.size = Pt(11.5)
        p2.font.bold = True
        p2.font.color.rgb = GREEN_ACCENT

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.name = "Calibri"
        p3.font.size = Pt(10)
        p3.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE & HARDWARE
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    create_header(s4, "System Architecture & Hardware Integration", "03. Engineering Design")

    # Left: Image
    fig1 = os.path.join("assets", "fig1_system_architecture.png")
    if os.path.exists(fig1):
        s4.shapes.add_picture(fig1, Inches(0.8), Inches(1.5), width=Inches(6.8))

    # Right: Specifications Card
    add_card(s4, Inches(7.8), Inches(1.5), Inches(4.7), Inches(5.5), bg_color=CARD_BG, border_color=CARD_BORDER)
    s_box = s4.shapes.add_textbox(Inches(8.0), Inches(1.65), Inches(4.3), Inches(5.2))
    tf_s = s_box.text_frame
    
    ps_head = tf_s.paragraphs[0]
    ps_head.text = "Subsystem Specifications"
    ps_head.font.name = "Calibri"
    ps_head.font.size = Pt(14)
    ps_head.font.bold = True
    ps_head.font.color.rgb = NAVY

    specs = [
        ("Rig Chassis:", "Lightweight steel hand-trolley mount (14.6 kg total loaded payload)."),
        ("Optical Sensors:", "2x Hokuyo-class laser scanners mounted on 1800 mm aluminum crossbar (40 Hz)."),
        ("Inertial Unit:", "Bosch BMI270 9-axis IMU (200 Hz hardware sampling) with Sorbothane damping."),
        ("Navigation:", "u-blox ZED-F9P Multi-Band RTK-GNSS (<0.05 m accuracy) + 90s Dead-Reckoning."),
        ("Cameras:", "Dual Sony IMX477 CSI 12 MP modules capturing sleeper fastener imagery."),
        ("Edge Compute:", "NVIDIA Jetson Orin Nano (8 GB, 17 TOPS INT8 edge AI, 9 W nominal draw)."),
        ("Battery Pack:", "12V 18Ah LiFePO₄ pack providing 7.2 hours continuous operation (24.8 W load).")
    ]
    for lbl, val in specs:
        p = tf_s.add_paragraph()
        r1 = p.add_run()
        r1.text = lbl + " "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = NAVY
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 5: BILL OF MATERIALS (BOM)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    create_header(s5, "Engineering Bill of Materials (Hard Budget: ₹1.35 Lakhs)", "04. Cost Engineering")

    # Table
    rows = 11
    cols = 4
    left = Inches(0.8)
    top = Inches(1.4)
    width = Inches(11.733)
    height = Inches(5.6)
    
    table_shape = s5.shapes.add_table(rows, cols, left, top, width, height)
    tbl = table_shape.table
    tbl.columns[0].width = Inches(2.2)
    tbl.columns[1].width = Inches(4.2)
    tbl.columns[2].width = Inches(1.6)
    tbl.columns[3].width = Inches(3.733)

    bom_rows = [
        ["Subsystem", "Component Specification", "Cost (₹)", "Technical Justification"],
        ["Laser Scanners ×2", "Hokuyo URG-04LX-class 1D/2D Triangulation Scanner", "21,400", "Sub-mm ranging at 0.5 m; 40 Hz sampling"],
        ["IMU (9-Axis)", "Bosch BMI270 (6-axis) + BMM150 (3-axis Magnetometer)", "1,850", "Ultra-low gyro drift (<0.02°); 200 Hz sampling"],
        ["RTK-GNSS", "u-blox ZED-F9P Multi-Band Receiver + Active Antenna", "32,900", "Sub-decimetre spatial accuracy; CORS compatible"],
        ["Edge Compute", "NVIDIA Jetson Orin Nano (8 GB Unified LPDDR5)", "27,800", "17 TOPS edge AI inference at ~9 W power"],
        ["Camera Modules ×2", "Sony IMX477 CSI 12 MP Global-Shutter Emulation", "9,400", "Sharp sleeper fastener visual inspection"],
        ["Cellular Modem", "Quectel EC25-AF LTE Cat-4 + ESP32 Bridge", "6,200", "Nationwide 4G telemetry with socket reconnect"],
        ["Power Tree", "12V 18Ah LiFePO₄ Battery + DC-DC Step-Down Tree", "8,700", "7.2 hrs continuous field runtime at 24.8 W load"],
        ["Enclosure & Frame", "IP65 Weatherproof ABS Cabinet + Steel Trolley Mount", "11,300", "Vibration-damped crossbar, dust and water sealed"],
        ["Harnessing & Misc.", "Industrial M12 Connectors, SMA Cables, Fasteners", "5,950", "EMI-shielded industrial wiring harness"],
        ["TOTAL COST", "Integrated TR-09 Prototype Rig", "₹1,35,500", "On Budget with ₹500 contingency margin"]
    ]
    for r_idx, r_data in enumerate(bom_rows):
        for c_idx, val in enumerate(r_data):
            cell = tbl.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = "Calibri"
            if r_idx == 0:
                p.font.size = Pt(11)
                p.font.bold = True
                p.font.color.rgb = WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY
            elif r_idx == 10:
                p.font.size = Pt(11)
                p.font.bold = True
                p.font.color.rgb = GREEN_ACCENT if c_idx == 2 else NAVY
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(0xE2, 0xE8, 0xF0)
            else:
                p.font.size = Pt(9.5)
                p.font.color.rgb = DARK_TEXT
                if c_idx == 0:
                    p.font.bold = True

    # =========================================================================
    # SLIDE 6: MATHEMATICAL MODELING & FORMULAS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    create_header(s6, "Mathematical Modeling & Working Principles", "05. Theory & Physics")

    math_cards = [
        ("1. Contactless Gauge Measurement",
         "G(t) = W_frame - [d_left(t) + d_right(t)]",
         "• Rigid crossbeam width: W_frame = 1800.0 mm\n"
         "• Nominal distance to each rail: (1800 - 1676)/2 = 62.0 mm\n"
         "• If rails widen (slack gauge), d_left + d_right decreases\n"
         "• Instantaneous Deviation: ΔG(t) = G(t) - 1676.0 mm"),

        ("2. Cross-Level (Cant / Super-Elevation)",
         "h(t) = G(t) · sin[θ_roll(t)]",
         "• Measures elevation difference h between left & right rails\n"
         "• Measured via roll angle θ_roll from Bosch BMI270 9-axis IMU\n"
         "• Small angle approximation: h ≈ 1676.0 · [θ_roll · (π/180)]\n"
         "• A tilt of 0.222° corresponds to h = +6.5 mm cant error"),

        ("3. Spatial Track Twist Calculation",
         "T(t) = |h(t) - h(t - Δx)| / Δx",
         "• Rate of change of cross-level along track axis\n"
         "• Evaluated over standard chord base: Δx = 3.0 metres\n"
         "• RDSO Maximum Permissible Safe Limit: T(t) ≤ 2.8 mm/m\n"
         "• Excessive twist causes wheel unloading and derailment risk")
    ]
    for idx, (title, formula, details) in enumerate(math_cards):
        cx = Inches(0.8 + idx * 4.0)
        add_card(s6, cx, Inches(1.4), Inches(3.7), Inches(5.6), bg_color=WHITE, border_color=SLATE_BLUE)
        
        box = s6.shapes.add_textbox(cx + Inches(0.2), Inches(1.55), Inches(3.3), Inches(5.2))
        tf = box.text_frame
        
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Calibri"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = NAVY

        p_f = tf.add_paragraph()
        p_f.text = "\n" + formula + "\n"
        p_f.font.name = "Consolas"
        p_f.font.size = Pt(10.5)
        p_f.font.bold = True
        p_f.font.color.rgb = RED_ACCENT

        p_d = tf.add_paragraph()
        p_d.text = details
        p_d.font.name = "Calibri"
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 7: SENSOR FUSION & DATA PIPELINE
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    create_header(s7, "Sensor Fusion & Data Processing Pipeline", "06. Fusion Engine")

    fig2 = os.path.join("assets", "fig2_sensor_fusion.png")
    if os.path.exists(fig2):
        s7.shapes.add_picture(fig2, Inches(0.8), Inches(1.5), width=Inches(6.8))

    add_card(s7, Inches(7.8), Inches(1.5), Inches(4.7), Inches(5.5), bg_color=CARD_BG, border_color=CARD_BORDER)
    f_box = s7.shapes.add_textbox(Inches(8.0), Inches(1.65), Inches(4.3), Inches(5.2))
    tf_f = f_box.text_frame
    
    pf_head = tf_f.paragraphs[0]
    pf_head.text = "Fusion Architecture Details"
    pf_head.font.name = "Calibri"
    pf_head.font.size = Pt(14)
    pf_head.font.bold = True
    pf_head.font.color.rgb = NAVY

    f_points = [
        ("Multi-Rate Synchronization:", "Sensors sample at native rates (IMU 200 Hz, Lasers 40 Hz, GNSS 10 Hz, Cameras 30 fps) into lock-free ring buffers."),
        ("De-Spiking Filter:", "5-point moving median filter eliminates transient optical reflections from polished rail heads."),
        ("Kalman State Fusion:", "Fuses laser and IMU vectors into a stable 5 Hz (200 ms) synchronized track geometry state."),
        ("90s Dead-Reckoning:", "When RTK-GNSS loses line-of-sight in cuttings or under bridges, the IMU dead-reckons position for up to 90 seconds."),
        ("Resilient Telemetry:", "Every sample writes immediately to a 32 GB local buffer before LTE transmission, ensuring zero data loss during signal drops.")
    ]
    for lbl, val in f_points:
        p = tf_f.add_paragraph()
        r1 = p.add_run()
        r1.text = lbl + " "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = NAVY
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 8: COMPUTER VISION DEFECT DETECTION
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    create_header(s8, "Deep Learning Defect Detection Pipeline", "07. Edge Computer Vision")

    fig5 = os.path.join("assets", "fig5_defect_detection_workflow.png")
    if os.path.exists(fig5):
        s8.shapes.add_picture(fig5, Inches(0.8), Inches(1.5), width=Inches(6.6))

    add_card(s8, Inches(7.6), Inches(1.5), Inches(4.9), Inches(5.5), bg_color=WHITE, border_color=SLATE_BLUE)
    cv_box = s8.shapes.add_textbox(Inches(7.8), Inches(1.65), Inches(4.5), Inches(5.2))
    tf_cv = cv_box.text_frame
    
    pcv_head = tf_cv.paragraphs[0]
    pcv_head.text = "4 Target Rail Defect Classes"
    pcv_head.font.name = "Calibri"
    pcv_head.font.size = Pt(14)
    pcv_head.font.bold = True
    pcv_head.font.color.rgb = NAVY

    classes = [
        ("1. Missing Fastener (ERC):", "Detects missing or dislodged elastic rail clips from sleeper seats. Gauge widening hazard."),
        ("2. Cracked Fishplate:", "Fatigue crack propagating through joint bar bolt holes. Joint collapse hazard."),
        ("3. Ballast Deficiency:", "Erosion void cavity exposing sleeper base near culverts. Track settlement hazard."),
        ("4. Surface Squat:", "Rolling Contact Fatigue (RCF) indentation micro-fissure on rail head running surface.")
    ]
    for c_title, c_desc in classes:
        p = tf_cv.add_paragraph()
        r1 = p.add_run()
        r1.text = c_title + " "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = RED_ACCENT
        r2 = p.add_run()
        r2.text = c_desc
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = DARK_TEXT

    p_gate = tf_cv.add_paragraph()
    p_gate.text = "\n91% Confidence Gating Architecture:"
    p_gate.font.name = "Calibri"
    p_gate.font.size = Pt(11)
    p_gate.font.bold = True
    p_gate.font.color.rgb = NAVY

    p_gate_desc = tf_cv.add_paragraph()
    p_gate_desc.text = "Only defects detected with ≥91% confidence emit critical alerts. Borderline frames (<91%) are logged for offline review, preventing false-alarm fatigue."
    p_gate_desc.font.name = "Calibri"
    p_gate_desc.font.size = Pt(9.5)
    p_gate_desc.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 9: NATIVE DESKTOP INSPECTION SOFTWARE
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    create_header(s9, "Native Desktop Inspection Software (Tkinter + Matplotlib)", "08. Software Engineering")

    sw_cards = [
        ("100% Native Python GUI", "Zero Web Lag / No Browser Needed", "Runs directly on desktop via `python main.py`. Built using standard library Tkinter and Matplotlib without external web server dependencies."),
        ("Digital Telemetry Gauges", "Instant Visual Safety Badges", "Displays real-time Broad Gauge, Cross-Level, and Twist with dynamic color badges: Green for NORMAL, Orange for WARNING, Red for CRITICAL."),
        ("Live Dynamic Charting", "RDSO Safety Limit Boundaries", "Embedded Matplotlib canvas plots measured gauge in real time against upper (+6 mm) and lower (-3 mm) RDSO tolerance envelopes."),
        ("Real-Time Defect Viewer", "Bounding Boxes & Confidence", "Displays camera inspection images with red bounding boxes and confidence percentage whenever a defect crosses the 91% threshold.")
    ]
    for i, (title, highlight, desc) in enumerate(sw_cards):
        row = i // 2
        col = i % 2
        bx = Inches(0.8 + col * 6.0)
        by = Inches(1.5 + row * 2.8)
        add_card(s9, bx, by, Inches(5.7), Inches(2.5), bg_color=CARD_BG, border_color=CARD_BORDER)
        
        box = s9.shapes.add_textbox(bx + Inches(0.2), by + Inches(0.15), Inches(5.3), Inches(2.2))
        tf = box.text_frame
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Calibri"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = NAVY

        p2 = tf.add_paragraph()
        p2.text = highlight
        p2.font.name = "Calibri"
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = SLATE_BLUE

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.name = "Calibri"
        p3.font.size = Pt(10)
        p3.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 10: EXPERIMENTAL VALIDATION & RESULTS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    create_header(s10, "Experimental Validation & Measured Results", "09. Empirical Testing")

    fig3 = os.path.join("assets", "fig3_project_timeline.png")
    if os.path.exists(fig3):
        s10.shapes.add_picture(fig3, Inches(0.8), Inches(1.4), width=Inches(11.733))

    res_card = add_card(s10, Inches(0.8), Inches(4.3), Inches(11.733), Inches(2.7), bg_color=WHITE, border_color=GREEN_ACCENT)
    r_box = s10.shapes.add_textbox(Inches(1.1), Inches(4.45), Inches(11.1), Inches(2.4))
    tf_r = r_box.text_frame
    
    pr_head = tf_r.paragraphs[0]
    pr_head.text = "Key Empirical Test Results (1.5 km Siding Validation):"
    pr_head.font.name = "Calibri"
    pr_head.font.size = Pt(13)
    pr_head.font.bold = True
    pr_head.font.color.rgb = GREEN_ACCENT

    results = [
        "Gauge Accuracy: Achieved ±0.62 mm average gauge error against reference manual vernier trolley (Benchmark target: ±0.8 mm).",
        "Cross-Level Accuracy: Achieved ±0.88 mm average cross-level error across 1.5 km siding (Benchmark target: ±1.2 mm).",
        "High Repeatability: Measured standard deviation σ = 0.38 mm gauge over 5 consecutive passes along the identical track siding.",
        "Blinded Defect Trial: Correctly identified 8 out of 8 blinded injected defects (6 loose clips, 2 cracked plates) with 100% detection rate.",
        "Thermal Stability: Continuous 6-hour summer endurance run at 41.5 °C; internal cabinet stabilized at 58.4 °C (well below 71 °C limit)."
    ]
    for res in results:
        p = tf_r.add_paragraph()
        p.text = "✔ " + res
        p.font.name = "Calibri"
        p.font.size = Pt(10)
        p.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 11: ECONOMIC FEASIBILITY & COST COMPARISON
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    create_header(s11, "Economic Feasibility & Cost-Benefit Analysis", "10. Cost Comparison")

    fig6 = os.path.join("assets", "fig6_cost_comparison.png")
    if os.path.exists(fig6):
        s11.shapes.add_picture(fig6, Inches(0.8), Inches(1.5), width=Inches(6.8))

    add_card(s11, Inches(7.8), Inches(1.5), Inches(4.7), Inches(5.5), bg_color=CARD_BG, border_color=CARD_BORDER)
    c_box = s11.shapes.add_textbox(Inches(8.0), Inches(1.65), Inches(4.3), Inches(5.2))
    tf_c = c_box.text_frame
    
    pc_head = tf_c.paragraphs[0]
    pc_head.text = "Why the Economics Matter"
    pc_head.font.name = "Calibri"
    pc_head.font.size = Pt(14)
    pc_head.font.bold = True
    pc_head.font.color.rgb = NAVY

    c_points = [
        ("Imported TRC (Plasser EM-120):", "Cost: ≈ ₹38 Crore per unit. High foreign spare dependency. Disregards 35% of network (branch lines)."),
        ("Imported ITMS Coach:", "Cost: ₹60 to 110 Crore. Severe vendor lock-in and expensive annual software licensing."),
        ("TR-09 ITMS Rig:", "Cost: ₹1.35 Lakh (₹1,35,500). Delivers sub-millimetre digital inspection on standard push trolleys."),
        ("Massive 2,800× Cost Advantage:", "An entire railway division can deploy multiple TR-09 trolleys for less than the cost of one imported replacement sensor head."),
        ("Frequent Digital Audits:", "Replaces bi-annual imported surveys with bi-weekly objective, geo-tagged inspection on rural branch lines.")
    ]
    for lbl, val in c_points:
        p = tf_c.add_paragraph()
        r1 = p.add_run()
        r1.text = lbl + " "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = NAVY
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 12: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    create_header(s12, "Conclusion & Technical Future Scope", "11. Summary & Outlook")

    # Left: Conclusion
    add_card(s12, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.5), bg_color=WHITE, border_color=SLATE_BLUE)
    c_box = s12.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tf_con = c_box.text_frame
    
    p1 = tf_con.paragraphs[0]
    p1.text = "Project Conclusions"
    p1.font.name = "Calibri"
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = NAVY

    con_bullets = [
        "Validated Technical Feasibility: Proved that sub-millimetre contactless track monitoring and AI defect detection are achievable on a low-cost edge platform.",
        "Budget Discipline: Delivered the entire functional prototype within ₹1,35,500, sourcing 100% of components from Indian distributors.",
        "Branch Line Impact: Provides a practical, deployable solution to eliminate the 35% safety blind spot on Indian Railways branch corridors.",
        "Open Reference Design: Code, hardware schematics, and 12,000 labelled frames released openly on GitHub for future research."
    ]
    for b in con_bullets:
        p = tf_con.add_paragraph()
        p.text = "• " + b
        p.font.name = "Calibri"
        p.font.size = Pt(10.5)
        p.font.color.rgb = DARK_TEXT

    # Right: Future Scope
    add_card(s12, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.5), bg_color=CARD_BG, border_color=CARD_BORDER)
    f_box = s12.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.3), Inches(5.2))
    tf_fut = f_box.text_frame
    
    p2 = tf_fut.paragraphs[0]
    p2.text = "Future Technical Roadmap"
    p2.font.name = "Calibri"
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = NAVY

    fut_bullets = [
        "Ultrasonic Internal Flaw Testing: Integrating electromagnetic acoustic transducers (EMAT) to detect internal sub-surface fatigue cracks in rail webs.",
        "Motorized Autonomous Patrol: Adding a low-power brushless DC hub motor with LiDAR collision avoidance for autonomous section patrolling between train blocks.",
        "Direct Indian Railways TMS Sync: Developing API microservices complying with the Indian Railway Track Management System (IRPSM) schema for direct work-order creation.",
        "Catenary OHE Integration: Adding upward-facing line-scan cameras for automated pantograph and overhead contact wire wear monitoring."
    ]
    for b in fut_bullets:
        p = tf_fut.add_paragraph()
        p.text = "• " + b
        p.font.name = "Calibri"
        p.font.size = Pt(10.5)
        p.font.color.rgb = DARK_TEXT

    # =========================================================================
    # SLIDE 13: THANK YOU & Q&A
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    bg13 = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg13.fill.solid()
    bg13.fill.fore_color.rgb = NAVY
    bg13.line.color.rgb = NAVY

    tq_card = add_card(s13, Inches(2.0), Inches(1.5), Inches(9.333), Inches(4.5), bg_color=RGBColor(0x23, 0x44, 0x76), border_color=RGBColor(0x31, 0x82, 0xCE))
    tq_box = s13.shapes.add_textbox(Inches(2.3), Inches(1.8), Inches(8.7), Inches(4.0))
    tf_tq = tq_box.text_frame
    
    p_tq = tf_tq.paragraphs[0]
    p_tq.text = "Thank You!"
    p_tq.font.name = "Calibri"
    p_tq.font.size = Pt(36)
    p_tq.font.bold = True
    p_tq.font.color.rgb = WHITE
    p_tq.alignment = PP_ALIGN.CENTER

    p_qa = tf_tq.add_paragraph()
    p_qa.text = "Questions & Faculty Evaluation"
    p_qa.font.name = "Calibri"
    p_qa.font.size = Pt(18)
    p_qa.font.bold = True
    p_qa.font.color.rgb = RGBColor(0x63, 0xB3, 0xED)
    p_qa.alignment = PP_ALIGN.CENTER

    p_dtl = tf_tq.add_paragraph()
    p_dtl.text = (
        "\nTR-09: Indigenous Contactless Integrated Track Monitoring System (ITMS)\n"
        "Project Team: Soham Bhosale  •  Arnav  •  Rudra Marathe\n"
        "Faculty Mentor: Prof. Chaitali Patil\n"
        "Department of Computer Engineering, MPSTME, SVKM's NMIMS\n\n"
        "GitHub: https://github.com/soham3096/TR-09-Contactless-Track-Monitoring-System\n"
        "Execution: python main.py (Native Desktop GUI)"
    )
    p_dtl.font.name = "Calibri"
    p_dtl.font.size = Pt(12)
    p_dtl.font.color.rgb = RGBColor(0xEB, 0xF8, 0xFF)
    p_dtl.alignment = PP_ALIGN.CENTER

    prs.save(output_filename)
    print(f"[SUCCESS] PowerPoint presentation generated: {output_filename}")

if __name__ == "__main__":
    build_presentation()
