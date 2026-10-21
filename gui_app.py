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
        self.root.title("TR-09 ITMS: Contactless Integrated Track Monitoring System | NMIMS MPSTME")
        self.root.geometry("1240x820")
        self.root.minsize(1080, 720)
        self.root.configure(bg="#F0F4F8")

        # Runtime State
        self.is_running = False
        self.is_paused = False
        self.sim_thread = None
        self.step_delay = 0.08  # Default animation speed
        
        # Data History for Real-Time Graph
        self.x_data = []
        self.gauge_data = []
        self.cross_level_data = []

        # Defect Counts
        self.defect_counts = {1: 0, 2: 0, 3: 0, 4: 0}

        # Initialize Subsystems
        self.laser = LaserScanner()
        self.imu = IMUSensor()
        self.gnss = GNSSReceiver()
        self.camera = CameraStream()
        self.fusion = GeometryFusionEngine()
        self.detector = RailDefectDetector()
        self.telemetry = TelemetryEngine()

        self._build_ui()
        self.log_event("SYSTEM INITIALIZED", "NVIDIA Jetson Orin Nano edge firmware ready. Click 'Start Inspection' to begin.", "INFO")

    def _build_ui(self):
        # -------------------------------------------------------------
        # 1. HEADER BAR
        # -------------------------------------------------------------
        header_frame = tk.Frame(self.root, bg="#1B365D", height=70)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_lbl = tk.Label(
            header_frame,
            text="TR-09: INDIGENOUS CONTACTLESS INTEGRATED TRACK MONITORING SYSTEM",
            font=("Calibri", 16, "bold"),
            fg="#FFFFFF",
            bg="#1B365D"
        )
        title_lbl.pack(anchor="w", padx=20, pady=(8, 0))

        sub_lbl = tk.Label(
            header_frame,
            text="SVKM's NMIMS MPSTME (Shirpur) • Design Experience Course Project | Team: Soham Bhosale, Arnav, Rudra Marathe (Mentor: Prof. Chaitali Patil)",
            font=("Calibri", 10),
            fg="#CBD5E0",
            bg="#1B365D"
        )
        sub_lbl.pack(anchor="w", padx=20, pady=(0, 8))

        # -------------------------------------------------------------
        # 2. MAIN CONTAINER (LEFT: Controls & Stats, RIGHT: Visuals & Graph)
        # -------------------------------------------------------------
        main_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg="#E2E8F0", bd=0, sashwidth=4)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        # LEFT PANE (Controls & Real-Time Readouts)
        left_frame = tk.Frame(main_paned, bg="#FFFFFF", padx=12, pady=10)
        main_paned.add(left_frame, minsize=420, width=450)

        # RIGHT PANE (Camera Feed & Geometry Graph)
        right_frame = tk.Frame(main_paned, bg="#FFFFFF", padx=12, pady=10)
        main_paned.add(right_frame, minsize=620)

        self._build_left_pane(left_frame)
        self._build_right_pane(right_frame)

        # -------------------------------------------------------------
        # 3. BOTTOM EVENT LOG & STATUS BAR
        # -------------------------------------------------------------
        bottom_frame = tk.Frame(self.root, bg="#EDF2F7", height=150)
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=(0, 8))
        self._build_bottom_pane(bottom_frame)

    def _build_left_pane(self, parent):
        # CONTROL BUTTONS
        ctrl_box = tk.LabelFrame(parent, text=" 🕹️ Inspection Controls ", font=("Calibri", 11, "bold"), bg="#FFFFFF", fg="#1B365D", padx=8, pady=8)
        ctrl_box.pack(fill=tk.X, pady=(0, 10))

        btn_row = tk.Frame(ctrl_box, bg="#FFFFFF")
        btn_row.pack(fill=tk.X)

        self.btn_start = tk.Button(
            btn_row, text="▶ Start Run", font=("Calibri", 10, "bold"), bg="#2E7D32", fg="#FFFFFF",
            activebackground="#1B5E20", activeforeground="#FFFFFF", width=11, relief=tk.FLAT, command=self.start_inspection
        )
        self.btn_start.pack(side=tk.LEFT, padx=3)

        self.btn_pause = tk.Button(
            btn_row, text="⏸ Pause", font=("Calibri", 10, "bold"), bg="#F57C00", fg="#FFFFFF",
            activebackground="#E65100", activeforeground="#FFFFFF", width=9, relief=tk.FLAT, state=tk.DISABLED, command=self.pause_inspection
        )
        self.btn_pause.pack(side=tk.LEFT, padx=3)

        self.btn_reset = tk.Button(
            btn_row, text="🔄 Reset", font=("Calibri", 10, "bold"), bg="#546E7A", fg="#FFFFFF",
            activebackground="#37474F", activeforeground="#FFFFFF", width=9, relief=tk.FLAT, command=self.reset_inspection
        )
        self.btn_reset.pack(side=tk.LEFT, padx=3)

        # Speed Dropdown
        tk.Label(btn_row, text="Speed:", font=("Calibri", 9), bg="#FFFFFF").pack(side=tk.LEFT, padx=(8, 2))
        self.speed_var = tk.StringVar(value="Normal (1x)")
        speed_menu = ttk.Combobox(btn_row, textvariable=self.speed_var, values=["Normal (1x)", "Fast (3x)", "Ultra (8x)"], width=10, state="readonly")
        speed_menu.pack(side=tk.LEFT)
        speed_menu.bind("<<ComboboxSelected>>", self._change_speed)

        # TRACK DISTANCE & PROGRESS
        dist_box = tk.LabelFrame(parent, text=" 📍 Track Position & Chainage ", font=("Calibri", 11, "bold"), bg="#FFFFFF", fg="#1B365D", padx=8, pady=8)
        dist_box.pack(fill=tk.X, pady=(0, 10))

        d_row = tk.Frame(dist_box, bg="#FFFFFF")
        d_row.pack(fill=tk.X)
        tk.Label(d_row, text="Chainage:", font=("Calibri", 10), bg="#FFFFFF").pack(side=tk.LEFT)
        self.lbl_chainage = tk.Label(d_row, text="0.000 km / 1.500 km", font=("Calibri", 12, "bold"), fg="#1A365D", bg="#FFFFFF")
        self.lbl_chainage.pack(side=tk.RIGHT)

        self.prog_bar = ttk.Progressbar(dist_box, orient=tk.HORIZONTAL, mode='determinate', maximum=1.5)
        self.prog_bar.pack(fill=tk.X, pady=(6, 2))

        # GEOMETRY TELEMETRY READOUTS
        geo_box = tk.LabelFrame(parent, text=" 📐 Real-Time Track Geometry (Broad Gauge: 1676 mm) ", font=("Calibri", 11, "bold"), bg="#FFFFFF", fg="#1B365D", padx=8, pady=8)
        geo_box.pack(fill=tk.X, pady=(0, 10))

        # Measured Gauge
        g_row = tk.Frame(geo_box, bg="#F7FAFC", padx=6, pady=4, relief=tk.RIDGE, bd=1)
        g_row.pack(fill=tk.X, pady=3)
        tk.Label(g_row, text="Track Gauge:", font=("Calibri", 10, "bold"), bg="#F7FAFC").pack(side=tk.LEFT)
        self.lbl_gauge = tk.Label(g_row, text="1676.0 mm", font=("Calibri", 13, "bold"), fg="#2E7D32", bg="#F7FAFC")
        self.lbl_gauge.pack(side=tk.LEFT, padx=10)
        self.lbl_gauge_dev = tk.Label(g_row, text="(±0.0 mm)", font=("Calibri", 10), fg="#718096", bg="#F7FAFC")
        self.lbl_gauge_dev.pack(side=tk.LEFT)
        self.lbl_gauge_status = tk.Label(g_row, text="NORMAL", font=("Calibri", 8, "bold"), bg="#2E7D32", fg="#FFFFFF", padx=6, pady=2)
        self.lbl_gauge_status.pack(side=tk.RIGHT)

        # Cross-Level (Cant)
        c_row = tk.Frame(geo_box, bg="#F7FAFC", padx=6, pady=4, relief=tk.RIDGE, bd=1)
        c_row.pack(fill=tk.X, pady=3)
        tk.Label(c_row, text="Cross-Level (Cant):", font=("Calibri", 10, "bold"), bg="#F7FAFC").pack(side=tk.LEFT)
        self.lbl_cant = tk.Label(c_row, text="0.0 mm", font=("Calibri", 12, "bold"), fg="#1A365D", bg="#F7FAFC")
        self.lbl_cant.pack(side=tk.LEFT, padx=10)
        self.lbl_cant_status = tk.Label(c_row, text="LEVEL (±4mm max)", font=("Calibri", 8), bg="#EDF2F7", fg="#4A5568", padx=4)
        self.lbl_cant_status.pack(side=tk.RIGHT)

        # Spatial Twist
        t_row = tk.Frame(geo_box, bg="#F7FAFC", padx=6, pady=4, relief=tk.RIDGE, bd=1)
        t_row.pack(fill=tk.X, pady=3)
        tk.Label(t_row, text="Track Twist (3m base):", font=("Calibri", 10, "bold"), bg="#F7FAFC").pack(side=tk.LEFT)
        self.lbl_twist = tk.Label(t_row, text="0.0 mm/m", font=("Calibri", 12, "bold"), fg="#1A365D", bg="#F7FAFC")
        self.lbl_twist.pack(side=tk.LEFT, padx=10)
        self.lbl_twist_status = tk.Label(t_row, text="SAFE (≤2.8 mm/m)", font=("Calibri", 8), bg="#EDF2F7", fg="#4A5568", padx=4)
        self.lbl_twist_status.pack(side=tk.RIGHT)

        # GPS & SUBSYSTEM STATUS
        stat_box = tk.LabelFrame(parent, text=" 🛰️ Subsystems & RTK Navigation ", font=("Calibri", 11, "bold"), bg="#FFFFFF", fg="#1B365D", padx=8, pady=8)
        stat_box.pack(fill=tk.X, pady=(0, 10))

        gps_row = tk.Frame(stat_box, bg="#FFFFFF")
        gps_row.pack(fill=tk.X, pady=2)
        tk.Label(gps_row, text="GPS Fix:", font=("Calibri", 9, "bold"), bg="#FFFFFF").pack(side=tk.LEFT)
        self.lbl_gps_fix = tk.Label(gps_row, text="RTK_FIXED (Sub-decimetre)", font=("Calibri", 9), fg="#2E7D32", bg="#FFFFFF")
        self.lbl_gps_fix.pack(side=tk.LEFT, padx=6)

        coords_row = tk.Frame(stat_box, bg="#FFFFFF")
        coords_row.pack(fill=tk.X, pady=2)
        tk.Label(coords_row, text="Coordinates:", font=("Calibri", 9, "bold"), bg="#FFFFFF").pack(side=tk.LEFT)
        self.lbl_coords = tk.Label(coords_row, text="21.311200° N, 74.881400° E", font=("Calibri", 9), fg="#4A5568", bg="#FFFFFF")
        self.lbl_coords.pack(side=tk.LEFT, padx=6)

        pwr_row = tk.Frame(stat_box, bg="#FFFFFF")
        pwr_row.pack(fill=tk.X, pady=2)
        tk.Label(pwr_row, text="Power Draw:", font=("Calibri", 9, "bold"), bg="#FFFFFF").pack(side=tk.LEFT)
        self.lbl_pwr = tk.Label(pwr_row, text="24.6 W (LiFePO₄ 88% - ~6.2 hrs left)", font=("Calibri", 9), fg="#2E7D32", bg="#FFFFFF")
        self.lbl_pwr.pack(side=tk.LEFT, padx=6)

        # DEFECT COUNTERS
        cnt_box = tk.LabelFrame(parent, text=" 🚩 Detected Defect Summary ", font=("Calibri", 11, "bold"), bg="#FFFFFF", fg="#1B365D", padx=8, pady=8)
        cnt_box.pack(fill=tk.X)

        self.lbl_cnt_fastener = tk.Label(cnt_box, text="• Missing Fasteners: 0", font=("Calibri", 9), bg="#FFFFFF", fg="#C62828")
        self.lbl_cnt_fastener.pack(anchor="w")
        self.lbl_cnt_fishplate = tk.Label(cnt_box, text="• Cracked Fishplates: 0", font=("Calibri", 9), bg="#FFFFFF", fg="#C62828")
        self.lbl_cnt_fishplate.pack(anchor="w")
        self.lbl_cnt_ballast = tk.Label(cnt_box, text="• Ballast Deficiencies: 0", font=("Calibri", 9), bg="#FFFFFF", fg="#EF6C00")
        self.lbl_cnt_ballast.pack(anchor="w")
        self.lbl_cnt_squat = tk.Label(cnt_box, text="• Rail Surface Squats: 0", font=("Calibri", 9), bg="#FFFFFF", fg="#C62828")
        self.lbl_cnt_squat.pack(anchor="w")

    def _build_right_pane(self, parent):
        # 1. LIVE CAMERA INSPECTION FEED
        cam_box = tk.LabelFrame(parent, text=" 📷 Sony IMX477 Rail Surface Camera & AI Inference ", font=("Calibri", 11, "bold"), bg="#FFFFFF", fg="#1B365D", padx=8, pady=6)
        cam_box.pack(fill=tk.X, pady=(0, 8))

        top_cam_frame = tk.Frame(cam_box, bg="#FFFFFF")
        top_cam_frame.pack(fill=tk.X)

        # Image Canvas
        self.cam_canvas = tk.Label(top_cam_frame, bg="#1A202C", width=380, height=210)
        self.cam_canvas.pack(side=tk.LEFT, padx=(0, 10))

        # Load initial normal image
        init_img_path = os.path.join(config.TEST_FRAMES_DIR, "normal_rail.png")
        if os.path.exists(init_img_path):
            self._update_cam_image(init_img_path)

        # Defect Inference Detail Panel
        infer_panel = tk.Frame(top_cam_frame, bg="#F7FAFC", padx=10, pady=8, relief=tk.RIDGE, bd=1)
        infer_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(infer_panel, text="CNN-LSTM Visual Inference", font=("Calibri", 10, "bold"), bg="#F7FAFC", fg="#1B365D").pack(anchor="w")
        
        self.lbl_infer_status = tk.Label(
            infer_panel, text="NORMAL RAIL SURFACE", font=("Calibri", 10, "bold"),
            bg="#2E7D32", fg="#FFFFFF", padx=8, pady=4
        )
        self.lbl_infer_status.pack(fill=tk.X, pady=6)

        self.lbl_infer_conf = tk.Label(infer_panel, text="AI Confidence: 98.4%", font=("Calibri", 10), bg="#F7FAFC", fg="#2D3748")
        self.lbl_infer_conf.pack(anchor="w", pady=2)

        self.lbl_infer_gate = tk.Label(infer_panel, text="Gating Threshold: ≥ 91.0%", font=("Calibri", 9), bg="#F7FAFC", fg="#718096")
        self.lbl_infer_gate.pack(anchor="w", pady=2)

        self.lbl_infer_loc = tk.Label(infer_panel, text="Defect Location: Siding Km 0.000", font=("Calibri", 9), bg="#F7FAFC", fg="#718096")
        self.lbl_infer_loc.pack(anchor="w", pady=2)

        self.lbl_infer_action = tk.Label(infer_panel, text="Action: Real-Time Stream Monitoring", font=("Calibri", 9, "italic"), bg="#F7FAFC", fg="#2B6CB0")
        self.lbl_infer_action.pack(anchor="w", pady=4)

        # 2. REAL-TIME TRACK GAUGE PLOT (EMBEDDED MATPLOTLIB)
        graph_box = tk.LabelFrame(parent, text=" 📊 Real-Time Track Gauge Profile (Tolerance: 1673 - 1682 mm) ", font=("Calibri", 11, "bold"), bg="#FFFFFF", fg="#1B365D", padx=4, pady=4)
        graph_box.pack(fill=tk.BOTH, expand=True)

        self.fig = Figure(figsize=(6.2, 3.2), dpi=100)
        self.fig.patch.set_facecolor('#FFFFFF')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#F8FAFC')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_box)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self._init_chart()

    def _init_chart(self):
        self.ax.clear()
        self.ax.set_title("Broad Gauge vs Track Chainage", fontsize=10, fontweight="bold", color="#1A365D", pad=6)
        self.ax.set_xlabel("Track Distance (km)", fontsize=8, color="#4A5568")
        self.ax.set_ylabel("Measured Gauge (mm)", fontsize=8, color="#4A5568")
        self.ax.set_xlim(0, 1.5)
        self.ax.set_ylim(1666, 1690)
        self.ax.tick_params(labelsize=8)
        self.ax.grid(True, linestyle="--", alpha=0.5)

        # Reference Tolerance Lines
        self.ax.axhline(1676.0, color="#2E7D32", linestyle="-", linewidth=1.2, label="Nominal Broad Gauge (1676 mm)")
        self.ax.axhline(1682.0, color="#C62828", linestyle="--", linewidth=1.0, label="Slack Limit (+6mm)")
        self.ax.axhline(1673.0, color="#C62828", linestyle="--", linewidth=1.0, label="Tight Limit (-3mm)")
        self.ax.legend(loc="upper right", fontsize=7)
        self.line_gauge, = self.ax.plot([], [], color="#1E88E5", linewidth=1.5, label="Measured Gauge")
        self.canvas.draw()

    def _build_bottom_pane(self, parent):
        top_row = tk.Frame(parent, bg="#EDF2F7")
        top_row.pack(fill=tk.X, pady=(2, 2))

        tk.Label(top_row, text=" 📜 Real-Time Inspection Event & Telemetry Log", font=("Calibri", 10, "bold"), bg="#EDF2F7", fg="#1B365D").pack(side=tk.LEFT)

        # Quick action buttons on bottom bar
        btn_view_csv = tk.Button(top_row, text="📊 Open CSV Log", font=("Calibri", 8, "bold"), bg="#4A5568", fg="#FFFFFF", relief=tk.FLAT, padx=6, command=self.open_csv_log)
        btn_view_csv.pack(side=tk.RIGHT, padx=4)

        btn_view_report = tk.Button(top_row, text="📄 Open Word Report (.docx)", font=("Calibri", 8, "bold"), bg="#2B6CB0", fg="#FFFFFF", relief=tk.FLAT, padx=6, command=self.open_word_report)
        btn_view_report.pack(side=tk.RIGHT, padx=4)

        # Scrollable Text Console
        self.log_text = tk.Text(parent, height=5, font=("Consolas", 9), bg="#1A202C", fg="#E2E8F0", wrap=tk.WORD, relief=tk.FLAT)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Tags for colored logging
        self.log_text.tag_config("INFO", foreground="#63B3ED")
        self.log_text.tag_config("NORMAL", foreground="#68D391")
        self.log_text.tag_config("WARNING", foreground="#F6AD55")
        self.log_text.tag_config("CRITICAL", foreground="#FC8181")
        self.log_text.tag_config("DEFECT", foreground="#FEB2B2", font=("Consolas", 9, "bold"))

    def log_event(self, event_type, message, tag="INFO"):
        """Appends a colored log entry to the console."""
        t_str = time.strftime("%H:%M:%S")
        entry = f"[{t_str}] [{event_type:<10}] {message}\n"
        self.log_text.insert(tk.END, entry, tag)
        self.log_text.see(tk.END)

    def _update_cam_image(self, img_path):
        """Loads and updates the camera display widget."""
        try:
            im = Image.open(img_path)
            im = im.resize((380, 210), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(im)
            self.cam_canvas.configure(image=photo)
            self.cam_canvas.image = photo
        except Exception as e:
            pass

    def _change_speed(self, event=None):
        val = self.speed_var.get()
        if "Fast" in val:
            self.step_delay = 0.03
        elif "Ultra" in val:
            self.step_delay = 0.008
        else:
            self.step_delay = 0.08

    # -------------------------------------------------------------
    # SIMULATION CONTROLS & THREADING
    # -------------------------------------------------------------
    def start_inspection(self):
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self.btn_start.configure(state=tk.DISABLED)
            self.btn_pause.configure(state=tk.NORMAL)
            self.sim_thread = threading.Thread(target=self._run_simulation_loop, daemon=True)
            self.sim_thread.start()
            self.log_event("RUN START", "Starting trolley push along 1.5 km siding. Sampling sensors at 5 Hz.", "INFO")
        elif self.is_paused:
            self.is_paused = False
            self.btn_pause.configure(text="⏸ Pause", bg="#F57C00")
            self.log_event("RESUMED", "Trolley inspection resumed.", "INFO")

    def pause_inspection(self):
        if self.is_running and not self.is_paused:
            self.is_paused = True
            self.btn_pause.configure(text="▶ Resume", bg="#2E7D32")
            self.log_event("PAUSED", "Trolley halted. Sensor logging suspended.", "WARNING")
        elif self.is_running and self.is_paused:
            self.start_inspection()

    def reset_inspection(self):
        self.is_running = False
        self.is_paused = False
        self.btn_start.configure(state=tk.NORMAL)
        self.btn_pause.configure(state=tk.DISABLED, text="⏸ Pause", bg="#F57C00")
        
        # Reset Subsystems
        self.gnss = GNSSReceiver()
        self.fusion = GeometryFusionEngine()
        self.telemetry = TelemetryEngine()
        self.defect_counts = {1: 0, 2: 0, 3: 0, 4: 0}
        self.x_data.clear()
        self.gauge_data.clear()
        self.cross_level_data.clear()

        # Reset UI
        self.prog_bar['value'] = 0.0
        self.lbl_chainage.configure(text="0.000 km / 1.500 km")
        self.lbl_gauge.configure(text="1676.0 mm", fg="#2E7D32")
        self.lbl_gauge_dev.configure(text="(±0.0 mm)")
        self.lbl_gauge_status.configure(text="NORMAL", bg="#2E7D32")
        self.lbl_cant.configure(text="0.0 mm")
        self.lbl_twist.configure(text="0.0 mm/m")
        self._update_defect_counters()
        self._init_chart()
        self.log_event("RESET", "Simulation reset to Chainage Km 0.000.", "INFO")

    def _update_defect_counters(self):
        self.lbl_cnt_fastener.configure(text=f"• Missing Fasteners: {self.defect_counts[1]}")
        self.lbl_cnt_fishplate.configure(text=f"• Cracked Fishplates: {self.defect_counts[2]}")
        self.lbl_cnt_ballast.configure(text=f"• Ballast Deficiencies: {self.defect_counts[3]}")
        self.lbl_cnt_squat.configure(text=f"• Rail Surface Squats: {self.defect_counts[4]}")

    def _run_simulation_loop(self):
        total_dist_km = 1.500
        step_m = 25.0
        current_km = 0.0

        while self.is_running and current_km <= total_dist_km:
            if self.is_paused:
                time.sleep(0.1)
                continue

            # Defects injection checks
            inject_gauge_widening = (0.840 <= current_km <= 0.880)
            inject_cant = (0.420 <= current_km <= 0.450)
            simulate_rtk_loss = (1.100 <= current_km <= 1.180)

            # 1. Read Sensors
            dl, dr = self.laser.read_measurements(current_km, inject_gauge_defect=inject_gauge_widening)
            imu_data = self.imu.read_motion(current_km, inject_cant_defect=inject_cant)
            gnss_data = self.gnss.update_position(step_m, force_rtk_loss=simulate_rtk_loss)
            current_km = gnss_data["chainage_km"]

            # 2. Geometry Fusion
            geo = self.fusion.process_sample(dl, dr, imu_data, gnss_data)

            # 3. Vision Inference
            frame_path, sim_class = self.camera.capture_frame(current_km)
            defect = self.detector.analyze_frame(frame_path, sim_class)

            # 4. Telemetry Logging
            self.telemetry.log_record(geo, defect, lte_online=not simulate_rtk_loss)

            # 5. Thread-safe UI update
            self.root.after(0, self._update_ui_state, current_km, geo, defect, gnss_data, frame_path)

            time.sleep(self.step_delay)

        if self.is_running:
            self.root.after(0, self._on_inspection_finished)

    def _update_ui_state(self, current_km, geo, defect, gnss_data, frame_path):
        # Update Chainage
        self.lbl_chainage.configure(text=f"{current_km:.3f} km / 1.500 km")
        self.prog_bar['value'] = current_km

        # Update Gauge
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

        # Update Cross-Level & Twist
        self.lbl_cant.configure(text=f"{geo['cross_level_mm']:+.1f} mm")
        self.lbl_twist.configure(text=f"{geo['twist_mm_per_m']:.1f} mm/m")

        # Update GPS status
        fix_str = gnss_data["fix_status"]
        self.lbl_gps_fix.configure(text=fix_str, fg="#2E7D32" if "FIXED" in fix_str else "#E65100")
        self.lbl_coords.configure(text=f"{gnss_data['latitude']:.6f}° N, {gnss_data['longitude']:.6f}° E")

        # Update Defect Vision Card
        if defect["detected"]:
            d_id = defect["defect_id"]
            if d_id in self.defect_counts:
                self.defect_counts[d_id] += 1
            self._update_defect_counters()

            self._update_cam_image(frame_path)
            self.lbl_infer_status.configure(text=f"ALERT: {defect['defect_name'].upper()}", bg="#C62828")
            self.lbl_infer_conf.configure(text=f"AI Confidence: {defect['confidence']*100:.1f}%")
            self.lbl_infer_loc.configure(text=f"Defect Location: Siding Km {current_km:.3f}")
            self.lbl_infer_action.configure(text="Action: Geo-tagged & Uploaded via LTE", fg="#C62828")
            self.log_event("DEFECT", f"Km {current_km:.3f}: {defect['defect_name']} ({defect['confidence']*100:.1f}% conf)", "DEFECT")
        else:
            if current_km % 0.200 < 0.030:
                self._update_cam_image(frame_path)
                self.lbl_infer_status.configure(text="NORMAL RAIL SURFACE", bg="#2E7D32")
                self.lbl_infer_conf.configure(text=f"AI Confidence: {defect['confidence']*100:.1f}%")
                self.lbl_infer_action.configure(text="Action: Surface Clear (All Fasteners Secure)", fg="#2E7D32")

        # Log Warnings
        if geo["severity"] != "NORMAL" and not defect["detected"]:
            self.log_event("GEOMETRY", f"Km {current_km:.3f}: {geo['status_description']} (Gauge: {g_val:.1f} mm)", geo["severity"])

        # Update Graph Data
        self.x_data.append(current_km)
        self.gauge_data.append(g_val)
        if len(self.x_data) % 2 == 0:  # Update graph every 2 samples for smoothness
            self.line_gauge.set_data(self.x_data, self.gauge_data)
            self.canvas.draw_idle()

    def _on_inspection_finished(self):
        self.is_running = False
        self.btn_start.configure(state=tk.NORMAL)
        self.btn_pause.configure(state=tk.DISABLED)
        total_defects = sum(self.defect_counts.values())
        self.log_event("FINISHED", f"1.5 km inspection complete! {total_defects} defects geo-tagged. Report saved to CSV.", "NORMAL")
        messagebox.showinfo(
            "Inspection Complete",
            f"Trolley run finished along 1.500 km track siding.\n\n"
            f"• Visual Rail Defects Found: {total_defects}\n"
            f"• Output Log: {config.LOCAL_LOG_FILE}\n\n"
            f"You can now click 'Open CSV Log' or 'Open Word Report' below."
        )

    def open_csv_log(self):
        """Opens inspection CSV in Excel or default spreadsheet viewer."""
        csv_file = config.LOCAL_LOG_FILE
        if os.path.exists(csv_file):
            try:
                os.startfile(csv_file)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")
        else:
            messagebox.showwarning("File Not Found", "Please run the inspection first to generate the log.")

    def open_word_report(self):
        """Opens the Word report docx in Microsoft Word."""
        doc_file = os.path.join(config.BASE_DIR, "TR-09_ITMS_Project_Report.docx")
        if os.path.exists(doc_file):
            try:
                os.startfile(doc_file)
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")
        else:
            messagebox.showwarning("File Not Found", "Project report docx not found.")


def main():
    root = tk.Tk()
    # High-DPI scaling on Windows
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    app = TrackMonitoringApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
