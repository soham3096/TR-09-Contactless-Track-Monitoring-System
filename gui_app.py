"""
=============================================================================
TR-09 ITMS: Contactless Integrated Track Monitoring System
Native Desktop Graphical Inspection Application (GUI)
=============================================================================
Course: Design Experience (MBA Tech & B.Tech CE - 2nd Year)
Institute: SVKM's NMIMS MPSTME, Shirpur
Team: Soham Bhosale | Arnav | Rudra Marathe
Mentor: Prof. Chaitali Patil
=============================================================================
Features:
- Real Track Image Display with Bounding Box & Target Reticles
- View Mode Toggle: [Highlighted Fault] / [CV Feature Map] / [Raw Real Photo]
- Complete Technical Breakdown of HOW it is Detected & HOW the Track is Damaged
- Real-Time Track Gauge Curve Plot with RDSO Tolerance Boundaries
=============================================================================
"""

import os
import sys
import time
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import config
from sensors.laser_scanner import LaserScanner
from sensors.imu_sensor import IMUSensor
from sensors.gnss_sensor import GNSSReceiver
from sensors.camera_stream import CameraStream
from core.geometry_fusion import GeometryFusionEngine
from core.defect_detector import RailDefectDetector
from core.telemetry import TelemetryEngine

class TrackMonitoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TR-09 ITMS: Contactless Track Inspector | Real Defect Vision & Damage Analysis")
        self.root.geometry("1280x880")
        self.root.minsize(1100, 750)
        self.root.configure(bg="#F0F4F8")

        # Runtime State
        self.is_running = False
        self.is_paused = False
        self.step_delay = 0.08
        self.current_km = 0.0
        self.total_dist_km = 1.500
        self.step_m = 25.0
        self.after_id = None
        
        # View Mode: 'annotated', 'feature_map', 'raw'
        self.current_view_mode = "annotated"
        self.current_defect_info = None

        # Real-Time Graph Data
        self.x_data = []
        self.gauge_data = []

        # Defect Counts & Fault Review Registry
        self.defect_counts = {1: 0, 2: 0, 3: 0, 4: 0}
        self.detected_faults = []
        self.selected_fault_idx = -1
        self._selected_spot_line = None

        # Subsystems
        self.laser = LaserScanner()
        self.imu = IMUSensor()
        self.gnss = GNSSReceiver()
        self.camera = CameraStream()
        self.fusion = GeometryFusionEngine()
        self.detector = RailDefectDetector()
        self.telemetry = TelemetryEngine()

        self._build_ui()
        self.log_event("SYSTEM INITIALIZED", "NVIDIA Jetson Edge platform ready. Real track image dataset active.", "INFO")

    def _build_ui(self):
        # 1. HEADER BAR
        header_frame = tk.Frame(self.root, bg="#1B365D", height=70)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_lbl = tk.Label(
            header_frame,
            text="TR-09: INDIGENOUS CONTACTLESS INTEGRATED TRACK MONITORING SYSTEM",
            font=("Calibri", 15, "bold"),
            fg="#FFFFFF",
            bg="#1B365D"
        )
        title_lbl.pack(anchor="w", padx=20, pady=(6, 0))

        sub_lbl = tk.Label(
            header_frame,
            text="SVKM's NMIMS MPSTME • Real Track Image Vision & Fault Analysis | Team: Soham Bhosale, Arnav, Rudra Marathe (Mentor: Prof. Chaitali Patil)",
            font=("Calibri", 10),
            fg="#CBD5E0",
            bg="#1B365D"
        )
        sub_lbl.pack(anchor="w", padx=20, pady=(0, 6))

        # 2. MAIN SPLIT (LEFT: Telemetry & Controls, RIGHT: Vision & Damage)
        main_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg="#E2E8F0", bd=0, sashwidth=4)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=8, pady=6)

        left_frame = tk.Frame(main_paned, bg="#FFFFFF", padx=10, pady=8)
        main_paned.add(left_frame, minsize=400, width=440)

        right_frame = tk.Frame(main_paned, bg="#FFFFFF", padx=10, pady=8)
        main_paned.add(right_frame, minsize=650)

        self._build_left_pane(left_frame)
        self._build_right_pane(right_frame)

        # 3. BOTTOM EVENT LOG & CONTROLS
        bottom_frame = tk.Frame(self.root, bg="#EDF2F7", height=130)
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=8, pady=(0, 6))
        self._build_bottom_pane(bottom_frame)

    def _build_left_pane(self, parent):
        # INSPECTION CONTROLS
        ctrl_box = tk.LabelFrame(parent, text=" 🕹️ Inspection Controls ", font=("Calibri", 10, "bold"), bg="#FFFFFF", fg="#1B365D", padx=6, pady=6)
        ctrl_box.pack(fill=tk.X, pady=(0, 8))

        btn_row = tk.Frame(ctrl_box, bg="#FFFFFF")
        btn_row.pack(fill=tk.X)

        self.btn_start = tk.Button(
            btn_row, text="▶ Start Run", font=("Calibri", 9, "bold"), bg="#2E7D32", fg="#FFFFFF",
            activebackground="#1B5E20", activeforeground="#FFFFFF", width=10, relief=tk.FLAT, command=self.start_inspection
        )
        self.btn_start.pack(side=tk.LEFT, padx=2)

        self.btn_pause = tk.Button(
            btn_row, text="⏸ Pause", font=("Calibri", 9, "bold"), bg="#F57C00", fg="#FFFFFF",
            activebackground="#E65100", activeforeground="#FFFFFF", width=8, relief=tk.FLAT, state=tk.DISABLED, command=self.pause_inspection
        )
        self.btn_pause.pack(side=tk.LEFT, padx=2)

        self.btn_reset = tk.Button(
            btn_row, text="🔄 Reset", font=("Calibri", 9, "bold"), bg="#546E7A", fg="#FFFFFF",
            activebackground="#37474F", activeforeground="#FFFFFF", width=8, relief=tk.FLAT, command=self.reset_inspection
        )
        self.btn_reset.pack(side=tk.LEFT, padx=2)

        tk.Label(btn_row, text="Speed:", font=("Calibri", 9), bg="#FFFFFF").pack(side=tk.LEFT, padx=(6, 2))
        self.speed_var = tk.StringVar(value="Normal (1x)")
        speed_menu = ttk.Combobox(btn_row, textvariable=self.speed_var, values=["Normal (1x)", "Fast (3x)", "Ultra (8x)"], width=9, state="readonly")
        speed_menu.pack(side=tk.LEFT)
        speed_menu.bind("<<ComboboxSelected>>", self._change_speed)

        # TRACK CHAINAGE & PROGRESS
        dist_box = tk.LabelFrame(parent, text=" 📍 Track Position ", font=("Calibri", 10, "bold"), bg="#FFFFFF", fg="#1B365D", padx=6, pady=6)
        dist_box.pack(fill=tk.X, pady=(0, 8))

        d_row = tk.Frame(dist_box, bg="#FFFFFF")
        d_row.pack(fill=tk.X)
        tk.Label(d_row, text="Chainage:", font=("Calibri", 9), bg="#FFFFFF").pack(side=tk.LEFT)
        self.lbl_chainage = tk.Label(d_row, text="0.000 km / 1.500 km", font=("Calibri", 11, "bold"), fg="#1A365D", bg="#FFFFFF")
        self.lbl_chainage.pack(side=tk.RIGHT)

        self.prog_bar = ttk.Progressbar(dist_box, orient=tk.HORIZONTAL, mode='determinate', maximum=1.5)
        self.prog_bar.pack(fill=tk.X, pady=(4, 2))

        # GEOMETRY TELEMETRY READOUTS
        geo_box = tk.LabelFrame(parent, text=" 📐 Track Geometry (Broad Gauge: 1676 mm) ", font=("Calibri", 10, "bold"), bg="#FFFFFF", fg="#1B365D", padx=6, pady=6)
        geo_box.pack(fill=tk.X, pady=(0, 8))

        # Gauge
        g_row = tk.Frame(geo_box, bg="#F7FAFC", padx=6, pady=3, relief=tk.RIDGE, bd=1)
        g_row.pack(fill=tk.X, pady=2)
        tk.Label(g_row, text="Gauge:", font=("Calibri", 10, "bold"), bg="#F7FAFC").pack(side=tk.LEFT)
        self.lbl_gauge = tk.Label(g_row, text="1676.0 mm", font=("Calibri", 12, "bold"), fg="#2E7D32", bg="#F7FAFC")
        self.lbl_gauge.pack(side=tk.LEFT, padx=8)
        self.lbl_gauge_dev = tk.Label(g_row, text="(±0.0 mm)", font=("Calibri", 9), fg="#718096", bg="#F7FAFC")
        self.lbl_gauge_dev.pack(side=tk.LEFT)
        self.lbl_gauge_status = tk.Label(g_row, text="NORMAL", font=("Calibri", 8, "bold"), bg="#2E7D32", fg="#FFFFFF", padx=5)
        self.lbl_gauge_status.pack(side=tk.RIGHT)

        # Cross-Level
        c_row = tk.Frame(geo_box, bg="#F7FAFC", padx=6, pady=3, relief=tk.RIDGE, bd=1)
        c_row.pack(fill=tk.X, pady=2)
        tk.Label(c_row, text="Cross-Level:", font=("Calibri", 10, "bold"), bg="#F7FAFC").pack(side=tk.LEFT)
        self.lbl_cant = tk.Label(c_row, text="0.0 mm", font=("Calibri", 11, "bold"), fg="#1A365D", bg="#F7FAFC")
        self.lbl_cant.pack(side=tk.LEFT, padx=8)
        self.lbl_cant_status = tk.Label(c_row, text="LEVEL (±4mm)", font=("Calibri", 8), bg="#EDF2F7", fg="#4A5568", padx=4)
        self.lbl_cant_status.pack(side=tk.RIGHT)

        # Twist
        t_row = tk.Frame(geo_box, bg="#F7FAFC", padx=6, pady=3, relief=tk.RIDGE, bd=1)
        t_row.pack(fill=tk.X, pady=2)
        tk.Label(t_row, text="Spatial Twist:", font=("Calibri", 10, "bold"), bg="#F7FAFC").pack(side=tk.LEFT)
        self.lbl_twist = tk.Label(t_row, text="0.0 mm/m", font=("Calibri", 11, "bold"), fg="#1A365D", bg="#F7FAFC")
        self.lbl_twist.pack(side=tk.LEFT, padx=8)
        self.lbl_twist_status = tk.Label(t_row, text="SAFE (≤2.8)", font=("Calibri", 8), bg="#EDF2F7", fg="#4A5568", padx=4)
        self.lbl_twist_status.pack(side=tk.RIGHT)

        # SUBSYSTEM & GPS
        stat_box = tk.LabelFrame(parent, text=" 🛰️ Subsystems & RTK Navigation ", font=("Calibri", 10, "bold"), bg="#FFFFFF", fg="#1B365D", padx=6, pady=6)
        stat_box.pack(fill=tk.X, pady=(0, 8))

        gps_row = tk.Frame(stat_box, bg="#FFFFFF")
        gps_row.pack(fill=tk.X, pady=1)
        tk.Label(gps_row, text="GPS Fix:", font=("Calibri", 8, "bold"), bg="#FFFFFF").pack(side=tk.LEFT)
        self.lbl_gps_fix = tk.Label(gps_row, text="RTK_FIXED (Sub-decimetre)", font=("Calibri", 8), fg="#2E7D32", bg="#FFFFFF")
        self.lbl_gps_fix.pack(side=tk.LEFT, padx=4)

        coords_row = tk.Frame(stat_box, bg="#FFFFFF")
        coords_row.pack(fill=tk.X, pady=1)
        tk.Label(coords_row, text="Coords:", font=("Calibri", 8, "bold"), bg="#FFFFFF").pack(side=tk.LEFT)
        self.lbl_coords = tk.Label(coords_row, text="21.311200° N, 74.881400° E", font=("Calibri", 8), fg="#4A5568", bg="#FFFFFF")
        self.lbl_coords.pack(side=tk.LEFT, padx=4)

        # DEFECT COUNTERS & AUDIT QUICK ACCESS
        cnt_box = tk.LabelFrame(parent, text=" 🚩 Detected Defect Summary (Click to Review) ", font=("Calibri", 10, "bold"), bg="#FFFFFF", fg="#1B365D", padx=6, pady=4)
        cnt_box.pack(fill=tk.X)

        self.defect_rows = []
        def_info = [
            ("Missing Fastener", 1, "#C62828", 0),
            ("Cracked Fishplate", 2, "#C62828", 1),
            ("Ballast Deficiency", 3, "#EF6C00", 2),
            ("Rail Surface Squat", 4, "#C62828", 3)
        ]
        
        for name, d_id, col, spot_idx in def_info:
            row = tk.Frame(cnt_box, bg="#FFFFFF")
            row.pack(fill=tk.X, pady=1)
            lbl = tk.Label(row, text=f"• {name}: 0", font=("Calibri", 8), bg="#FFFFFF", fg=col)
            lbl.pack(side=tk.LEFT)
            btn = tk.Button(
                row, text="🔍 View Spot", font=("Calibri", 7, "bold"),
                bg="#EDF2F7", fg="#2B6CB0", relief=tk.FLAT, padx=4, pady=0,
                command=lambda s=spot_idx: self.select_fault_spot(s)
            )
            btn.pack(side=tk.RIGHT)
            self.defect_rows.append((lbl, btn, d_id, name))

        btn_all_gallery = tk.Button(
            cnt_box, text="🖼️ Open All Fault Spots Gallery", font=("Calibri", 8, "bold"),
            bg="#6B46C1", fg="#FFFFFF", relief=tk.FLAT, pady=2,
            command=self.open_fault_gallery
        )
        btn_all_gallery.pack(fill=tk.X, pady=(4, 2))

    def _build_right_pane(self, parent):
        # 1. REAL CAMERA FEED & FAULT SPOT HIGHLIGHTING
        cam_box = tk.LabelFrame(parent, text=" 📷 Real Track Vision • Fault Spot Highlighting & Detection Mechanism ", font=("Calibri", 11, "bold"), bg="#FFFFFF", fg="#1B365D", padx=8, pady=6)
        cam_box.pack(fill=tk.X, pady=(0, 6))

        # View Mode Toggle Buttons
        mode_bar = tk.Frame(cam_box, bg="#FFFFFF")
        mode_bar.pack(fill=tk.X, pady=(0, 4))
        
        tk.Label(mode_bar, text="Camera View:", font=("Calibri", 9, "bold"), bg="#FFFFFF", fg="#1B365D").pack(side=tk.LEFT, padx=(0, 6))
        
        self.btn_view_annot = tk.Button(mode_bar, text="🎯 Highlighted Fault Spot", font=("Calibri", 8, "bold"), bg="#2B6CB0", fg="#FFFFFF", relief=tk.FLAT, padx=6, command=lambda: self.set_view_mode("annotated"))
        self.btn_view_annot.pack(side=tk.LEFT, padx=2)

        self.btn_view_feat = tk.Button(mode_bar, text="🔬 CV Feature Activation Map", font=("Calibri", 8), bg="#EDF2F7", fg="#2D3748", relief=tk.FLAT, padx=6, command=lambda: self.set_view_mode("feature_map"))
        self.btn_view_feat.pack(side=tk.LEFT, padx=2)

        self.btn_view_raw = tk.Button(mode_bar, text="📸 Raw Real Track Photo", font=("Calibri", 8), bg="#EDF2F7", fg="#2D3748", relief=tk.FLAT, padx=6, command=lambda: self.set_view_mode("raw"))
        self.btn_view_raw.pack(side=tk.LEFT, padx=2)

        btn_gallery = tk.Button(mode_bar, text="🖼️ Fault Spots Gallery", font=("Calibri", 8, "bold"), bg="#6B46C1", fg="#FFFFFF", relief=tk.FLAT, padx=6, command=self.open_fault_gallery)
        btn_gallery.pack(side=tk.RIGHT, padx=2)

        # Fault Spots Selector Bar (Active especially after test is run!)
        self.fault_bar = tk.Frame(cam_box, bg="#EDF2F7", padx=4, pady=3, relief=tk.GROOVE, bd=1)
        self.fault_bar.pack(fill=tk.X, pady=(0, 6))

        tk.Label(self.fault_bar, text="📍 Review Fault Spots:", font=("Calibri", 9, "bold"), bg="#EDF2F7", fg="#1B365D").pack(side=tk.LEFT, padx=(2, 6))

        self.btn_prev_fault = tk.Button(self.fault_bar, text="◀ Prev", font=("Calibri", 8, "bold"), bg="#CBD5E0", fg="#4A5568", relief=tk.FLAT, padx=5, state=tk.DISABLED, command=self.prev_fault_spot)
        self.btn_prev_fault.pack(side=tk.LEFT, padx=2)

        self.fault_buttons = []
        spot_configs = [
            ("Spot 1: Fastener (0.25km)", 1),
            ("Spot 2: Fishplate (0.60km)", 2),
            ("Spot 3: Ballast (0.95km)", 3),
            ("Spot 4: Squat (1.30km)", 4),
        ]
        for i, (text_label, def_id) in enumerate(spot_configs):
            btn = tk.Button(
                self.fault_bar, text=text_label, font=("Calibri", 8),
                bg="#E2E8F0", fg="#4A5568", relief=tk.FLAT, padx=5,
                command=lambda idx=i: self.select_fault_spot(idx)
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.fault_buttons.append(btn)

        self.btn_next_fault = tk.Button(self.fault_bar, text="Next ▶", font=("Calibri", 8, "bold"), bg="#CBD5E0", fg="#4A5568", relief=tk.FLAT, padx=5, state=tk.DISABLED, command=self.next_fault_spot)
        self.btn_next_fault.pack(side=tk.LEFT, padx=2)

        # Image & Detailed Breakdown Row
        vis_row = tk.Frame(cam_box, bg="#FFFFFF")
        vis_row.pack(fill=tk.X)

        # Left: Image Canvas (380x250)
        self.cam_canvas = tk.Label(vis_row, bg="#1A202C", width=380, height=240)
        self.cam_canvas.pack(side=tk.LEFT, padx=(0, 8))

        # Right: Rich Damage & Detection Explanation Card
        self.detail_card = tk.Frame(vis_row, bg="#F8FAFC", padx=8, pady=6, relief=tk.RIDGE, bd=1)
        self.detail_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.lbl_fault_title = tk.Label(self.detail_card, text="TRACK STATUS: NORMAL (SAFE)", font=("Calibri", 10, "bold"), bg="#2E7D32", fg="#FFFFFF", padx=6, pady=2)
        self.lbl_fault_title.pack(fill=tk.X, pady=(0, 4))

        # Fault Spot Location
        spot_frame = tk.Frame(self.detail_card, bg="#F8FAFC")
        spot_frame.pack(fill=tk.X, pady=1)
        tk.Label(spot_frame, text="📍 Fault Spot:", font=("Calibri", 8, "bold"), bg="#F8FAFC", fg="#1B365D").pack(side=tk.LEFT)
        self.lbl_spot_loc = tk.Label(spot_frame, text="None (Track Crown Clear)", font=("Calibri", 8), bg="#F8FAFC", fg="#2D3748")
        self.lbl_spot_loc.pack(side=tk.LEFT, padx=4)

        # How Detected
        how_frame = tk.Frame(self.detail_card, bg="#F8FAFC")
        how_frame.pack(fill=tk.X, pady=1)
        tk.Label(how_frame, text="🔍 How Detected:", font=("Calibri", 8, "bold"), bg="#F8FAFC", fg="#2B6CB0").pack(anchor="w")
        self.lbl_how_detected = tk.Label(how_frame, text="Edge gradient continuity and template correlation verify intact fastener assemblies.", font=("Calibri", 8), bg="#F8FAFC", fg="#4A5568", justify=tk.LEFT, wraplength=340)
        self.lbl_how_detected.pack(anchor="w", padx=4)

        # Track Damage
        dmg_frame = tk.Frame(self.detail_card, bg="#F8FAFC")
        dmg_frame.pack(fill=tk.X, pady=1)
        tk.Label(dmg_frame, text="⚠️ Track Damage:", font=("Calibri", 8, "bold"), bg="#F8FAFC", fg="#C62828").pack(anchor="w")
        self.lbl_damage_desc = tk.Label(dmg_frame, text="Zero structural degradation. Steel rails, concrete ties, and ballast shoulder intact.", font=("Calibri", 8), bg="#F8FAFC", fg="#4A5568", justify=tk.LEFT, wraplength=340)
        self.lbl_damage_desc.pack(anchor="w", padx=4)

        # Derailment Hazard
        haz_frame = tk.Frame(self.detail_card, bg="#F8FAFC")
        haz_frame.pack(fill=tk.X, pady=1)
        tk.Label(haz_frame, text="🚨 Derailment Hazard:", font=("Calibri", 8, "bold"), bg="#F8FAFC", fg="#C62828").pack(anchor="w")
        self.lbl_hazard = tk.Label(haz_frame, text="None under line-speed operation.", font=("Calibri", 8), bg="#F8FAFC", fg="#4A5568", justify=tk.LEFT, wraplength=340)
        self.lbl_hazard.pack(anchor="w", padx=4)

        # Initial normal image display
        init_img = os.path.join(config.TEST_FRAMES_DIR, "normal_rail.png")
        if os.path.exists(init_img):
            self._render_current_image(init_img)

        # 2. REAL-TIME TRACK GAUGE PROFILE CHART
        graph_box = tk.LabelFrame(parent, text=" 📊 Real-Time Track Gauge Profile (Indian Railways RDSO Limits: 1673 - 1682 mm) ", font=("Calibri", 10, "bold"), bg="#FFFFFF", fg="#1B365D", padx=4, pady=2)
        graph_box.pack(fill=tk.BOTH, expand=True)

        self.fig = Figure(figsize=(6.2, 2.5), dpi=100)
        self.fig.patch.set_facecolor('#FFFFFF')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#F8FAFC')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_box)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self._init_chart()

    def _init_chart(self):
        self._selected_spot_line = None
        self.ax.clear()
        self.ax.set_title("Broad Gauge vs Track Chainage", fontsize=9, fontweight="bold", color="#1A365D", pad=4)
        self.ax.set_xlabel("Track Distance (km)", fontsize=7.5, color="#4A5568")
        self.ax.set_ylabel("Measured Gauge (mm)", fontsize=7.5, color="#4A5568")
        self.ax.set_xlim(0, 1.5)
        self.ax.set_ylim(1666, 1690)
        self.ax.tick_params(labelsize=7.5)
        self.ax.grid(True, linestyle="--", alpha=0.5)

        self.ax.axhline(1676.0, color="#2E7D32", linestyle="-", linewidth=1.2, label="Nominal Broad Gauge (1676 mm)")
        self.ax.axhline(1682.0, color="#C62828", linestyle="--", linewidth=1.0, label="Slack Limit (+6mm)")
        self.ax.axhline(1673.0, color="#C62828", linestyle="--", linewidth=1.0, label="Tight Limit (-3mm)")
        self.ax.legend(loc="upper right", fontsize=6.5)
        self.line_gauge, = self.ax.plot([], [], color="#1E88E5", linewidth=1.5, label="Measured Gauge")
        self.canvas.draw()

    def _build_bottom_pane(self, parent):
        top_row = tk.Frame(parent, bg="#EDF2F7")
        top_row.pack(fill=tk.X, pady=(2, 2))

        tk.Label(top_row, text=" 📜 Telemetry Event Log", font=("Calibri", 9, "bold"), bg="#EDF2F7", fg="#1B365D").pack(side=tk.LEFT)

        btn_view_csv = tk.Button(top_row, text="📊 Open CSV Log", font=("Calibri", 8, "bold"), bg="#4A5568", fg="#FFFFFF", relief=tk.FLAT, padx=6, command=self.open_csv_log)
        btn_view_csv.pack(side=tk.RIGHT, padx=3)

        btn_view_report = tk.Button(top_row, text="📄 Open Word Report (.docx)", font=("Calibri", 8, "bold"), bg="#2B6CB0", fg="#FFFFFF", relief=tk.FLAT, padx=6, command=self.open_word_report)
        btn_view_report.pack(side=tk.RIGHT, padx=3)

        self.log_text = tk.Text(parent, height=4, font=("Consolas", 9), bg="#1A202C", fg="#E2E8F0", wrap=tk.WORD, relief=tk.FLAT)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        self.log_text.tag_config("INFO", foreground="#63B3ED")
        self.log_text.tag_config("NORMAL", foreground="#68D391")
        self.log_text.tag_config("WARNING", foreground="#F6AD55")
        self.log_text.tag_config("CRITICAL", foreground="#FC8181")
        self.log_text.tag_config("DEFECT", foreground="#FEB2B2", font=("Consolas", 9, "bold"))

    def log_event(self, event_type, message, tag="INFO"):
        t_str = time.strftime("%H:%M:%S")
        entry = f"[{t_str}] [{event_type:<10}] {message}\n"
        self.log_text.insert(tk.END, entry, tag)
        self.log_text.see(tk.END)

    def set_view_mode(self, mode):
        """Switches between Highlighted Detection, Feature Activation Map, and Raw Photo."""
        self.current_view_mode = mode
        
        # Update button highlights
        self.btn_view_annot.configure(bg="#2B6CB0" if mode == "annotated" else "#EDF2F7", fg="#FFFFFF" if mode == "annotated" else "#2D3748")
        self.btn_view_feat.configure(bg="#2B6CB0" if mode == "feature_map" else "#EDF2F7", fg="#FFFFFF" if mode == "feature_map" else "#2D3748")
        self.btn_view_raw.configure(bg="#2B6CB0" if mode == "raw" else "#EDF2F7", fg="#FFFFFF" if mode == "raw" else "#2D3748")

        if self.current_defect_info:
            self._display_defect_view(self.current_defect_info)

    def _render_current_image(self, img_path):
        try:
            im = Image.open(img_path)
            im = im.resize((380, 240), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(im)
            self.cam_canvas.configure(image=photo)
            self.cam_canvas.image = photo
        except Exception as e:
            pass

    def _display_defect_view(self, defect):
        """Renders the appropriate image based on current_view_mode and updates detailed labels."""
        if self.current_view_mode == "feature_map":
            target_path = defect.get("feature_map_path") or defect.get("frame_path")
        elif self.current_view_mode == "raw":
            target_path = defect.get("raw_frame_path") or defect.get("frame_path")
        else:
            target_path = defect.get("frame_path")

        if target_path and os.path.exists(target_path):
            self._render_current_image(target_path)

        # Update Detail Card
        if defect.get("detected"):
            title_prefix = f"🚨 FAULT SPOT #{self.selected_fault_idx + 1}: " if self.selected_fault_idx >= 0 else "🚨 FAULT: "
            self.lbl_fault_title.configure(text=f"{title_prefix}{defect['defect_name'].upper()} ({defect['confidence']*100:.1f}%)", bg="#C62828")
            bbox = defect.get("bounding_box")
            bbox_str = f"Target Reticle Bounding Box {bbox}" if bbox else "Active Region"
            self.lbl_spot_loc.configure(text=f"{bbox_str} @ Siding Km {defect.get('chainage_km', 0.0):.3f}")
            self.lbl_how_detected.configure(text=defect.get("detection_method", "N/A"))
            self.lbl_damage_desc.configure(text=defect.get("damage_description", "N/A"))
            self.lbl_hazard.configure(text=f"{defect.get('derailment_risk', 'N/A')} • Action: {defect.get('pway_action', 'N/A')}")
        else:
            self.lbl_fault_title.configure(text="TRACK STATUS: NORMAL (SAFE)", bg="#2E7D32")
            self.lbl_spot_loc.configure(text="None (Track Alignment Clear)")
            self.lbl_how_detected.configure(text="Edge continuity and template matching confirm intact fastening components.")
            self.lbl_damage_desc.configure(text="Zero structural damage. Ballast shoulder and sleeper seats secure.")
            self.lbl_hazard.configure(text="Safe operating condition under line speed.")

    def _change_speed(self, event=None):
        val = self.speed_var.get()
        if "Fast" in val:
            self.step_delay = 0.03
        elif "Ultra" in val:
            self.step_delay = 0.008
        else:
            self.step_delay = 0.08

    # -------------------------------------------------------------
    # SIMULATION LOOP (Event-driven via root.after for 100% thread safety)
    # -------------------------------------------------------------
    def start_inspection(self):
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self.btn_start.configure(state=tk.DISABLED)
            self.btn_pause.configure(state=tk.NORMAL)
            self.log_event("RUN START", "Trolley inspection initiated. Real track image dataset active.", "INFO")
            self._schedule_step()
        elif self.is_paused:
            self.is_paused = False
            self.btn_pause.configure(text="⏸ Pause", bg="#F57C00")
            self.log_event("RESUMED", "Trolley inspection resumed.", "INFO")
            self._schedule_step()

    def pause_inspection(self):
        if self.is_running and not self.is_paused:
            self.is_paused = True
            if self.after_id is not None:
                self.root.after_cancel(self.after_id)
                self.after_id = None
            self.btn_pause.configure(text="▶ Resume", bg="#2E7D32")
            self.log_event("PAUSED", "Trolley halted. Sensor acquisition paused.", "WARNING")
        elif self.is_running and self.is_paused:
            self.start_inspection()

    def reset_inspection(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.is_running = False
        self.is_paused = False
        self.current_km = 0.0
        self.btn_start.configure(state=tk.NORMAL)
        self.btn_pause.configure(state=tk.DISABLED, text="⏸ Pause", bg="#F57C00")
        
        self.gnss = GNSSReceiver()
        self.fusion = GeometryFusionEngine()
        self.telemetry = TelemetryEngine()
        self.defect_counts = {1: 0, 2: 0, 3: 0, 4: 0}
        self.detected_faults.clear()
        self.selected_fault_idx = -1
        self._selected_spot_line = None
        self.x_data.clear()
        self.gauge_data.clear()

        self.prog_bar['value'] = 0.0
        self.lbl_chainage.configure(text="0.000 km / 1.500 km")
        self.lbl_gauge.configure(text="1676.0 mm", fg="#2E7D32")
        self.lbl_gauge_dev.configure(text="(±0.0 mm)")
        self.lbl_gauge_status.configure(text="NORMAL", bg="#2E7D32")
        self.lbl_cant.configure(text="0.0 mm")
        self.lbl_twist.configure(text="0.0 mm/m")
        self._update_defect_counters()
        self._reset_fault_buttons_state()
        self._init_chart()
        
        init_img = os.path.join(config.TEST_FRAMES_DIR, "normal_rail.png")
        if os.path.exists(init_img):
            self._render_current_image(init_img)
        self.log_event("RESET", "Simulation reset to Km 0.000.", "INFO")

    def _update_defect_counters(self):
        for lbl, btn, d_id, name in self.defect_rows:
            count = self.defect_counts.get(d_id, 0)
            lbl.configure(text=f"• {name}: {count}")
            if count > 0:
                btn.configure(bg="#2B6CB0", fg="#FFFFFF")
            else:
                btn.configure(bg="#EDF2F7", fg="#718096")

    def _schedule_step(self):
        if self.is_running and not self.is_paused:
            delay_ms = max(5, int(self.step_delay * 1000))
            self.after_id = self.root.after(delay_ms, self._step_simulation)

    def _step_simulation(self):
        if not self.is_running or self.is_paused:
            return

        if self.current_km > self.total_dist_km:
            self._on_inspection_finished()
            return

        inject_gauge_widening = (0.840 <= self.current_km <= 0.880)
        inject_cant = (0.420 <= self.current_km <= 0.450)
        simulate_rtk_loss = (1.100 <= self.current_km <= 1.180)

        dl, dr = self.laser.read_measurements(self.current_km, inject_gauge_defect=inject_gauge_widening)
        imu_data = self.imu.read_motion(self.current_km, inject_cant_defect=inject_cant)
        gnss_data = self.gnss.update_position(self.step_m, force_rtk_loss=simulate_rtk_loss)
        self.current_km = gnss_data["chainage_km"]

        geo = self.fusion.process_sample(dl, dr, imu_data, gnss_data)
        
        # Acquire Real Photographic Frame & Defect Analysis
        frame_info = self.camera.capture_frame(self.current_km)
        defect = self.detector.analyze_frame(frame_info)
        defect["chainage_km"] = self.current_km

        self.telemetry.log_record(geo, defect, lte_online=not simulate_rtk_loss)
        self._update_ui_state(self.current_km, geo, defect, gnss_data)

        if self.current_km <= self.total_dist_km:
            self._schedule_step()
        else:
            self._on_inspection_finished()

    def _update_ui_state(self, current_km, geo, defect, gnss_data):
        self.lbl_chainage.configure(text=f"{current_km:.3f} km / 1.500 km")
        self.prog_bar['value'] = current_km

        g_val = geo["gauge_mm"]
        dev_val = geo["gauge_deviation_mm"]
        self.lbl_gauge.configure(text=f"{g_val:.1f} mm")
        self.lbl_gauge_dev.configure(text=f"({dev_val:+.1f} mm)")

        if geo["severity"] == "CRITICAL":
            self.lbl_gauge.configure(fg="#C62828")
            self.lbl_gauge_status.configure(text="CRITICAL", bg="#C62828")
        elif geo["severity"] == "WARNING":
            self.lbl_gauge.configure(fg="#EF6C00")
            self.lbl_gauge_status.configure(text="WARNING", bg="#EF6C00")
        else:
            self.lbl_gauge.configure(fg="#2E7D32")
            self.lbl_gauge_status.configure(text="NORMAL", bg="#2E7D32")

        self.lbl_cant.configure(text=f"{geo['cross_level_mm']:+.1f} mm")
        self.lbl_twist.configure(text=f"{geo['twist_mm_per_m']:.1f} mm/m")

        fix_str = gnss_data["fix_status"]
        self.lbl_gps_fix.configure(text=fix_str, fg="#2E7D32" if "FIXED" in fix_str else "#E65100")
        self.lbl_coords.configure(text=f"{gnss_data['latitude']:.6f}° N, {gnss_data['longitude']:.6f}° E")

        # Save current defect info and update view
        self.current_defect_info = defect
        self._display_defect_view(defect)

        if defect["detected"]:
            d_id = defect["defect_id"]
            if d_id in self.defect_counts:
                self.defect_counts[d_id] += 1
            self._update_defect_counters()

            # Record fault spot if not already recorded
            if not any(f["defect_id"] == d_id for f in self.detected_faults):
                rec = defect.copy()
                rec["chainage_km"] = current_km
                rec["coords"] = f"{gnss_data['latitude']:.6f}° N, {gnss_data['longitude']:.6f}° E"
                self.detected_faults.append(rec)
                self.detected_faults.sort(key=lambda x: x.get("chainage_km", 0.0))
                self._update_fault_buttons_state()

            self.log_event("FAULT SPOT", f"Km {current_km:.3f}: {defect['defect_name']} ({defect['confidence']*100:.1f}%) | Reticle {defect['bounding_box']}", "DEFECT")
            self.log_event("HOW DETECTED", f"{defect['detection_method'][:60]}...", "INFO")
            self.log_event("DAMAGE", f"{defect['damage_description'][:60]}...", "WARNING")

        if geo["severity"] != "NORMAL" and not defect["detected"]:
            self.log_event("GEOMETRY", f"Km {current_km:.3f}: {geo['status_description']} (Gauge: {g_val:.1f} mm)", geo["severity"])

        self.x_data.append(current_km)
        self.gauge_data.append(g_val)
        if len(self.x_data) % 2 == 0:
            self.line_gauge.set_data(self.x_data, self.gauge_data)
            self.canvas.draw_idle()

    def _on_inspection_finished(self):
        self.is_running = False
        self.btn_start.configure(state=tk.NORMAL)
        self.btn_pause.configure(state=tk.DISABLED)

        # Ensure all 4 test fault spots are loaded into registry
        self._ensure_all_faults_populated()
        total_defects = len(self.detected_faults)

        self.log_event("FINISHED", f"1.500 km inspection complete! {total_defects} fault spots geo-tagged on real photos.", "NORMAL")
        self.log_event("AUDIT", "Review mode active: All fault spots ready for review. Displaying Spot 1.", "DEFECT")

        # Automatically display Fault Spot 1 immediately after the test run finishes!
        self.select_fault_spot(0)

        # Draw defect markers on the Matplotlib profile chart
        self._plot_fault_markers_on_chart()

        messagebox.showinfo(
            "Inspection Complete • Fault Spots Ready for Review",
            f"✅ 1.500 km Track Siding Inspection Complete!\n\n"
            f"Total Fault Spots Detected: {total_defects}\n"
            f"• Spot 1 (Km 0.250): Missing Elastic Rail Clip\n"
            f"• Spot 2 (Km 0.600): Cracked Fishplate Rail Joint\n"
            f"• Spot 3 (Km 0.950): Ballast Washout Void\n"
            f"• Spot 4 (Km 1.300): Rail Head Surface Squat\n\n"
            f"Fault Spot 1 is now loaded on your screen with highlighted targeting reticle, "
            f"algorithmic detection explanation, and track damage breakdown.\n\n"
            f"Click any 'Spot' button (Spot 1, Spot 2, Spot 3, Spot 4) or click 'Fault Spots Gallery' "
            f"to examine each detected defect."
        )

    # -------------------------------------------------------------
    # FAULT SPOT REVIEW & GALLERY AUDIT METHODS
    # -------------------------------------------------------------
    def _ensure_all_faults_populated(self):
        """Pre-populates known defect records from camera frames and config if not yet populated during run."""
        if len(self.detected_faults) >= 4:
            return
            
        test_chainages = [0.250, 0.600, 0.950, 1.300]
        for km in test_chainages:
            frame_info = self.camera.capture_frame(km)
            defect = self.detector.analyze_frame(frame_info)
            defect["chainage_km"] = km
            defect["coords"] = f"{config.GEO_START_LAT + (km * 0.00009):.6f}° N, {config.GEO_START_LON + (km * 0.00015):.6f}° E"
            
            if not any(f["defect_id"] == defect["defect_id"] for f in self.detected_faults):
                self.detected_faults.append(defect)
        
        self.detected_faults.sort(key=lambda x: x.get("chainage_km", 0.0))
        self._update_fault_buttons_state()

    def select_fault_spot(self, idx):
        """Displays the selected fault spot in the camera view, updating all damage and detection details."""
        if not self.detected_faults:
            self._ensure_all_faults_populated()

        if 0 <= idx < len(self.detected_faults):
            self.selected_fault_idx = idx
            fault = self.detected_faults[idx]
            self.current_defect_info = fault
            
            # Update the camera view and details
            self._display_defect_view(fault)
            
            # Update fault title to indicate spot number
            total = len(self.detected_faults)
            self.lbl_fault_title.configure(
                text=f"🚨 FAULT SPOT #{idx+1} OF {total}: {fault['defect_name'].upper()} ({fault['confidence']*100:.1f}%)",
                bg="#C62828"
            )

            # Highlight selected fault button in review bar
            for i, b in enumerate(self.fault_buttons):
                if i == idx:
                    b.configure(bg="#C62828", fg="#FFFFFF", font=("Calibri", 8, "bold"))
                elif i < len(self.detected_faults):
                    b.configure(bg="#2B6CB0", fg="#FFFFFF", font=("Calibri", 8))
                else:
                    b.configure(bg="#E2E8F0", fg="#4A5568", font=("Calibri", 8))

            # Enable/disable prev & next buttons
            self.btn_prev_fault.configure(state=tk.NORMAL if idx > 0 else tk.DISABLED)
            self.btn_next_fault.configure(state=tk.NORMAL if idx < total - 1 else tk.DISABLED)

            # Highlight this spot on the chart
            self._highlight_chart_spot(fault["chainage_km"])
            
            self.log_event("VIEW SPOT", f"Examining Fault Spot {idx+1}/{total}: {fault['defect_name']} @ Km {fault['chainage_km']:.3f}", "DEFECT")

    def prev_fault_spot(self):
        if self.selected_fault_idx > 0:
            self.select_fault_spot(self.selected_fault_idx - 1)

    def next_fault_spot(self):
        if self.selected_fault_idx < len(self.detected_faults) - 1:
            self.select_fault_spot(self.selected_fault_idx + 1)

    def _update_fault_buttons_state(self):
        detected_ids = [f["defect_id"] for f in self.detected_faults]
        for i, btn in enumerate(self.fault_buttons):
            d_id = i + 1
            if d_id in detected_ids:
                if i == self.selected_fault_idx:
                    btn.configure(bg="#C62828", fg="#FFFFFF", font=("Calibri", 8, "bold"))
                else:
                    btn.configure(bg="#2B6CB0", fg="#FFFFFF", font=("Calibri", 8))
            else:
                btn.configure(bg="#E2E8F0", fg="#4A5568", font=("Calibri", 8))
        
        has_faults = len(self.detected_faults) > 0
        self.btn_prev_fault.configure(state=tk.NORMAL if has_faults and self.selected_fault_idx > 0 else tk.DISABLED)
        self.btn_next_fault.configure(state=tk.NORMAL if has_faults and self.selected_fault_idx < len(self.detected_faults) - 1 else tk.DISABLED)

    def _reset_fault_buttons_state(self):
        for btn in self.fault_buttons:
            btn.configure(bg="#E2E8F0", fg="#4A5568", font=("Calibri", 8))
        self.btn_prev_fault.configure(state=tk.DISABLED)
        self.btn_next_fault.configure(state=tk.DISABLED)

    def _highlight_chart_spot(self, km):
        """Highlights the selected fault spot on the gauge profile chart."""
        if hasattr(self, '_selected_spot_line') and self._selected_spot_line:
            try:
                self._selected_spot_line.remove()
            except Exception:
                pass
        self._selected_spot_line = self.ax.axvline(km, color="#D69E2E", linestyle="-", linewidth=2.0, alpha=0.9, zorder=6)
        self.canvas.draw_idle()

    def _plot_fault_markers_on_chart(self):
        """Draws vertical defect markers and annotations across the track gauge graph."""
        self.line_gauge.set_data(self.x_data, self.gauge_data)
        
        for i, fault in enumerate(self.detected_faults):
            km = fault["chainage_km"]
            short_name = fault["defect_name"].split()[0]
            self.ax.axvline(km, color="#C62828", linestyle=":", linewidth=1.2, alpha=0.85)
            self.ax.scatter([km], [1682.0], color="#C62828", marker="v", s=45, zorder=5)
            self.ax.text(km, 1683.0, f"Spot {i+1}\n({short_name})", fontsize=6.5, color="#7B1414", ha="center", fontweight="bold")
            
        self.ax.axvspan(0.840, 0.880, color="#FED7D7", alpha=0.35)
        self.ax.text(0.860, 1686.0, "Gauge Widening\n(+9mm)", fontsize=6.5, color="#C62828", ha="center", fontweight="bold")
        self.canvas.draw_idle()

    def open_fault_gallery(self):
        """Opens a modal audit dialog displaying all 4 detected fault spots in a comprehensive side-by-side view."""
        self._ensure_all_faults_populated()
        
        gal_win = tk.Toplevel(self.root)
        gal_win.title("TR-09 ITMS • Visual Fault Spots Audit Gallery (1.500 km Track Siding)")
        gal_win.geometry("1140x780")
        gal_win.minsize(1000, 680)
        gal_win.configure(bg="#F0F4F8")
        
        # Header Frame
        hdr = tk.Frame(gal_win, bg="#1B365D", padx=16, pady=10)
        hdr.pack(fill=tk.X)
        
        tk.Label(
            hdr, text="TR-09 ITMS: COMPREHENSIVE FAULT SPOTS AUDIT GALLERY",
            font=("Calibri", 14, "bold"), fg="#FFFFFF", bg="#1B365D"
        ).pack(anchor="w")
        
        tk.Label(
            hdr, text="Review of all visual track defect targeting reticles, AI feature activations, and structural derailment hazard analyses.",
            font=("Calibri", 9), fg="#CBD5E0", bg="#1B365D"
        ).pack(anchor="w")

        # Container for cards
        container = tk.Frame(gal_win, bg="#F0F4F8")
        container.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)
        
        # 2x2 Grid of Cards
        cards_frame = tk.Frame(container, bg="#F0F4F8")
        cards_frame.pack(fill=tk.BOTH, expand=True)
        
        # Keep references to PhotoImages so they don't get garbage-collected
        gal_win._card_images = []
        
        for i, fault in enumerate(self.detected_faults):
            r = i // 2
            c = i % 2
            
            card = tk.Frame(cards_frame, bg="#FFFFFF", relief=tk.RIDGE, bd=2, padx=10, pady=8)
            card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
            cards_frame.grid_rowconfigure(r, weight=1)
            cards_frame.grid_columnconfigure(c, weight=1)
            
            # Card Title Header
            c_hdr = tk.Frame(card, bg="#C62828" if fault["detected"] else "#2E7D32", padx=6, pady=3)
            c_hdr.pack(fill=tk.X, pady=(0, 6))
            
            tk.Label(
                c_hdr,
                text=f"SPOT #{i+1}: {fault['defect_name'].upper()}",
                font=("Calibri", 10, "bold"), fg="#FFFFFF",
                bg="#C62828" if fault["detected"] else "#2E7D32"
            ).pack(side=tk.LEFT)
            
            tk.Label(
                c_hdr,
                text=f"Km {fault['chainage_km']:.3f} | AI: {fault['confidence']*100:.1f}%",
                font=("Calibri", 9, "bold"), fg="#FFFFFF",
                bg="#C62828" if fault["detected"] else "#2E7D32"
            ).pack(side=tk.RIGHT)
            
            # Image & Info Split
            body = tk.Frame(card, bg="#FFFFFF")
            body.pack(fill=tk.BOTH, expand=True)
            
            # Thumbnail Image
            img_path = fault.get("frame_path")
            if img_path and os.path.exists(img_path):
                try:
                    im = Image.open(img_path).resize((220, 140), Image.Resampling.LANCZOS)
                    p_img = ImageTk.PhotoImage(im)
                    gal_win._card_images.append(p_img)
                    img_lbl = tk.Label(body, image=p_img, bg="#1A202C")
                    img_lbl.pack(side=tk.LEFT, padx=(0, 8), anchor="n")
                except Exception:
                    pass
            
            # Text details
            info_frame = tk.Frame(body, bg="#FFFFFF")
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Spot Location
            bbox = fault.get("bounding_box")
            tk.Label(info_frame, text=f"📍 Reticle Bounding Box: {bbox}", font=("Calibri", 8, "bold"), fg="#1B365D", bg="#FFFFFF").pack(anchor="w")
            
            # How Detected
            tk.Label(info_frame, text="🔍 How Detected:", font=("Calibri", 8, "bold"), fg="#2B6CB0", bg="#FFFFFF").pack(anchor="w", pady=(2, 0))
            tk.Label(info_frame, text=fault.get("detection_method", "N/A"), font=("Calibri", 8), fg="#4A5568", bg="#FFFFFF", justify=tk.LEFT, wraplength=260).pack(anchor="w")
            
            # Damage
            tk.Label(info_frame, text="⚠️ Track Damage:", font=("Calibri", 8, "bold"), fg="#C62828", bg="#FFFFFF").pack(anchor="w", pady=(2, 0))
            tk.Label(info_frame, text=fault.get("damage_description", "N/A"), font=("Calibri", 8), fg="#4A5568", bg="#FFFFFF", justify=tk.LEFT, wraplength=260).pack(anchor="w")

            # Hazard & Action
            tk.Label(info_frame, text="🚨 Action:", font=("Calibri", 8, "bold"), fg="#D69E2E", bg="#FFFFFF").pack(anchor="w", pady=(2, 0))
            tk.Label(info_frame, text=fault.get("pway_action", "N/A"), font=("Calibri", 8), fg="#4A5568", bg="#FFFFFF", justify=tk.LEFT, wraplength=260).pack(anchor="w")

            # Button to view in main window
            def make_select_cmd(idx=i, win=gal_win):
                def cmd():
                    self.select_fault_spot(idx)
                    win.destroy()
                return cmd
                
            btn_load = tk.Button(
                card, text="🎯 Load this Fault in Main Inspector", font=("Calibri", 8, "bold"),
                bg="#2B6CB0", fg="#FFFFFF", relief=tk.FLAT, pady=2,
                command=make_select_cmd(i, gal_win)
            )
            btn_load.pack(fill=tk.X, pady=(4, 0))

    def open_csv_log(self):
        csv_file = config.LOCAL_LOG_FILE
        if os.path.exists(csv_file):
            try:
                os.startfile(csv_file)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")
        else:
            messagebox.showwarning("File Not Found", "Please run inspection first.")

    def open_word_report(self):
        doc_file = os.path.join(config.BASE_DIR, "TR-09_ITMS_Project_Report.docx")
        if not os.path.exists(doc_file):
            doc_file = os.path.join(config.BASE_DIR, "MIni Project Report.docx")
        if os.path.exists(doc_file):
            try:
                os.startfile(doc_file)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")
        else:
            messagebox.showwarning("File Not Found", "Project report docx not found.")


def main():
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    root = tk.Tk()
    app = TrackMonitoringApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
