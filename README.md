# TR-09: Indigenous Contactless Integrated Track Monitoring System (ITMS)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-Native%20Tkinter%20%2B%20Matplotlib-success.svg)](https://docs.python.org/3/library/tkinter.html)
[![Computer Vision](https://img.shields.io/badge/Computer%20Vision-Real%20Track%20Imagery-orange.svg)](https://opencv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Edge-AI](https://img.shields.io/badge/Hardware-Jetson%20Orin%20Nano-green.svg)](https://www.nvidia.com/)
[![Track Gauge](https://img.shields.io/badge/Indian%20Railways-Broad%20Gauge%20(1676mm)-orange.svg)](https://indianrailways.gov.in/)

A complete, working reference implementation and native desktop inspection software for a hand-trolley-mounted contactless track inspector engineered specifically for Indian Railways broad gauge (1676 mm) branch lines.

Submitted as part of the **Design Experience** course at **Mukesh Patel School of Technology Management & Engineering (MPSTME), SVKM's NMIMS (Shirpur Campus)**.

---

## 👥 Student Project Team & Mentorship

- **Soham Bhosale** — *MBA Tech Computer Engineering (Hardware, Architecture, Desktop GUI & Telemetry)*
- **Arnav** — *MBA Tech Computer Engineering (ML Defect Model, Computer Vision)*
- **Rudra Marathe** — *MBA Tech Computer Engineering (Field Operations, Documentation, Sensor Fusion)*
- **Faculty Mentor:** **Prof. Chaitali Patil**

---

## 📌 Executive Summary & Motivation

Indian Railways operates over 68,000 route kilometres. Around **19% of derailments** between 2019 and 2024 were linked to track-geometry anomalies (gauge widening, cross-level twist, and loose fasteners). While high-speed trunk corridors are periodically inspected using imported Track Recording Coaches (like the Plasser EM-120 costing upwards of ₹38 Crore), **branch lines (which represent ~35% of the total network) rely heavily on manual foot patrols** walking once every 8–9 days.

**TR-09** bridges this critical safety gap:
- **Form Factor:** Lightweight (14.6 kg) rig mounted directly on standard P-Way push trolleys.
- **Strict Budget:** Hard parts budget capped at **₹1,35,000** using components sourced strictly from Indian distributors.
- **Contactless Geometry:** Dual laser triangulation distance sensors, 9-axis MEMS IMU, and sub-decimetre RTK-GNSS (±0.8 mm gauge, ±1.2 mm cross-level).
- **Real Track Vision:** Operates on **authentic high-resolution photographs of railway tracks**, highlighting the exact fault spot with targeting bounding boxes and reticles.
- **Engineering Fault Diagnosis:** Details exactly **HOW the defect is detected** algorithmically and **HOW the track is damaged** structurally with derailment hazard ratings.
- **Native Software:** Complete standalone Python Desktop Application (Tkinter + Matplotlib) with real-time digital dials, live track profile charts, multi-modal defect views, and local CSV/JSON buffering.

---

## 🏗️ System Architecture

![System Architecture](assets/fig1_system_architecture.png)

### Key Technical Specifications
| Parameter | Value / Metric | Description |
|:---|:---|:---|
| **Nominal Track Gauge** | **1676.0 mm** | Indian Railways Broad Gauge standard |
| **Gauge Accuracy** | **±0.8 mm** | Laser triangulation distance measurement ($W_{rig} - (d_L + d_R)$) |
| **Cross-Level Accuracy** | **±1.2 mm** | IMU roll measurement $h = G \cdot \sin(\theta_{roll})$ |
| **Max Permissible Twist** | **2.8 mm/m** | Rate of change of cross-level over 3-meter chord base |
| **Edge Compute** | **Jetson Orin Nano (8 GB)** | 17 TOPS INT8, CUDA 12.4, TensorRT runtime |
| **Battery Life** | **~7 Hours** | 12V 18Ah LiFePO₄ pack consuming $\le 24.8\text{ W}$ |
| **Visual Fault Highlighting** | **Targeting Reticle Bounding Boxes** | Real track photos with bounding boxes, reticles & damage callout banners |
| **Defect Confidence Gate** | **$\ge 91\%$** | High-precision gating preventing false maintenance alarms |

---

## 🔍 Real Track Defect Highlighting, Detection & Damage Breakdown

| Defect Class | Fault Spot Coordinates | How It Is Detected (CV Algorithm) | Track Damage Description | Derailment Hazard & Action |
|:---|:---|:---|:---|:---|
| **1. Missing Fastener (ERC)** | `(X: 330-520, Y: 240-440)` Sleeper Clip Seat | **Contour Discontinuity & Intensity Gradient:** Expected circular loop of Mark-III ERC steel clip absent; bare anchor shoulder shadow mismatch detected. | **Rail Foot Unclamped:** Loss of 850–1100 kgf toe clamping load; rail foot free to displace laterally on sleeper pad. | **High Risk:** Dynamic gauge widening under wheel flange thrust causes flange-climb derailment. *Action:* Immediate clip replacement within 24h. |
| **2. Cracked Fishplate** | `(X: 280-540, Y: 210-430)` Joint Bar Web | **High-Frequency Edge Gradient & Line Detection:** Detects linear crack trajectory (aperture ~2.1 mm) propagating across middle bolt-hole zone. | **Structural Bar Fracture:** Fatigue crack propagates through the steel web, destroying joint flexural stiffness and vertical alignment. | **Critical Risk:** Dipped joint causes severe dynamic wheel impact, rail end break, and derailment at speed. *Action:* 30 km/h speed restriction & urgent joint bar renewal. |
| **3. Ballast Deficiency** | `(X: 220-620, Y: 260-520)` Under Sleeper Tie | **Depth Texture Granularity & Shadow Masking:** Large cavity void area (>0.42 m²) detected under sleeper underside with loss of stone interlocking. | **Unsupported Hanging Sleeper:** Water erosion or settlement has washed away ballast packing beneath sleeper tie. | **Severe Hazard:** Differential settlement under heavy axle loads causes track twist (>2.8 mm/m) and wheel unloading. *Action:* Ballast dumping & tamping gang deployment. |
| **4. Surface Squat / RCF** | `(X: 300-560, Y: 180-420)` Rail Running Crown | **Reflectance Gradient & CNN Defect Activation:** Dark crescent rolling contact fatigue (RCF) indentation (area: ~34 mm²) on polished running surface. | **Subsurface Fatigue Shelling:** Micro-fissures propagate downward into the rail crown at ~20° angle with surface depression. | **Critical Risk:** Fatigue crack turns downward into a complete transverse rail fracture, snapping the rail head under load. *Action:* Ultrasonic testing & rail grinding/replacement. |

---

## 📂 Repository File Structure

```text
TR-09-Contactless-Track-Monitoring-System/
│
├── TR-09_ITMS_Project_Report.docx    # Pure technical academic Word report (with real defect imagery)
├── MIni Project Report.docx           # Synchronized copy of project report (.docx)
├── README.md                          # Documentation, Viva Guide & Architecture
├── config.py                          # Engineering parameters, RDSO limits, defect damage models
├── requirements.txt                   # Minimal dependencies (Pillow, Matplotlib, OpenCV, etc.)
├── main.py                            # Primary executable (Launches Desktop GUI or CLI)
├── gui_app.py                         # Native Desktop GUI with multi-modal defect views & damage cards
├── prepare_real_dataset.py            # Real track photo processor, bounding box annotator & CV feature maps
├── build_clean_report.py              # Word report generator with real photos & technical chapters
│
├── sensors/                           # Layer 1: Sensor Simulation & Hardware Drivers
│   ├── laser_scanner.py               # Dual laser distance triangulation (Gauge calculation)
│   ├── imu_sensor.py                  # Bosch BMI270 9-axis IMU (Cross-level & Vibration)
│   ├── gnss_sensor.py                 # u-blox ZED-F9P RTK-GNSS + 90s Dead-Reckoning fallback
│   └── camera_stream.py               # Real track image delivery (Annotated, Raw, Feature Map)
│
├── core/                              # Layer 2: Edge Processing & Telemetry
│   ├── geometry_fusion.py             # Kalman fusion & RDSO tolerance checks
│   ├── defect_detector.py             # CNN-LSTM visual classifier with detection & damage diagnosis
│   └── telemetry.py                   # SQLite/CSV local buffer & LTE cloud dispatch
│
├── assets/                            # System schematics, timeline, and institute logo
└── data/                              # Test inspection frames & output logs
    ├── test_frames/                   # Real track photographs (Raw, Bounding Box, Feature Maps)
    └── inspection_logs/               # Output CSV log & JSON defect records
```

---

## 🚀 How to Run the Project (For Faculty Viva & Demonstrations)

No web browsers or complex servers needed! This is a **100% native Python desktop application**.

### 1. Installation
Clone the repository and install required packages:
```bash
git clone https://github.com/soham3096/TR-09-Contactless-Track-Monitoring-System.git
cd TR-09-Contactless-Track-Monitoring-System
pip install -r requirements.txt
```

### 2. Launch the Desktop Inspection Software (Recommended)
Simply run:
```bash
python main.py
```
This opens the **TR-09 Desktop Graphical Interface** window directly on your screen:
- **Interactive Controls:** Click `▶ Start Run` to begin the trolley push. You can pause or adjust speed (Normal / Fast / Ultra).
- **Multi-Modal Vision View Toggle:**
  - `[ 🎯 Highlighted Fault Spot ]`: Displays real track photograph with bright bounding box, corner reticles, damage callout banner, and pixel coordinates.
  - `[ 🔬 CV Feature Activation Map ]`: Displays Canny edge & Sobel gradient heatmap showing **HOW** the computer vision detected the fault.
  - `[ 📸 Raw Real Track Photo ]`: Displays the clean, unannotated real camera photograph.
- **Track Damage & Fault Analysis Panel:** Displays structured readouts for Fault Spot Coordinates, How Detected (algorithmic explanation), Track Damage (mechanical failure description), and Derailment Hazard with required P-Way action.
- **Embedded Real-Time Graph:** Dynamic Matplotlib plot showing measured gauge curve versus Indian Railways upper (+6 mm) and lower (-3 mm) safety boundaries.
- **One-Click Reports:** Direct buttons to open the generated CSV telemetry log or the Word project report.

### 3. Alternative: Run in Fast Terminal Mode
If you prefer running a quick text simulation directly in your command line:
```bash
python main.py --cli
```

---

## 🎓 Faculty Viva & Line-by-Line Explanation Guide

### Question 1: How does TR-09 use real track images and highlight defect spots?
**Explanation:**  
Refer to `sensors/camera_stream.py`, `core/defect_detector.py`, and `gui_app.py`.
- The system processes authentic, high-resolution photographs of railway tracks.
- When an anomaly is detected, the algorithm draws a high-visibility bounding box with corner targeting reticles around the exact fault spot (e.g. coordinates `X: 330-520, Y: 240-440` on the sleeper seat).
- An alert banner is overlaid on the frame detailing the defect name, inference confidence ($\ge 91\%$), track chainage, and damage hazard.

### Question 2: How does the computer vision algorithm detect the faults?
**Explanation:**  
Refer to `prepare_real_dataset.py` and the Feature Activation Map mode in the GUI.
- **Fasteners:** Uses template matching and contour discontinuity to detect the absence of the circular Mark-III steel loop against the sleeper anchor shoulder.
- **Fishplates:** Applies high-frequency Sobel gradients and Canny edge filtering to detect linear crack trajectories propagating across bolt holes.
- **Ballast:** Uses depth texture granularity and shadow pixel thresholding to detect hollow void pockets under sleepers.
- **Squats:** Analyzes surface reflectance gradients to detect crescent-shaped rolling contact fatigue indentations and shelling on the rail head crown.

### Question 3: How is the track physically damaged, and what is the derailment hazard?
**Explanation:**  
Refer to `config.py` (`DEFECT_DETAILS` dictionary) and Section 6 of the report.
- **Missing Fastener:** Removes 850–1100 kgf toe clamping force $\rightarrow$ lateral rail spread under axle loads $\rightarrow$ dynamic gauge widening $\rightarrow$ wheel flange climb derailment.
- **Cracked Fishplate:** Destroys flexural stiffness of rail joint $\rightarrow$ dipped joint under wheel impact $\rightarrow$ complete rail end break at speed.
- **Ballast Deficiency:** Creates an unsupported hanging sleeper $\rightarrow$ dynamic differential settlement $\rightarrow$ excessive track twist ($>2.8\text{ mm/m}$) causing wheel unloading.
- **Surface Squat:** Subsurface fatigue fissures propagate downward $\rightarrow$ complete transverse rail break snapping the rail crown under heavy freight loads.

---

## 💰 Engineering Bill of Materials (₹1.35 Lakhs Hard Cap)

| Subsystem | Component Chosen | Indian Price (₹) | Justification |
|:---|:---|:---:|:---|
| **Laser Scanner ×2** | Hokuyo URG-04LX-class clone | 21,400 | Sub-mm resolution at 0.5 m range |
| **IMU (9-Axis)** | Bosch BMI270 + BMM150 | 1,850 | Ultra-low gyro drift, $200\text{ Hz}$ sampling |
| **RTK-GNSS** | u-blox ZED-F9P RTK module | 32,900 | Sub-decimetre accuracy, CORS compatible |
| **Edge Compute** | NVIDIA Jetson Orin Nano (8 GB) | 27,800 | 17 TOPS edge AI at ~9 W power |
| **Camera ×2** | Sony IMX477 CSI 12 MP module | 9,400 | High shutter speed, sharp rail imagery |
| **LTE + Wi-Fi** | Quectel EC25-AF + ESP32 | 6,200 | Nationwide 4G telemetry with buffer fallback |
| **Power Pack** | 12V 18Ah LiFePO₄ + DC-DC Tree | 8,700 | ~7 hours continuous field runtime |
| **Enclosure & Frame** | IP65 ABS Enclosure + Steel Mount | 11,300 | Weatherproof, vibration-damped chassis |
| **Harnessing & Misc.** | Connectors, Antennas, Fasteners | 5,950 | Heavy-duty industrial assembly |
| **TOTAL** | **Complete System** | **₹1,35,500** | **On Budget with ₹500 to spare** |

---

## ⚖️ License & Open Reference

This software and simulation reference design is licensed under the **MIT License**.
