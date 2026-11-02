import streamlit as st
import pandas as pd
import os
from streamlit_folium import st_folium

from models.moisture_model import predict_future_moisture
from processing.image_processing import analyze_vegetation_coverage
from processing.spatial_mapping import generate_spatial_map
from recommendations.restoration_engine import calculate_restoration_index

# Page Configuration
st.set_page_config(
    page_title="TIMBER AI - Forest Restoration DSS", 
    page_icon="🌲",
    layout="wide"
)

# Initialize navigation session state
if "landing_passed" not in st.session_state:
    st.session_state["landing_passed"] = False

if "current_tab" not in st.session_state:
    st.session_state["current_tab"] = "🗺️ Geospatial Map"

# Custom CSS for Full-Page Forest Background & Clean Content Layout
st.markdown("""
<style>
    /* Full Page Forest Background */
    .stApp {
        background: linear-gradient(rgba(11, 26, 14, 0.70), rgba(11, 26, 14, 0.82)),
                    url('https://images.unsplash.com/photo-1448375240586-882707db888b?q=80&w=1920&auto=format&fit=crop');
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
        background-repeat: no-repeat !important;
    }

    /* Top Pill Badge */
    .badge-pill {
        display: inline-block;
        background: rgba(240, 253, 244, 0.18);
        border: 1px solid rgba(240, 253, 244, 0.35);
        backdrop-filter: blur(10px);
        padding: 8px 22px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
        color: #ffffff !important;
        margin-bottom: 22px;
        letter-spacing: 0.5px;
    }

    /* Hero Text Formatting */
    .hero-main-title {
        font-size: 52px;
        font-weight: 900;
        letter-spacing: 1.5px;
        color: #ffffff !important;
        margin-bottom: 12px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-shadow: 0 4px 14px rgba(0, 0, 0, 0.5);
    }

    .hero-sub-title {
        font-size: 19px;
        font-weight: 700;
        color: #f0fdf4 !important;
        margin-bottom: 16px;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    }
    
    .hero-desc {
        font-size: 15px;
        color: #e2f7e5 !important;
        max-width: 800px;
        margin: 0 auto 35px auto;
        line-height: 1.55;
        font-weight: 400;
        text-shadow: 0 2px 6px rgba(0, 0, 0, 0.5);
    }

    /* Primary CTA Buttons */
    div.stButton > button[kind="primary"] {
        background-color: #2d5a27 !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        letter-spacing: 1px !important;
        border-radius: 25px !important;
        height: 50px !important;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35) !important;
    }
    div.stButton > button[kind="primary"] * {
        color: #ffffff !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #0b1a0e !important;
    }

    /* Secondary Navigation Buttons */
    div.stButton > button[kind="secondary"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 1.5px solid #2d5a27 !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        border-radius: 12px !important;
        height: 46px !important;
    }
    div.stButton > button[kind="secondary"] * {
        color: #0b1a0e !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #f0fdf4 !important;
    }

    /* Inner Page High Contrast Text */
    .stMarkdown, .stSubheader, .stMetric, label, h2, h3 {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Ensure mock data exists
if not os.path.exists("data/sensor_readings.csv"):
    from generate_mock_data import generate_sensor_data
    generate_sensor_data()

sensor_df = pd.read_csv("data/sensor_readings.csv")

# ---------------------------------------------------------
# LANDING SCREEN
# ---------------------------------------------------------
if not st.session_state["landing_passed"]:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center;">
        <div class="badge-pill">🌲 AI-Powered Decision Support</div>
        <div class="hero-main-title">TIMBER AI</div>
        <div class="hero-sub-title">Technology-Integrated Monitoring and Biodiversity Enhancement for Reforestation</div>
        <div class="hero-desc">
            Empowering environmental managers and restoration teams with real-time drone canopy analysis, 
            predictive soil telemetry, and intelligent priority index recommendations to ensure sustainable forest recovery.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Single Centered Explore Now Button
    c_left, c_btn, c_right = st.columns([1.2, 1, 1.2])
    with c_btn:
        if st.button("EXPLORE NOW", key="btn_explore_now", type="primary", use_container_width=True):
            st.session_state["landing_passed"] = True
            st.session_state["current_tab"] = "🗺️ Geospatial Map"
            st.rerun()

# ---------------------------------------------------------
# MAIN SYSTEM DASHBOARD SCREEN
# ---------------------------------------------------------
else:
    # Top Navigation Buttons (Without Header Banner Box)
    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)

    with nav_col1:
        if st.button("🗺️ Geospatial Map", type="primary" if st.session_state["current_tab"] == "🗺️ Geospatial Map" else "secondary", use_container_width=True):
            st.session_state["current_tab"] = "🗺️ Geospatial Map"
            st.rerun()
    with nav_col2:
        if st.button("🚁 Drone Vision", type="primary" if st.session_state["current_tab"] == "🚁 Drone Vision" else "secondary", use_container_width=True):
            st.session_state["current_tab"] = "🚁 Drone Vision"
            st.rerun()
    with nav_col3:
        if st.button("📊 Soil Telemetry", type="primary" if st.session_state["current_tab"] == "📊 Soil Telemetry" else "secondary", use_container_width=True):
            st.session_state["current_tab"] = "📊 Soil Telemetry"
            st.rerun()
    with nav_col4:
        if st.button("🎯 Priority Engine", type="primary" if st.session_state["current_tab"] == "🎯 Priority Engine" else "secondary", use_container_width=True):
            st.session_state["current_tab"] = "🎯 Priority Engine"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Module Views
    if st.session_state["current_tab"] == "🗺️ Geospatial Map":
        st.subheader("🗺️ Geospatial Priority Mapping")
        map_obj = generate_spatial_map(sensor_df)
        st_folium(map_obj, width=1100, height=520)

    elif st.session_state["current_tab"] == "🚁 Drone Vision":
        st.subheader("🚁 Drone Image Canopy Analysis")
        uploaded_file = st.file_uploader("Upload Drone Aerial Image", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            c1, c2 = st.columns(2)
            veg_pct, preview_img = analyze_vegetation_coverage(uploaded_file)
            with c1:
                st.image(uploaded_file, caption="Original Aerial Input", use_container_width=True)
            with c2:
                st.image(preview_img, caption="Vegetation Segmentation Mask", use_container_width=True)
            st.metric("Detected Canopy Cover", f"{veg_pct}%")

    elif st.session_state["current_tab"] == "📊 Soil Telemetry":
        st.subheader("📊 Predictive Soil Telemetry Model")
        c1, c2 = st.columns(2)
        with c1:
            prev_m = st.slider("Current Soil Moisture (%)", 10.0, 90.0, 32.0)
            temp_val = st.slider("Ambient Temperature (°C)", 20.0, 45.0, 31.0)
        
        predicted_m = predict_future_moisture(prev_m, temp_val)
        with c2:
            st.metric("Predicted Next-Cycle Soil Moisture", f"{predicted_m:.2f}%", 
                      delta=f"{predicted_m - prev_m:.2f}%")
            if predicted_m < 25.0:
                st.warning("⚠️ Critical Soil Moisture Stress Detected! Irrigation Recommended.")

    elif st.session_state["current_tab"] == "🎯 Priority Engine":
        st.subheader("🎯 Priority Index & Action Engine")
        c1, c2 = st.columns(2)
        with c1:
            veg_in = st.number_input("Canopy Density (%)", 0.0, 100.0, 35.0)
            moist_in = st.number_input("Soil Moisture (%)", 0.0, 100.0, 22.0)
        
        res = calculate_restoration_index(veg_in, moist_in)
        with c2:
            st.metric("Restoration Priority Index", f"{res['index_score']} / 100")
            if res['status_color'] == 'red':
                st.error(f"Status: {res['status']}")
            else:
                st.success(f"Status: {res['status']}")
            
        st.markdown("---")
        st.write(f"**Recommended Action Plan:** {res['action_plan']}")
        st.write(f"**Irrigation Strategy:** {res['irrigation_plan']}")