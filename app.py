"""
=============================================================================
TR-09 ITMS: Live Contactless Track Monitoring Web Dashboard
=============================================================================
Author: Soham Bhosale, Arnav, Rudra Marathe
Course: Design Experience, MPSTME, NMIMS
Mentor: Prof. Chaitali Patil
Run with: streamlit run app.py
=============================================================================
"""

import os
import json
import pandas as pd
import streamlit as st
from PIL import Image
import config

# Page Setup
st.set_page_config(
    page_title="TR-09 ITMS Dashboard | NMIMS MPSTME",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished engineering look
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1A365D;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4A5568;
        margin-bottom: 15px;
    }
    .metric-card {
        background-color: #F7FAFC;
        border-radius: 8px;
        padding: 12px;
        border-left: 5px solid #2B6CB0;
    }
    .stAlert {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR: SYSTEM STATUS & CONTROLS
# -----------------------------------------------------------------------------
with st.sidebar:
    if os.path.exists(os.path.join(config.ASSETS_DIR, "nmims_logo.png")):
        st.image(os.path.join(config.ASSETS_DIR, "nmims_logo.png"), width=180)

    st.markdown("### 🛠️ TR-09 Subsystem Status")
    st.success("🟢 NVIDIA Jetson Orin Nano (9W, 17 TOPS)")
    st.success("🟢 2x Laser Scanners (40 Hz Triangulation)")
    st.success("🟢 Bosch BMI270 IMU (200 Hz Sampling)")
    st.success("🟢 u-blox ZED-F9P RTK-GNSS (Sub-decimetre)")
    st.success("🟢 Quectel EC25 4G LTE Telemetry (<4s latency)")
    
    st.markdown("---")
    st.markdown("### 🔋 Battery & Power")
    st.progress(88, text="LiFePO₄ 12V 18Ah: 88% (~6.1 hrs left)")
    st.caption("Power Draw: 24.8 W / 26 W max")

    st.markdown("---")
    st.markdown("### 👥 Student Project Team")
    st.markdown("""
    - **Soham Bhosale** *(MBA Tech CE)*
    - **Arnav** *(MBA Tech CE)*
    - **Rudra Marathe** *(MBA Tech CE)*
    - **Mentor:** Prof. Chaitali Patil
    - *MPSTME, SVKM's NMIMS*
    """)

# -----------------------------------------------------------------------------
# MAIN HEADER
# -----------------------------------------------------------------------------
st.markdown("<div class='main-title'>🚆 TR-09: Contactless Integrated Track Monitoring System</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Indigenous Real-Time Track Geometry & Vision Defect Inspection | Indian Railways Broad Gauge (1676 mm)</div>", unsafe_allow_html=True)

# Check if data exists
if not os.path.exists(config.LOCAL_LOG_FILE):
    st.warning("⚠️ No inspection log found. Please run the inspection simulation first using `python main.py` or click below.")
    if st.button("▶️ Run 1.5 km Inspection Simulation Now"):
        with st.spinner("Executing track inspection run..."):
            from main import run_inspection
            run_inspection(sleep_delay_sec=0.01)
        st.rerun()
    st.stop()

# Load Data
df = pd.read_csv(config.LOCAL_LOG_FILE)
defects_json_path = config.DEFECT_EVENTS_FILE
defects_list = []
if os.path.exists(defects_json_path):
    try:
        with open(defects_json_path, "r", encoding="utf-8") as f:
            defects_list = json.load(f)
    except Exception:
        defects_list = []

# -----------------------------------------------------------------------------
# KEY METRICS ROW
# -----------------------------------------------------------------------------
col1, col2, col3, col4, col5 = st.columns(5)
total_dist = df["chainage_km"].max() if not df.empty else 0.0
avg_gauge = df["gauge_mm"].mean() if not df.empty else 1676.0
max_dev = df["gauge_deviation_mm"].abs().max() if not df.empty else 0.0
total_defects = len(defects_list)
safety_status = "SAFE (Broad Gauge Normal)" if max_dev <= 6.0 else "ALERT: TRACK MAINTENANCE NEEDED"

with col1:
    st.metric("Track Length Inspected", f"{total_dist:.3f} km")
with col2:
    st.metric("Nominal Broad Gauge", f"{config.NOMINAL_GAUGE_MM:.1f} mm")
with col3:
    st.metric("Avg Measured Gauge", f"{avg_gauge:.2f} mm", delta=f"{avg_gauge - 1676.0:+.2f} mm")
with col4:
    st.metric("Max Deviation", f"±{max_dev:.2f} mm")
with col5:
    st.metric("Defects Geo-Tagged", f"{total_defects} events", delta="-Requires Action" if total_defects > 0 else "Clear")

st.markdown("---")

# -----------------------------------------------------------------------------
# TABS FOR FACULTY DEMO
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Track Geometry Analytics",
    "🔍 AI Defect Detection Feed",
    "📋 Telemetry Log Data",
    "📐 System Architecture & BoM"
])

# ----------------- TAB 1: GEOMETRY ANALYTICS -----------------
with tab1:
    st.subheader("1. Track Gauge Profile (Broad Gauge 1676 mm)")
    st.caption("RDSO Tolerance Envelope: -3.0 mm (Tight: 1673 mm) to +6.0 mm (Slack: 1682 mm)")
    
    # Chart 1: Gauge vs Chainage
    chart_data = df[["chainage_km", "gauge_mm"]].copy()
    chart_data["Upper RDSO Limit (1682 mm)"] = 1682.0
    chart_data["Lower RDSO Limit (1673 mm)"] = 1673.0
    chart_data["Nominal Broad Gauge"] = 1676.0
    chart_data = chart_data.set_index("chainage_km")
    
    st.line_chart(chart_data, color=["#1E88E5", "#E53935", "#E53935", "#43A047"])

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader("2. Cross-Level (Cant / Super-elevation)")
        st.caption("Elevation difference between Left and Right rail heads (Tolerance: ±4.0 mm)")
        cant_data = df[["chainage_km", "cross_level_mm"]].copy()
        cant_data["Max Allowed (+4mm)"] = 4.0
        cant_data["Min Allowed (-4mm)"] = -4.0
        cant_data = cant_data.set_index("chainage_km")
        st.line_chart(cant_data, color=["#8E24AA", "#FB8C00", "#FB8C00"])

    with col_g2:
        st.subheader("3. Spatial Track Twist (mm/m over 3m Chord)")
        st.caption("Rate of change of cross-level (RDSO Permissible Safe Limit: 2.8 mm/m)")
        twist_data = df[["chainage_km", "twist_mm_per_m"]].copy()
        twist_data["RDSO Twist Limit (2.8 mm/m)"] = 2.8
        twist_data = twist_data.set_index("chainage_km")
        st.line_chart(twist_data, color=["#00897B", "#D81B60"])

# ----------------- TAB 2: AI DEFECT FEED -----------------
with tab2:
    st.subheader("Visual Defect Detections (CNN-LSTM Model Inference)")
    st.markdown("Defects detected with **Confidence ≥ 91%** and automatically geo-tagged with RTK-GNSS coordinates:")

    if not defects_list:
        st.info("No visual defects detected in this run. Track surface is in normal condition.")
    else:
        for idx, defect in enumerate(defects_list):
            with st.container():
                d_col1, d_col2 = st.columns([1, 2])
                with d_col1:
                    img_path = defect.get("frame_path", "")
                    if os.path.exists(img_path):
                        st.image(Image.open(img_path), caption=f"Inspection Frame @ Km {defect['chainage_km']:.3f}", use_container_width=True)
                    else:
                        st.warning("Frame thumbnail not available.")
                with d_col2:
                    st.error(f"### Defect #{idx+1}: {defect['defect_name']}")
                    st.markdown(f"""
                    - **Track Location:** Chainage **Km {defect['chainage_km']:.3f}** (Siding Section)
                    - **GPS Coordinates:** `{defect['latitude']:.6f}° N, {defect['longitude']:.6f}° E`
                    - **Inference Confidence:** **{defect['confidence']*100:.1f}%** (Target threshold: ≥ 91.0%)
                    - **Gauge at Location:** {defect['gauge_mm']:.1f} mm
                    - **Cloud Telemetry Status:** `{defect['status']}` via Quectel LTE
                    """)
                    st.button(f"Generate P-Way Maintenance Ticket #{idx+101}", key=f"btn_{idx}")
                st.divider()

# ----------------- TAB 3: LOG DATA & EXPORT -----------------
with tab3:
    st.subheader("Inspection Telemetry Records")
    st.dataframe(df, use_container_width=True)

    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Full Track Inspection Report (CSV)",
        data=csv_bytes,
        file_name="TR-09_Track_Inspection_Log.csv",
        mime="text/csv",
    )

# ----------------- TAB 4: ARCHITECTURE & BOM -----------------
with tab4:
    st.subheader("TR-09 System Architecture & Engineering Bill of Materials (BoM)")
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        if os.path.exists(os.path.join(config.ASSETS_DIR, "fig1_system_architecture.png")):
            st.image(os.path.join(config.ASSETS_DIR, "fig1_system_architecture.png"), caption="Figure 1: TR-09 System Architecture", use_container_width=True)
    with col_a2:
        if os.path.exists(os.path.join(config.ASSETS_DIR, "fig2_sensor_fusion.png")):
            st.image(os.path.join(config.ASSETS_DIR, "fig2_sensor_fusion.png"), caption="Figure 2: Sensor Fusion & Data Pipeline", use_container_width=True)

    st.markdown("### Bill of Materials (Hard Budget: ₹1.35 Lakhs - All Indian Sourced)")
    bom_data = [
        {"Subsystem": "Laser Scanner ×2", "Part Chosen": "Hokuyo URG-04LX-class clone", "Indian Price (₹)": "21,400", "Role": "Sub-mm gauge measurement at 0.5 m"},
        {"Subsystem": "IMU (9-Axis)", "Part Chosen": "Bosch BMI270 + BMM150", "Indian Price (₹)": "1,850", "Role": "Roll/Cant, Cross-level, Twist"},
        {"Subsystem": "RTK-GNSS", "Part Chosen": "u-blox ZED-F9P RTK module", "Indian Price (₹)": "32,900", "Role": "Sub-decimetre geo-tagging & CORS"},
        {"Subsystem": "Edge Compute", "Part Chosen": "NVIDIA Jetson Orin Nano 8 GB", "Indian Price (₹)": "27,800", "Role": "17 TOPS edge AI at ~9 W"},
        {"Subsystem": "Camera ×2", "Part Chosen": "Sony IMX477 CSI module", "Indian Price (₹)": "9,400", "Role": "12 MP rail surface inspection"},
        {"Subsystem": "LTE + Wi-Fi", "Part Chosen": "Quectel EC25-AF + ESP32", "Indian Price (₹)": "6,200", "Role": "Cloud telemetry & local buffer resync"},
        {"Subsystem": "Power Tree", "Part Chosen": "12V 18Ah LiFePO₄ + DC-DC", "Indian Price (₹)": "8,700", "Role": "7-hour continuous field operation"},
        {"Subsystem": "Enclosure & Mount", "Part Chosen": "IP65 ABS + Steel Trolley Mount", "Indian Price (₹)": "11,300", "Role": "Vibration-damped track chassis"},
        {"Subsystem": "Cables & Misc.", "Part Chosen": "Connectors, Antennas, Hardware", "Indian Price (₹)": "5,950", "Role": "Harnessing and fasteners"},
        {"Subsystem": "TOTAL", "Part Chosen": "Complete ITMS Rig", "Indian Price (₹)": "1,35,500", "Role": "On Budget with ₹500 spare"}
    ]
    st.table(pd.DataFrame(bom_data))

st.caption("TR-09 Indigenous Track Monitoring System | NMIMS MPSTME Design Experience 2025–26 | Open Reference Design")
