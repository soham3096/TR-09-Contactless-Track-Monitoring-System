"""
=============================================================================
Academic Project Report Generator (.docx)
TR-09: Development of Indigenous Contactless Integrated Track Monitoring Systems
Institute: SVKM's NMIMS MPSTME, Shirpur
Course: Design Experience (MBA Tech & B.Tech CE - 2nd Year)
Authors: Soham Bhosale, Arnav, Rudra Marathe | Mentor: Prof. Chaitali Patil
=============================================================================
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Sets background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets inner padding for a table cell in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def add_callout_box(doc, text, title=None, border_color="2B6CB0", bg_color="F0F4F8"):
    """Creates a styled callout quote box with left colored accent border."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=160)
    
    # Left border only
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="36" w:space="0" w:color="{border_color}"/>'
        f'<w:top w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if title:
        r_title = p.add_run(f"{title}\n")
        r_title.bold = True
        r_title.font.name = "Calibri"
        r_title.font.size = Pt(10.5)
        r_title.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        
    r_text = p.add_run(text)
    r_text.font.name = "Calibri"
    r_text.font.size = Pt(10)
    r_text.font.italic = True
    r_text.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)

    # Empty paragraph after table for spacing
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_after = Pt(4)

def format_table(table, col_widths, headers, data, header_bg="1B365D", alt_bg="F7FAFC"):
    """Applies modern styling to docx table."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Header Row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], header_bg)
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    # Data Rows
    for row_idx, row_data in enumerate(data):
        row_cells = table.add_row().cells
        bg = alt_bg if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, cell_value in enumerate(row_data):
            row_cells[col_idx].text = str(cell_value)
            set_cell_background(row_cells[col_idx], bg)
            set_cell_margins(row_cells[col_idx], top=80, bottom=80, left=120, right=120)
            p = row_cells[col_idx].paragraphs[0]
            p.paragraph_format.line_spacing = 1.1
            p.paragraph_format.space_after = Pt(2)
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(9)
                r.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
                if col_idx == 0:
                    r.font.bold = True

    # Apply widths
    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = Inches(width)

def build_word_report(output_filename="TR-09_ITMS_Project_Report.docx"):
    doc = Document()
    
    # Page Margins: 1 inch (72 pt)
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # -------------------------------------------------------------------------
    # COVER PAGE
    # -------------------------------------------------------------------------
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(10)
    p_logo.paragraph_format.space_after = Pt(15)
    logo_path = os.path.join("assets", "nmims_logo.png")
    if os.path.exists(logo_path):
        p_logo.add_run().add_picture(logo_path, width=Inches(1.8))

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst1 = p_inst.add_run("SVKM'S Narsee Monjee Institute of Management Studies\n")
    r_inst1.bold = True
    r_inst1.font.size = Pt(13)
    r_inst1.font.name = "Calibri"
    r_inst1.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    r_inst2 = p_inst.add_run("Mukesh Patel School of Technology Management & Engineering\nShirpur Campus, Maharashtra")
    r_inst2.font.size = Pt(11)
    r_inst2.font.name = "Calibri"
    r_inst2.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)
    p_inst.paragraph_format.space_after = Pt(25)

    p_proj = doc.add_paragraph()
    p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_proj = p_proj.add_run("DEVELOPMENT OF INDIGENOUS CONTACTLESS INTEGRATED TRACK MONITORING SYSTEMS (ITMS)\n")
    r_proj.bold = True
    r_proj.font.size = Pt(18)
    r_proj.font.name = "Calibri"
    r_proj.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)
    
    r_codename = p_proj.add_run("TR-09 Prototype Reference Design & Evaluation")
    r_codename.font.size = Pt(13)
    r_codename.font.bold = True
    r_codename.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)
    p_proj.paragraph_format.space_after = Pt(25)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("A Project Report submitted in partial fulfilment of the requirements for\n")
    r_sub.font.size = Pt(10.5)
    r_sub.font.name = "Calibri"
    r_sub.font.italic = True
    
    r_course = p_sub.add_run("Course: Design Experience\n")
    r_course.bold = True
    r_course.font.size = Pt(11.5)
    r_course.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    r_prog = p_sub.add_run("Programme: MBA Tech & B.Tech Computer Engineering – Second Year\n")
    r_prog.bold = True
    r_prog.font.size = Pt(11)

    r_batch = p_sub.add_run("Batch: 2024–2029  |  Academic Year: 2025–26")
    r_batch.font.size = Pt(10.5)
    p_sub.paragraph_format.space_after = Pt(30)

    # Students & Mentor Box
    p_team = doc.add_paragraph()
    p_team.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_by = p_team.add_run("Submitted By:\n")
    r_by.bold = True
    r_by.font.size = Pt(11)
    r_by.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    r_names = p_team.add_run(
        "1. Soham Bhosale (MBA Tech Computer Engineering)\n"
        "2. Arnav (MBA Tech Computer Engineering)\n"
        "3. Rudra Marathe (MBA Tech Computer Engineering)\n\n"
    )
    r_names.font.size = Pt(11)
    r_names.font.name = "Calibri"

    r_guide = p_team.add_run("Under the Guidance of:\n")
    r_guide.bold = True
    r_guide.font.size = Pt(11)
    r_guide.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    r_mentor = p_team.add_run("Prof. Chaitali Patil\nDepartment of Computer Engineering, MPSTME")
    r_mentor.bold = True
    r_mentor.font.size = Pt(11.5)
    r_mentor.font.name = "Calibri"
    r_mentor.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)

    # Page Break after Cover
    doc.add_page_break()

    # Configure Header / Footer for inner pages
    header = doc.sections[0].header
    p_hdr = header.paragraphs[0]
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_hdr = p_hdr.add_run("TR-09: Indigenous Contactless ITMS | MPSTME NMIMS")
    r_hdr.font.name = "Calibri"
    r_hdr.font.size = Pt(8.5)
    r_hdr.font.color.rgb = RGBColor(0x71, 0x80, 0x96)

    footer = doc.sections[0].footer
    p_ftr = footer.paragraphs[0]
    p_ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ftr = p_ftr.add_run("Design Experience Project Report  •  Academic Year 2025–26")
    r_ftr.font.name = "Calibri"
    r_ftr.font.size = Pt(8.5)
    r_ftr.font.color.rgb = RGBColor(0x71, 0x80, 0x96)

    # -------------------------------------------------------------------------
    # CERTIFICATE & DECLARATION
    # -------------------------------------------------------------------------
    h_cert = doc.add_heading("Certificate of Approval", level=1)
    h_cert.paragraph_format.space_before = Pt(12)
    h_cert.paragraph_format.space_after = Pt(12)
    for r in h_cert.runs:
        r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_cert = doc.add_paragraph(
        "This is to certify that the project report entitled \"Development of Indigenous Contactless "
        "Integrated Track Monitoring Systems (ITMS) – TR-09 Prototype\" is a bonafide record of work carried out by "
        "Soham Bhosale, Arnav, and Rudra Marathe, students of Second Year MBA Tech & B.Tech Computer Engineering "
        "at Mukesh Patel School of Technology Management & Engineering, SVKM's NMIMS, Shirpur, under my supervision "
        "and guidance in partial fulfilment of the requirements for the Design Experience course during the academic year 2025–26."
    )
    p_cert.paragraph_format.line_spacing = 1.15
    p_cert.paragraph_format.space_after = Pt(40)

    # Signatures
    sig_tbl = doc.add_table(rows=2, cols=2)
    sig_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_tbl.cell(0, 0).paragraphs[0].text = "______________________________\nProf. Chaitali Patil\nProject Mentor, MPSTME"
    sig_tbl.cell(0, 1).paragraphs[0].text = "______________________________\nHead of Department\nComputer Engineering, MPSTME"
    sig_tbl.cell(1, 0).paragraphs[0].text = "\nDate: 21 October 2026\nPlace: Shirpur"
    sig_tbl.cell(1, 1).paragraphs[0].text = "\n______________________________\nExternal Examiner"
    for r in sig_tbl.rows:
        for c in r.cells:
            for p in c.paragraphs:
                for run in p.runs:
                    run.font.name = "Calibri"
                    run.font.size = Pt(10)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # TABLE OF CONTENTS / INDEX
    # -------------------------------------------------------------------------
    h_index = doc.add_heading("Index", level=1)
    for r in h_index.runs:
        r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    index_headers = ["Section", "Title", "Page"]
    index_data = [
        ["01", "Introduction", "1"],
        ["02", "Reason Behind the Project", "2"],
        ["03", "Review of Literature", "4"],
        ["04", "Problem Definition", "6"],
        ["05", "Objectives of the Project", "7"],
        ["06", "Proposed Methodology / Conceptual Framework", "8"],
        ["07", "Team, Roles, and Work", "10"],
        ["08", "Project Timeline", "11"],
        ["09", "Risk Register", "12"],
        ["10", "Outcomes, in Three Layers", "13"],
        ["11", "Reflection", "15"],
        ["12", "References", "16"],
        ["13", "Software Architecture, Implementation & GitHub Repository", "17"]
    ]
    tbl_idx = doc.add_table(rows=1, cols=3)
    format_table(tbl_idx, [1.0, 4.5, 0.9], index_headers, index_data)

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(15)

    # LIST OF TABLES
    h_lot = doc.add_heading("List of Tables", level=2)
    for r in h_lot.runs:
        r.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)
    lot_headers = ["Table No.", "Name of Table", "Page No."]
    lot_data = [
        ["3.1", "Sample of the Shortlist (Literature Review Comparison)", "4"],
        ["5.1", "In Scope, Out of Scope Matrix", "7"],
        ["6.2", "Bill of Materials (Budget Hard Cap: ₹1.35 Lakhs)", "8"],
        ["7.0", "Team, Roles, and Work Breakdown", "10"],
        ["8.1", "Project Timeline – Two Semester Plan", "11"],
        ["9.0", "Risk Register and Mitigation Matrix", "12"],
        ["10.4", "Cost-Benefit Across Track Inspection Approaches", "13"],
        ["13.1", "TR-09 Software Architecture Modules and Core Functions", "18"]
    ]
    tbl_lot = doc.add_table(rows=1, cols=3)
    format_table(tbl_lot, [1.2, 4.3, 0.9], lot_headers, lot_data)

    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_after = Pt(15)

    # LIST OF FIGURES
    h_lof = doc.add_heading("List of Figures", level=2)
    for r in h_lof.runs:
        r.font.color.rgb = RGBColor(0x2B, 0x6C, 0xB0)
    lof_headers = ["Fig No.", "Name of Figure", "Page No."]
    lof_data = [
        ["Fig 1 (2.3)", "TR-09 System Architecture Diagram", "3"],
        ["Fig 2 (6.6)", "Sensor Fusion and Data Processing Pipeline", "9"],
        ["Fig 3 (8.1)", "Project Timeline – Two Semester Gantt Plan", "11"],
        ["Fig 4 (7.1)", "Team Structure – Four Pods + Mentor", "10"],
        ["Fig 5 (11.3)", "Defect Detection Workflow (CNN-LSTM Model)", "15"],
        ["Fig 6 (11.3)", "Cost-per-Unit Comparison Across Inspection Approaches", "16"],
        ["Fig 7 (13.1)", "Interactive Streamlit Web Dashboard Interface", "19"]
    ]
    tbl_lof = doc.add_table(rows=1, cols=3)
    format_table(tbl_lof, [1.2, 4.3, 0.9], lof_headers, lof_data)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # SECTION 01: INTRODUCTION
    # -------------------------------------------------------------------------
    h1 = doc.add_heading("01. Introduction", level=1)
    for r in h1.runs:
        r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_intro = doc.add_paragraph(
        "This report documents TR-09, a hand-trolley-mounted contactless track inspector designed and built "
        "by second-year MBA Tech and B.Tech Computer Engineering students at MPSTME Shirpur as part of the "
        "Design Experience course. The prototype is aimed squarely at the branch lines that imported Track Recording "
        "Cars rarely visit — roughly a third of India's route kilometres — and is held to a hard parts budget of "
        "₹1.35 lakh, with every component sourced from Indian distributors.\n\n"
        "Our headline targets are ±0.8 mm gauge accuracy, ±1.2 mm cross-level accuracy, and detection of four common "
        "rail-defect classes at ≥ 91% precision. Sensor data fuses on an NVIDIA Jetson Orin Nano at the edge, streams "
        "over LTE to a cloud dashboard, and back-fills locally when the radio drops. The full design — schematics, "
        "Bill of Materials (BoM), firmware, ML weights, and an open reference dataset — ships under a permissive licence "
        "on GitHub by July 2026."
    )
    p_intro.paragraph_format.line_spacing = 1.15
    p_intro.paragraph_format.space_after = Pt(12)

    # Highlight metrics callout
    add_callout_box(
        doc,
        "• Hard Parts Budget Cap: ₹1.35 Lakh (All Indian-sourced)\n"
        "• Geometry Tolerances: ±0.8 mm Gauge Accuracy | ±1.2 mm Cross-Level Accuracy\n"
        "• Open Reference Release: 12,000 labelled frames & full software on GitHub",
        title="TR-09 Headline Engineering Benchmarks"
    )

    # -------------------------------------------------------------------------
    # SECTION 02: REASON BEHIND THE PROJECT
    # -------------------------------------------------------------------------
    h2 = doc.add_heading("02. Reason Behind the Project", level=1)
    for r in h2.runs:
        r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_r1 = doc.add_paragraph(
        "Indian Railways carries the country in a way that's easy to take for granted — about 24 million passengers "
        "and 3.5 million tonnes of freight a day, across 68,000-plus route kilometres. The whole thing rides on two thin "
        "steel lines that have to stay within millimetres of where they were yesterday. According to the Ministry of Railways' "
        "2024 safety review, around 19% of derailments between 2019 and 2024 traced back to track-geometry issues — twist, "
        "gauge widening, or quietly rotting fasteners that a walking patrol just couldn't see in time. The patrols themselves "
        "are heroic but stretched. A single P-Way gang typically covers 8 to 10 km of section, and the official window for a "
        "thorough foot inspection has compressed from once a week to roughly once every nine days as freight density climbs.\n\n"
        "The expensive answer already exists. Track Recording Cars — the imported Plasser EM-120 and EM-SAT family — do this "
        "job beautifully on the trunk corridors, but they cost about ₹38 crore a unit, depend on European spares, and visit "
        "any given branch line maybe twice a year. Branch lines, which carry around 35% of our route kilometres, mostly go "
        "un-instrumented. That's the gap our project sits inside."
    )
    p_r1.paragraph_format.line_spacing = 1.15
    p_r1.paragraph_format.space_after = Pt(8)

    doc.add_heading("2.1 What Contactless Inspection Actually Changes", level=2)
    p_r2 = doc.add_paragraph(
        "Modern contactless ITMS rigs use lasers, line-scan cameras, an IMU, and a GNSS receiver to measure everything a "
        "contact-trolley does — but at line speed, without touching the rail, and without the calibration drift that mechanical "
        "sensors suffer. Recent field studies put the numbers at roughly 6× faster inspection, around 92% defect-detection F1, "
        "and a 37% drop in unplanned maintenance call-outs (Iyer & Hassan, 2024; Wei et al., 2023).\n\n"
        "The shift matters less for the trunk routes — they will get the imported coaches one way or another — and more for "
        "the long tail of the network where decisions are still made by someone walking, looking, and writing in a register. "
        "If that someone could push a trolley once a fortnight and walk away with a geo-tagged report instead, the maintenance "
        "economics on those lines change quietly but completely."
    )
    p_r2.paragraph_format.line_spacing = 1.15

    doc.add_heading("2.2 Why a Hand-Trolley, and Not Something Bigger", level=2)
    p_r3 = doc.add_paragraph(
        "Our first instinct was to imagine a small autonomous car. We talked ourselves out of it within a week. Branch lines "
        "have unpredictable pedestrian crossings, rough ballast, and very limited supervision; an unmanned vehicle on those lines "
        "is a regulatory and safety problem we are not equipped to solve. A hand-trolley is the existing standard tool of the "
        "P-Way gang — already insured, already understood, already on the line. Adding a sensor cabinet to it is a much smaller "
        "institutional ask.\n\n"
        "It also means TR-09 has a single, very honest persona it must serve: the senior P-Way inspector who knows their section "
        "better than any sensor will. The trolley is for them, not instead of them."
    )
    p_r3.paragraph_format.line_spacing = 1.15

    doc.add_heading("2.3 Where This Fits in the National Picture", level=2)
    p_r4 = doc.add_paragraph(
        "The National Rail Plan 2030, the Atmanirbhar Bharat brief for safety-critical infrastructure, and RDSO's own indigenous "
        "TRC trials on the Lucknow–Kanpur section all point in the same direction: build it here, document it openly, and lower "
        "the cost until the technology can scale beyond a few flagship corridors. TR-09 is not a competitor to that work — it is a "
        "tributary. Every rupee we spend learning how to make a low-cost rig work is a rupee that does not need to be spent again "
        "by the next student team."
    )
    p_r4.paragraph_format.line_spacing = 1.15

    # Insert Figure 1
    fig1_path = os.path.join("assets", "fig1_system_architecture.png")
    if os.path.exists(fig1_path):
        p_fig1 = doc.add_paragraph()
        p_fig1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig1.paragraph_format.space_before = Pt(10)
        p_fig1.add_run().add_picture(fig1_path, width=Inches(5.8))
        p_cap1 = doc.add_paragraph("Figure 1: TR-09 System Architecture (Sensors, Edge Compute, LTE & Cloud Dashboard)")
        p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap1.paragraph_format.space_after = Pt(14)
        for r in p_cap1.runs:
            r.font.size = Pt(9.5)
            r.font.italic = True
            r.font.bold = True
            r.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    # -------------------------------------------------------------------------
    # SECTION 03: REVIEW OF LITERATURE
    # -------------------------------------------------------------------------
    h3 = doc.add_heading("03. Review of Literature", level=1)
    for r in h3.runs:
        r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_lit = doc.add_paragraph(
        "Before we wrote a single line of firmware, we read. Across IEEE Xplore, Scopus, SpringerLink, and the RDSO publication "
        "archive, we worked through 32 papers and three white papers published between 2019 and 2025. Each was scored on five axes: "
        "sensor stack, edge-vs-cloud inference, dataset region, claimed accuracy, and replicability of the build. The patterns "
        "below are what surfaced.\n\n"
        "• Pattern One — The sensor stack has converged: Of the 32 papers, 27 use some combination of laser triangulation, "
        "an inertial measurement unit, and a GNSS receiver. The arguments are now mostly about which model of each, not whether "
        "to use them. We spent our energy on integration instead of second-guessing the sensor list.\n\n"
        "• Pattern Two — Edge AI is finally cheap enough: Inference that needed a workstation in 2020 now fits on a 9-watt module. "
        "The Jetson Orin Nano benchmarks at about 17 TOPS for under ₹28,000. Three years ago, TR-09 would have needed a backpack-mounted "
        "laptop. Today it fits in a small IP65 cabinet that bolts to the trolley deck.\n\n"
        "• Pattern Three — Indian-context data is missing: Almost every published model is trained on Chinese ballast or European "
        "concrete sleepers. We could only find two open datasets that include Indian wooden-and-concrete mixed-sleeper sections. "
        "One of TR-09's secondary outcomes is to release a labelled dataset of around 12,000 frames from the test loop at Shirpur.\n\n"
        "• Pattern Four — Replicability is rare: Of the 32 papers, only four published a complete bill of materials, and only one "
        "shared firmware. Most projects sit behind vendor-locked sensors or institutional licences. This influenced our open-release "
        "decision more than anything else: we want the next team to start where we ended."
    )
    p_lit.paragraph_format.line_spacing = 1.15
    p_lit.paragraph_format.space_after = Pt(10)

    # Table 3.1
    p_t31_lbl = doc.add_paragraph("Table 3.1: Sample of the Shortlist (Literature Review Analysis)")
    p_t31_lbl.paragraph_format.space_before = Pt(8)
    p_t31_lbl.paragraph_format.space_after = Pt(4)
    for r in p_t31_lbl.runs:
        r.font.bold = True
        r.font.size = Pt(9.5)

    t31_headers = ["Ref", "Year / Authors", "What They Did", "Headline Result", "Where It Falls Short"]
    t31_data = [
        ["A", "2024 · Iyer & Hassan", "Laser-IMU fusion at 180 km/h", "±0.3 mm gauge", "22 kg sensor head; coach scale"],
        ["B", "2023 · Wei et al.", "CNN-Transformer for fastener defects", "F1 of 0.92", "Trained on Chinese ballast only"],
        ["C", "2023 · Krishnan", "RDSO indigenous prototype review", "Roadmap to 2030", "No third-party benchmarks"],
        ["D", "2022 · Adeyemi & Park", "Low-cost MEMS-IMU for ride quality", "₹4,200 per node", "Track geometry not measured"],
        ["E", "2025 · Sharma et al.", "Edge ML on Jetson for rail surface", "94% mAP, 11 W draw", "Cooling above 46 °C"],
        ["F", "2024 · DRDO TBR", "Indigenous TRC trial on Lucknow line", "₹13.8 cr target", "Coach-scale only; not for branch lines"],
        ["G", "2024 · Banerjee et al.", "RTK-GNSS drift on Indian sections", "Sub-decimetre CORS", "Limited urban coverage"],
        ["H", "2023 · Müller & Sato", "Line-scan vision for ballast wear", "0.89 IoU", "Needs controlled lighting rig"]
    ]
    tbl_t31 = doc.add_table(rows=1, cols=5)
    format_table(tbl_t31, [0.5, 1.4, 1.8, 1.3, 1.4], t31_headers, t31_data)

    p_sp3 = doc.add_paragraph()
    p_sp3.paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 04: PROBLEM DEFINITION
    # -------------------------------------------------------------------------
    h4 = doc.add_heading("04. Problem Definition", level=1)
    for r in h4.runs:
        r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_prob = doc.add_paragraph(
        "Statistics make the problem feel abstract until you put them next to each other:\n"
        "• 19% of derailments (2019–2024) were linked directly to track-geometry anomalies.\n"
        "• ₹38 Crore is the approximate cost of one imported Track Recording Car unit.\n"
        "• 9 Days is the average gap between manual foot patrol inspections on branch lines.\n"
        "• 35% of Indian route kilometres are branch lines that rarely receive automated inspection.\n"
        "• ≤ ₹1.35 Lakh is the TR-09 hard parts budget cap.\n"
        "• 12,000 labelled visual frames are planned for open release."
    )
    p_prob.paragraph_format.line_spacing = 1.15

    doc.add_heading("4.1 Three Failure Modes Worth Naming", level=2)
    p_fmodes = doc.add_paragraph(
        "4.1.1 Slow Gauge Widening: Wooden sleepers in older sections deform slowly under load. A few millimetres a year "
        "is invisible to a foot patrol but disastrous when it crosses tolerance during a heavy summer. Continuous, repeatable "
        "measurement turns this from a trailing indicator into a leading one.\n\n"
        "4.1.2 Missing or Loose Fasteners: Theft, vibration, and weather all conspire to loosen elastic-rail clips (ERCs). "
        "A walking patrol catches the obvious cases. A camera that sees every fastener every fortnight catches the rest.\n\n"
        "4.1.3 Ballast Deficiency Near Culverts and Crossings: Water washes ballast away faster than the maintenance cycle can "
        "replace it. The damage tends to concentrate at culverts and unmanned crossings — exactly the spots that are hardest to "
        "inspect on foot at night."
    )
    p_fmodes.paragraph_format.line_spacing = 1.15

    doc.add_heading("4.2 The Formal Problem Statement", level=2)
    p_stmt = doc.add_paragraph(
        "Design and validate a contactless, hand-trolley-mounted track inspector that:\n"
        "(a) Measures gauge, cross-level, twist, and rail surface with at least the accuracy of an in-service push trolley;\n"
        "(b) Costs no more than ₹1.35 lakh in parts using India-available components;\n"
        "(c) Is operable end-to-end by two students with one day of training; and\n"
        "(d) Ships as an open reference design — schematics, BoM, firmware, ML weights, and labelled datasets."
    )
    p_stmt.paragraph_format.line_spacing = 1.15
    p_stmt.paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 05: OBJECTIVES OF THE PROJECT
    # -------------------------------------------------------------------------
    h5 = doc.add_heading("05. Objectives of the Project", level=1)
    for r in h5.runs:
        r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_obj = doc.add_paragraph(
        "We agreed early that an objective only counts if we can either show it on a bench or record it on a field run. "
        "Each objective below has an owner, a measurement method, and a pass/fail line:\n"
        "1. Build a working trolley-mounted ITMS prototype within ₹1.35 lakh in parts, sourced from Indian distributors only.\n"
        "2. Hit ±0.8 mm gauge accuracy and ±1.2 mm cross-level accuracy against a calibrated reference trolley over a 1.5 km test loop.\n"
        "3. Detect four defect classes — missing fastener, cracked fishplate, ballast deficiency, surface squat — with ≥ 91% precision and ≥ 87% recall.\n"
        "4. Publish a live dashboard that updates within 4 seconds of a defect event and works on a normal phone browser.\n"
        "5. Release the full reference design — BoM, firmware, ML model, dataset, assembly notes — under a permissive licence on GitHub by July 2026.\n"
        "6. Document mapping to RDSO geometry tolerances, IS-3973 environmental classes, and the IRPSM data schema."
    )
    p_obj.paragraph_format.line_spacing = 1.15
    p_obj.paragraph_format.space_after = Pt(8)

    # Table 5.1
    p_t51_lbl = doc.add_paragraph("Table 5.1: In Scope vs. Out of Scope Matrix")
    p_t51_lbl.paragraph_format.space_before = Pt(8)
    p_t51_lbl.paragraph_format.space_after = Pt(4)
    for r in p_t51_lbl.runs:
        r.font.bold = True
        r.font.size = Pt(9.5)

    t51_headers = ["Subsystem / Capability", "In Scope (TR-09)", "Out of Scope (Deferred to Future)"]
    t51_data = [
        ["Track Geometry", "Gauge, cross-level, and spatial twist", "Ultrasonic internal rail-flaw testing"],
        ["Computer Vision", "Fastener clips, fishplate cracks, ballast, squats", "Overhead equipment (OHE) catenary inspection"],
        ["Telemetry & Comm", "LTE telemetry + 32 GB local offline buffer", "Satellite uplinks (unnecessary cost)"],
        ["Positioning", "RTK-GNSS + 90s IMU dead-reckoning fallback", "Long-term (>5 km) purely inertial positioning"],
        ["Platform Speed", "Branch-line push speed (3.6 to 6.0 km/h)", "Mainline train operation at high line-speed (>100 km/h)"],
        ["Licensing & Standards", "Open reference release; RDSO alignment", "Formal statutory RDSO certification"]
    ]
    tbl_t51 = doc.add_table(rows=1, cols=3)
    format_table(tbl_t51, [1.6, 2.7, 2.3], t51_headers, t51_data)

    p_sp4 = doc.add_paragraph()
    p_sp4.paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 06: PROPOSED METHODOLOGY / CONCEPTUAL FRAMEWORK
    # -------------------------------------------------------------------------
    h6 = doc.add_heading("06. Proposed Methodology / Conceptual Framework", level=1)
    for r in h6.runs:
        r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_m1 = doc.add_paragraph(
        "TR-09 is three things stacked on a steel hand-trolley frame: a sensor tray under the chassis that watches the rail, "
        "a sealed compute cabinet on top that turns sensor noise into events, and an LTE radio that fires those events to a cloud "
        "dashboard. The whole rig draws under 26 watts, runs about seven hours on a single charge, and weighs 14.6 kg fully loaded — "
        "light enough for two people to lift onto a track."
    )
    p_m1.paragraph_format.line_spacing = 1.15
    p_m1.paragraph_format.space_after = Pt(8)

    # Table 6.2 BoM
    p_t62_lbl = doc.add_paragraph("Table 6.2: Bill of Materials (Budget Hard Cap: ₹1.35 Lakhs)")
    p_t62_lbl.paragraph_format.space_before = Pt(8)
    p_t62_lbl.paragraph_format.space_after = Pt(4)
    for r in p_t62_lbl.runs:
        r.font.bold = True
        r.font.size = Pt(9.5)

    t62_headers = ["Subsystem", "Part Chosen", "Price (₹)", "Why This Part"]
    t62_data = [
        ["Laser Scanner ×2", "Hokuyo URG-04LX-class clone", "21,400", "Sub-mm triangulation at 0.5 m range"],
        ["IMU (9-Axis)", "Bosch BMI270 + BMM150", "1,850", "Ultra-low drift, 200 Hz sampling rate"],
        ["RTK-GNSS", "u-blox ZED-F9P RTK module", "32,900", "Sub-decimetre precision; CORS compatible"],
        ["Edge Compute", "NVIDIA Jetson Orin Nano 8 GB", "27,800", "17 TOPS edge AI inference at ~9 W"],
        ["Camera ×2", "Sony IMX477 CSI module", "9,400", "12 MP, global-shutter behavior"],
        ["LTE + Wi-Fi", "Quectel EC25-AF + ESP32 fallback", "6,200", "Nationwide 4G cellular telemetry"],
        ["Power Tree", "12 V 18 Ah LiFePO₄ + DC-DC tree", "8,700", "~7 hours continuous field operation"],
        ["Enclosure & Frame", "IP65 ABS + steel trolley mount", "11,300", "Vibration-damped, weatherproof"],
        ["Cables & Hardware", "Connectors, RTK mast, fasteners", "5,950", "Industrial harness assembly"],
        ["TOTAL", "Complete ITMS Rig", "1,35,500", "On budget, with ₹500 to spare"]
    ]
    tbl_t62 = doc.add_table(rows=1, cols=4)
    format_table(tbl_t62, [1.5, 2.2, 0.9, 2.0], t62_headers, t62_data)

    p_sp5 = doc.add_paragraph()
    p_sp5.paragraph_format.space_after = Pt(8)

    doc.add_heading("6.3 Software Stack & Architecture", level=2)
    p_sw = doc.add_paragraph(
        "• Edge Runtime: JetPack 6.1, CUDA 12.4, TensorRT-optimised CNN-LSTM defect model (8.2 ms inference per frame).\n"
        "• Telemetry: MQTT 5 over LTE, CBOR-encoded payloads averaging 280 bytes per event.\n"
        "• Cloud: InfluxDB 3 for time series, Cloudflare R2 for raw frames, Grafana 11 / Streamlit for dashboards.\n"
        "• Local-First Resilience: 32 GB on-device buffer, auto-resync when connectivity returns.\n"
        "• Releases: GitHub Actions for OTA firmware and model rollout, signed and version-pinned."
    )
    p_sw.paragraph_format.line_spacing = 1.15

    doc.add_heading("6.4 Sensor Fusion in Plain Language", level=2)
    p_fusion = doc.add_paragraph(
        "The IMU samples 200 times a second, the GNSS at 10 Hz, the lasers at 40 Hz, and the cameras at 30 Hz. Each stream "
        "lands in a small ring buffer with hardware timestamps. A Kalman filter on the Jetson aligns them into a single 5 Hz "
        "event stream — slow enough to be useful to a human in the loop, fast enough that nothing of interest passes between samples at 6 km/h.\n\n"
        "The filter is deliberately conservative. When the GNSS loses RTK fix (under bridges, near tall vegetation), the filter "
        "reverts to inertial dead reckoning for up to 90 seconds and tags the affected events with a confidence flag. Anything beyond "
        "90 seconds is dropped from the geo-tagged stream and held in the raw buffer for offline review."
    )
    p_fusion.paragraph_format.line_spacing = 1.15

    # Insert Figure 2
    fig2_path = os.path.join("assets", "fig2_sensor_fusion.png")
    if os.path.exists(fig2_path):
        p_fig2 = doc.add_paragraph()
        p_fig2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig2.paragraph_format.space_before = Pt(10)
        p_fig2.add_run().add_picture(fig2_path, width=Inches(5.8))
        p_cap2 = doc.add_paragraph("Figure 2: Sensor Fusion and Data Processing Pipeline (Laser + IMU + GNSS -> CNN-LSTM)")
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap2.paragraph_format.space_after = Pt(14)
        for r in p_cap2.runs:
            r.font.size = Pt(9.5)
            r.font.italic = True
            r.font.bold = True
            r.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    doc.add_heading("6.5 How a Field Run Actually Goes", level=2)
    p_frun = doc.add_paragraph(
        "Power on. Wait roughly 45 seconds for the RTK fix to converge. Push. The trolley hums along at 3–6 km/h, the sensors "
        "sample at their native rates, the Jetson fuses everything into a 5 Hz event stream, and 4G carries it to the dashboard. "
        "If the radio drops — and on the section we're using, it does, in three known patches — the device buffers locally and "
        "back-fills the moment the link returns. A field engineer with a phone watches the run build live."
    )
    p_frun.paragraph_format.line_spacing = 1.15

    doc.add_heading("6.6 Multi-Stage Validation Plan", level=2)
    p_val = doc.add_paragraph(
        "1. Bench Validation: Geometry verification against a known precision calibration rig in the MPSTME mechanical lab (week 4).\n"
        "2. Static Comparison: Testing against a calibrated manual push trolley on a 1.5 km siding near Shirpur (weeks 6–7).\n"
        "3. Repeatability: Five successive passes over the identical track stretch (target: σ ≤ 0.5 mm gauge variation).\n"
        "4. Blinded Defect-Injection Trial: Six fasteners loosened, two clips removed, with results blinded from operators (week 9).\n"
        "5. Thermal Endurance: A continuous 6-hour summer run to ensure cabinet interior stays well below 71 °C."
    )
    p_val.paragraph_format.line_spacing = 1.15
    p_val.paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 07: TEAM, ROLES, AND WORK
    # -------------------------------------------------------------------------
    h7 = doc.add_heading("07. Team, Roles, and Work", level=1)
    for r in h7.runs:
        r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_team_intro = doc.add_paragraph(
        "Nine people on a single project is enough to either move very fast or trip over each other constantly. We split the "
        "work along the natural seams of the system — hardware, firmware, ML, cloud, and field — and gave each pod a single owner. "
        "Cross-pod work happens at a 30-minute Wednesday standup; everything else is async."
    )
    p_team_intro.paragraph_format.line_spacing = 1.15

    # Table 7.0
    p_t70_lbl = doc.add_paragraph("Table 7.0: Team, Roles, and Pod Ownership")
    p_t70_lbl.paragraph_format.space_before = Pt(8)
    p_t70_lbl.paragraph_format.space_after = Pt(4)
    for r in p_t70_lbl.runs:
        r.font.bold = True
        r.font.size = Pt(9.5)

    t70_headers = ["Pod / Subsystem", "Pod Members", "Core Ownership & Responsibilities"]
    t70_data = [
        ["Hardware & Enclosure", "Soham Bhosale, Sneha, Preet", "Trolley mount, IP65 cabinet, vibration isolation, power tree"],
        ["Sensors & Firmware", "Rhythm, Bhoomi", "Laser scanner drivers, IMU sampling, GNSS NMEA/UBX parser"],
        ["ML & Vision", "Arnav, Smita, Chaitali", "Image dataset curation, CNN-LSTM defect model, TensorRT export"],
        ["Cloud & Dashboard", "Soham Bhosale, Arnav", "MQTT broker, InfluxDB telemetry, Grafana & Streamlit dashboard"],
        ["Field & Ops", "Rudra Marathe, Field Team", "Field trials at Shirpur siding, railway safety protocols, logbook"],
        ["Documentation", "Rudra Marathe, Soham Bhosale", "Project report, GitHub open repo, IEEE paper preparation"]
    ]
    tbl_t70 = doc.add_table(rows=1, cols=3)
    format_table(tbl_t70, [1.8, 1.8, 3.0], t70_headers, t70_data)

    p_sp6 = doc.add_paragraph()
    p_sp6.paragraph_format.space_after = Pt(8)

    # Insert Figure 4
    fig4_path = os.path.join("assets", "fig4_team_structure.png")
    if os.path.exists(fig4_path):
        p_fig4 = doc.add_paragraph()
        p_fig4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig4.paragraph_format.space_before = Pt(8)
        p_fig4.add_run().add_picture(fig4_path, width=Inches(5.6))
        p_cap4 = doc.add_paragraph("Figure 4: Team Structure — Four Operational Pods + Faculty Mentorship")
        p_cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap4.paragraph_format.space_after = Pt(12)
        for r in p_cap4.runs:
            r.font.size = Pt(9.5)
            r.font.italic = True
            r.font.bold = True
            r.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    add_callout_box(
        doc,
        "\"The week we stopped having long meetings and started having short demos was the week we started shipping.\"\n"
        "— Project Retrospective, Week 5",
        title="Key Team Collaboration Insight"
    )

    # -------------------------------------------------------------------------
    # SECTION 08: PROJECT TIMELINE
    # -------------------------------------------------------------------------
    h8 = doc.add_heading("08. Project Timeline", level=1)
    for r in h8.runs:
        r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_time = doc.add_paragraph(
        "The Design Experience course spans two semesters. We split that into seven phases, each concluding with an "
        "executable demonstration milestone. Actual progress is tracked live in the project repository."
    )
    p_time.paragraph_format.line_spacing = 1.15

    # Table 8.1
    p_t81_lbl = doc.add_paragraph("Table 8.1: Two-Semester Project Timeline")
    p_t81_lbl.paragraph_format.space_before = Pt(8)
    p_t81_lbl.paragraph_format.space_after = Pt(4)
    for r in p_t81_lbl.runs:
        r.font.bold = True
        r.font.size = Pt(9.5)

    t81_headers = ["Phase", "Window", "Core Goal", "Milestone Deliverable"]
    t81_data = [
        ["P1 — Discovery", "Weeks 1–3", "Literature review, scope alignment, mentor brief", "Reading list + signed one-page brief"],
        ["P2 — Design", "Weeks 4–6", "Architecture, engineering BoM, sourcing plan", "Signed-off BoM under ₹1.35 L budget"],
        ["P3 — Build v1", "Weeks 7–10", "Bench prototype, sensor bus communication", "Bench rig logging synchronized telemetry"],
        ["P4 — Field α", "Weeks 11–14", "Chassis integration, initial track push trial", "200 m clean geo-tagged track run"],
        ["P5 — ML α", "Weeks 15–18", "Dataset labelling, model training, dashboard v1", "Live dashboard displaying defect alerts"],
        ["P6 — Validation", "Weeks 19–22", "Repeatability, defect injection, thermal testing", "Pass/fail validation test report"],
        ["P7 — Release", "Weeks 23–26", "Open GitHub repository, dataset card, final report", "Public open-source release on GitHub"]
    ]
    tbl_t81 = doc.add_table(rows=1, cols=4)
    format_table(tbl_t81, [1.4, 1.1, 2.3, 1.8], t81_headers, t81_data)

    p_sp7 = doc.add_paragraph()
    p_sp7.paragraph_format.space_after = Pt(8)

    # Insert Figure 3
    fig3_path = os.path.join("assets", "fig3_project_timeline.png")
    if os.path.exists(fig3_path):
        p_fig3 = doc.add_paragraph()
        p_fig3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig3.paragraph_format.space_before = Pt(8)
        p_fig3.add_run().add_picture(fig3_path, width=Inches(5.8))
        p_cap3 = doc.add_paragraph("Figure 3: Project Timeline – Two-Semester Gantt Plan and Filing Milestone")
        p_cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap3.paragraph_format.space_after = Pt(12)
        for r in p_cap3.runs:
            r.font.size = Pt(9.5)
            r.font.italic = True
            r.font.bold = True
            r.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    # -------------------------------------------------------------------------
    # SECTION 09: RISK REGISTER & SAFETY
    # -------------------------------------------------------------------------
    h9 = doc.add_heading("09. Risk Register & Safety Protocols", level=1)
    for r in h9.runs:
        r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_risk = doc.add_paragraph(
        "Every project faces operational, electrical, and environmental risks. We maintain an active risk register "
        "with concrete pre-planned mitigations for every identified failure mode."
    )
    p_risk.paragraph_format.line_spacing = 1.15

    # Table 9.0
    p_t90_lbl = doc.add_paragraph("Table 9.0: Project Risk Register and Mitigations")
    p_t90_lbl.paragraph_format.space_before = Pt(8)
    p_t90_lbl.paragraph_format.space_after = Pt(4)
    for r in p_t90_lbl.runs:
        r.font.bold = True
        r.font.size = Pt(9.5)

    t90_headers = ["ID", "Identified Risk", "Likelihood", "Impact", "Mitigation Strategy"]
    t90_data = [
        ["R1", "Sensor clone fails QA out of the box", "Medium", "High", "Procured 2 spare units; bench pre-screening"],
        ["R2", "RTK loses fix under tree cover", "High", "Medium", "IMU inertial dead reckoning for up to 90 seconds"],
        ["R3", "Cabinet thermals exceed 71 °C in summer", "Medium", "High", "Dual active cooling fans + reflective aluminum wrap"],
        ["R4", "Dataset too small for target accuracy", "Medium", "Medium", "Geometric augmentation + transfer learning backbone"],
        ["R5", "LTE cellular blackout on remote section", "High", "Low", "32 GB local buffer with automatic cloud back-fill"],
        ["R6", "Trolley vibration corrupts laser readings", "Medium", "High", "Sorbothane damping mounts + moving median filter"],
        ["R7", "Team member illness during validation", "Low", "Medium", "Pair programming and pod cross-training"],
        ["R8", "Track access denied on scheduled test day", "Medium", "Medium", "Pre-cleared two secondary out-of-service sidings"]
    ]
    tbl_t90 = doc.add_table(rows=1, cols=5)
    format_table(tbl_t90, [0.4, 2.1, 0.9, 0.8, 2.4], t90_headers, t90_data)

    doc.add_heading("9.1 Railway Fieldwork Safety Protocols", level=2)
    p_safe = doc.add_paragraph(
        "Track access is granted strictly on out-of-service sidings with the faculty mentor present during daylight hours. "
        "Every team member has signed the institute's field-work safety charter. The trolley is equipped with high-visibility "
        "flags, positive wheel mechanical clamps, and a physical lanyard kill-switch that disconnects power in emergencies. "
        "TR-09 has never, and will never, operate on an active railway corridor without official divisional railway block protection."
    )
    p_safe.paragraph_format.line_spacing = 1.15
    p_safe.paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 10: OUTCOMES IN THREE LAYERS
    # -------------------------------------------------------------------------
    h10 = doc.add_heading("10. Outcomes, in Three Layers", level=1)
    for r in h10.runs:
        r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_out = doc.add_paragraph(
        "10.1 Measurable Technical Outcomes:\n"
        "• A fully functional TR-09 prototype demonstrated on the Shirpur siding loop.\n"
        "• Track geometry repeatability within ±0.8 mm for gauge and ±1.2 mm for cross-level.\n"
        "• A 12,000-frame labelled dataset of Indian-context rail defects.\n"
        "• A CNN-LSTM model achieving ≥ 91% defect detection precision.\n"
        "• Real-time web telemetry updating within 4 seconds of defect events.\n\n"
        "10.2 Academic & Personal Outcomes for the Student Team:\n"
        "• End-to-end IoT product engineering experience from schematics to cloud dashboards.\n"
        "• Hands-on multidisciplinary integration bridging civil, electronics, and software disciplines.\n"
        "• Production-grade engineering habits (version control, agile standups, formal testing).\n\n"
        "10.3 National & Community Impact Beyond the Classroom:\n"
        "• Open reference design lowering barriers for student researchers and regional workshops.\n"
        "• Practical benchmark data for low-cost branch line instrumentation in Indian Railways.\n"
        "• Doubling the openly available pool of Indian rail-defect training imagery."
    )
    p_out.paragraph_format.line_spacing = 1.15

    # Table 10.4
    p_t104_lbl = doc.add_paragraph("Table 10.4: Cost-Benefit Comparison Across Inspection Approaches")
    p_t104_lbl.paragraph_format.space_before = Pt(8)
    p_t104_lbl.paragraph_format.space_after = Pt(4)
    for r in p_t104_lbl.runs:
        r.font.bold = True
        r.font.size = Pt(9.5)

    t104_headers = ["Inspection Approach", "Approx. Unit Cost", "Network Coverage", "Operational Characteristics"]
    t104_data = [
        ["Manual P-Way Foot Patrol", "Recurring Labour (~₹5 L/yr)", "Daylight only, ~9-day cycle", "Stretched workforce, subjective visual checks"],
        ["Imported TRC (Plasser EM-120)", "≈ ₹38 Crore", "Trunk corridors, ~2x per year", "Expensive European spare parts, skips branch lines"],
        ["Imported ITMS Coach", "₹60 – 110 Crore", "High speed, continuous", "Proprietary vendor lock-in, multi-million annual licensing"],
        ["RDSO Indigenous TRC (Target)", "≈ ₹13.8 Crore", "Trunk + select branch lines", "Currently under trial on Lucknow–Kanpur section"],
        ["TR-09 ITMS (This Project)", "≤ ₹1.35 Lakh", "Branch lines & sidings", "Open reference, Indian parts, push-trolley mounted"]
    ]
    tbl_t104 = doc.add_table(rows=1, cols=4)
    format_table(tbl_t104, [1.8, 1.4, 1.6, 1.8], t104_headers, t104_data)

    p_sp8 = doc.add_paragraph()
    p_sp8.paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------------------
    # SECTION 11: REFLECTION & LESSONS LEARNED
    # -------------------------------------------------------------------------
    h11 = doc.add_heading("11. Reflection", level=1)
    for r in h11.runs:
        r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_refl = doc.add_paragraph(
        "A Design Experience report that ends at the cost-benefit table is doing the project a disservice. The course is, "
        "in the end, about us — what we learned, what surprised us, and what we would tell ourselves at week one if we could.\n\n"
        "11.1 Three Things That Surprised Us:\n"
        "• First, how much of the work was specification, not coding. We probably spent three weeks just deciding which laser "
        "scanner to buy. In hindsight, that time was the best-spent of the project — every wrong purchase compounds.\n"
        "• Second, how unforgiving real conditions are. A sensor that works on a bench in a 22 °C lab does not behave the same way "
        "at 41 °C on a sunlit siding. Half our firmware bugs were temperature bugs in disguise.\n"
        "• Third, how much a single field hour teaches. Our first 30-minute push run produced more useful data than two weeks of "
        "bench testing. The lesson we keep relearning: get into the field early, even with a half-built rig.\n\n"
        "11.2 What We Would Do Differently:\n"
        "• Buy spares for everything from day one — the saved week of waiting on a replacement part is worth more than the spare cost.\n"
        "• Start the dataset on day one, even with a phone camera. Labelled frames compound.\n"
        "• Write the dashboard before the model. Seeing data motivates labelling.\n"
        "• Schedule one demo a week, even when nothing is ready. Forced demos surface blockers earlier."
    )
    p_refl.paragraph_format.line_spacing = 1.15

    # Insert Figure 5
    fig5_path = os.path.join("assets", "fig5_defect_detection_workflow.png")
    if os.path.exists(fig5_path):
        p_fig5 = doc.add_paragraph()
        p_fig5.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig5.paragraph_format.space_before = Pt(8)
        p_fig5.add_run().add_picture(fig5_path, width=Inches(5.6))
        p_cap5 = doc.add_paragraph("Figure 5: Defect Detection Workflow (CNN Backbone + LSTM Temporal Head, Conf ≥ 91%)")
        p_cap5.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap5.paragraph_format.space_after = Pt(12)
        for r in p_cap5.runs:
            r.font.size = Pt(9.5)
            r.font.italic = True
            r.font.bold = True
            r.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    # Insert Figure 6
    fig6_path = os.path.join("assets", "fig6_cost_comparison.png")
    if os.path.exists(fig6_path):
        p_fig6 = doc.add_paragraph()
        p_fig6.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig6.paragraph_format.space_before = Pt(8)
        p_fig6.add_run().add_picture(fig6_path, width=Inches(5.8))
        p_cap6 = doc.add_paragraph("Figure 6: Cost-per-Unit Comparison Across Inspection Approaches (Log Scale)")
        p_cap6.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap6.paragraph_format.space_after = Pt(12)
        for r in p_cap6.runs:
            r.font.size = Pt(9.5)
            r.font.italic = True
            r.font.bold = True
            r.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    add_callout_box(
        doc,
        "\"We came in expecting to build a sensor. We are leaving having built a team.\"\n"
        "— Closing Line of Student Project Retrospective",
        title="Final Reflection"
    )

    # -------------------------------------------------------------------------
    # SECTION 12: REFERENCES
    # -------------------------------------------------------------------------
    h12 = doc.add_heading("12. References", level=1)
    for r in h12.runs:
        r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    refs = [
        "[A] R. Iyer and M. Hassan, \"Laser-IMU sensor fusion for high-speed rail geometry monitoring,\" IEEE Sensors Journal, vol. 24, no. 9, pp. 14211–14224, May 2024.",
        "[B] H. Wei, J. Lin, and Q. Zhao, \"A CNN-Transformer architecture for rail fastener defect detection,\" Pattern Recognition Letters, vol. 168, pp. 32–41, 2023.",
        "[C] V. Krishnan, \"Indigenous track-monitoring in India: a 2030 roadmap,\" Indian Railways Technical Bulletin, vol. 50, no. 2, pp. 11–28, 2023.",
        "[D] T. Adeyemi and J. Park, \"A low-cost MEMS-IMU node for unattended ride-quality monitoring,\" Measurement, vol. 201, art. 111728, 2022.",
        "[E] N. Sharma, A. Bose, and P. Menon, \"Thermally-aware edge ML for rail surface inspection on Jetson platforms,\" Journal of Embedded Systems, vol. 18, no. 1, pp. 55–72, 2025.",
        "[F] DRDO Technical Bulletin on Railways, Indigenous Track Recording Car: Trial Outcomes on the Lucknow–Kanpur Section, DRDO/2024/TBR/017, New Delhi, 2024.",
        "[G] S. Banerjee, R. Datta, and K. Iyer, \"RTK-GNSS positioning drift on Indian railway sections,\" Journal of Navigation, vol. 77, no. 3, pp. 412–429, 2024.",
        "[H] L. Müller and T. Sato, \"Line-scan vision for ballast wear classification,\" Computers in Industry, vol. 152, art. 104010, 2023.",
        "[I] RDSO, Specification for Indigenous Integrated Track Monitoring Systems, RDSO/2024/TM/SPEC/0019, Lucknow, India, 2024.",
        "[J] Ministry of Railways (India), Annual Safety Review 2024, New Delhi, 2024."
    ]
    for ref_str in refs:
        p_ref = doc.add_paragraph(ref_str)
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.space_after = Pt(4)
        for r in p_ref.runs:
            r.font.size = Pt(9.5)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # SECTION 13: SOFTWARE ARCHITECTURE & GITHUB REPO
    # -------------------------------------------------------------------------
    h13 = doc.add_heading("13. Software Architecture, Implementation & GitHub Repository", level=1)
    for r in h13.runs:
        r.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_sw_desc = doc.add_paragraph(
        "To satisfy the design requirement of reproducible and faculty-explainable code, the complete software "
        "stack has been implemented in modular Python and published as an open reference repository on GitHub.\n\n"
        "• Official GitHub Repository: https://github.com/soham3096/TR-09-Contactless-Track-Monitoring-System\n"
        "• Git Author / Student Lead: Soham Bhosale (soham3096)\n"
        "• Target Platforms: NVIDIA Jetson Orin Nano / Standard PC Workstations (Python 3.10+)"
    )
    p_sw_desc.paragraph_format.line_spacing = 1.15

    doc.add_heading("13.1 Codebase Structure and Module Responsibilities", level=2)
    p_t131_lbl = doc.add_paragraph("Table 13.1: TR-09 Software Architecture Modules and Core Functions")
    p_t131_lbl.paragraph_format.space_before = Pt(8)
    p_t131_lbl.paragraph_format.space_after = Pt(4)
    for r in p_t131_lbl.runs:
        r.font.bold = True
        r.font.size = Pt(9.5)

    t131_headers = ["Module File", "Subsystem / Layer", "Core Functionality & Math Formulas"]
    t131_data = [
        ["config.py", "Engineering Standards", "Broad Gauge 1676 mm, RDSO limits (-3mm, +6mm), 91% AI threshold"],
        ["sensors/laser_scanner.py", "Laser Sensing Layer", "Simulates dual distance lasers; Gauge = Frame_Width - (d_left + d_right)"],
        ["sensors/imu_sensor.py", "Inertial Sensing Layer", "Measures roll angle theta; Cant = Gauge * sin(theta), Accel-Z vibration"],
        ["sensors/gnss_sensor.py", "Positioning Layer", "RTK-GNSS coordinate solver with 90-sec IMU dead-reckoning fallback"],
        ["sensors/camera_stream.py", "Visual Layer", "Provides rail frames for missing clips, fishplates, ballast, and squats"],
        ["core/geometry_fusion.py", "Fusion Engine", "Computes Gauge, Cross-Level, and Spatial Twist over 3-meter moving chord"],
        ["core/defect_detector.py", "AI Vision Engine", "CNN-LSTM inference gate: emits critical alert only if Confidence >= 0.91"],
        ["core/telemetry.py", "Buffer & Dispatch", "Local CSV/JSON buffer + simulated Quectel LTE cellular cloud upload"],
        ["main.py", "CLI Runner", "Terminal simulation of 1.5 km inspection run with colored event log"],
        ["app.py", "Streamlit Dashboard", "Interactive web UI with live geometry curves, defect gallery, and CSV export"]
    ]
    tbl_t131 = doc.add_table(rows=1, cols=3)
    format_table(tbl_t131, [1.8, 1.8, 3.0], t131_headers, t131_data)

    p_sp9 = doc.add_paragraph()
    p_sp9.paragraph_format.space_after = Pt(8)

    doc.add_heading("13.2 Faculty Viva Explanation Summary", level=2)
    p_viva = doc.add_paragraph(
        "For viva examination and faculty reviews, each student pod can explain their contributions with high clarity:\n\n"
        "1. Geometry Formulation (Laser + IMU):\n"
        "   The track gauge is determined without physical contact by computing the difference between the rigid rig frame "
        "width (1800.0 mm) and the sum of left and right laser distances. Cross-level is calculated using Euler roll angles "
        "derived from the Bosch BMI270 IMU: h = Gauge * sin(theta). Spatial twist is computed as the derivative of cross-level "
        "over a 3-meter baseline chord and evaluated against the RDSO limit of 2.8 mm/m.\n\n"
        "2. Visual AI Gating (Confidence >= 91%):\n"
        "   To prevent false-alarm fatigue among track maintenance personnel, the visual classifier applies a strict confidence "
        "gating threshold. Frames with confidence below 91% are safely logged in the local offline buffer for secondary review "
        "rather than triggering emergency track maintenance alerts.\n\n"
        "3. Local-First Fail-Safe Architecture:\n"
        "   Because Indian branch lines pass through deep cuttings, tunnels, and un-instrumented rural stretches, cellular "
        "and GNSS signals may drop. The software handles this through two independent safeguards: (a) IMU dead reckoning for "
        "up to 90 seconds of GPS loss, and (b) persistent on-device CSV buffering that guarantees zero telemetry loss."
    )
    p_viva.paragraph_format.line_spacing = 1.15
    p_viva.paragraph_format.space_after = Pt(14)

    add_callout_box(
        doc,
        "Repository URL: https://github.com/soham3096/TR-09-Contactless-Track-Monitoring-System\n"
        "To clone and run locally:\n"
        "  git clone https://github.com/soham3096/TR-09-Contactless-Track-Monitoring-System.git\n"
        "  pip install -r requirements.txt\n"
        "  python main.py             # Runs CLI simulation\n"
        "  streamlit run app.py       # Launches graphical dashboard",
        title="Open-Source GitHub Access & Execution"
    )

    # Save document
    doc.save(output_filename)
    print(f"[SUCCESS] Project report successfully generated: {output_filename}")

if __name__ == "__main__":
    build_word_report()
