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

# Custom Styling: Forest Green Palette & High-Contrast Typography
st.markdown("""
<style>
    /* Global Page Background */
    .stApp {
        background-color: #ebf2ea;
    }
    
    /* Top Header Banner */
    .nav-container {
        background: linear-gradient(135deg, #1e4620 0%, #2d5a27 100%);
        padding: 22px 30px;
        border-radius: 16px;
        color: #ffffff;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(30, 70, 32, 0.15);
    }
    .nav-title {
        font-size: 26px;
        font-weight: 800;
        margin: 0;
        color: #ffffff !important;
        letter-spacing: 0.5px;
    }
    .nav-subtitle {
        font-size: 13.5px;
        margin-top: 4px;
        color: #cce3ca !important;
    }

    /* Menu Card Box Container */
    .card-box {
        background-color: #ffffff;
        border: 1.5px solid #d0e1ce;
        border-radius: 18px;
        padding: 24px 20px 18px 20px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        margin-bottom: 0px;
    }
    .card-title {
        font-size: 19px;
        font-weight: 700;
        color: #1e4620;
        margin-bottom: 10px;
    }
    .card-desc {
        font-size: 13.5px;
        color: #1b4332;
        line-height: 1.4;
        margin-bottom: 15px;
        min-height: 42px;
        font-weight: 500;
    }

    /* Customizing Navigation & Card Action Buttons (Ensuring Pure White Text) */
    div.stButton > button[kind="primary"] {
        background-color: #265329 !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        border-radius: 10px !important;
        height: 44px !important;
        box-shadow: 0 2px 6px rgba(38, 83, 41, 0.2) !important;
    }
    /* Force white text on primary buttons in all states */
    div.stButton > button[kind="primary"] * {
        color: #ffffff !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #1a3c1c !important;
    }
    
    div.stButton > button[kind="secondary"] {
        background-color: #ffffff !important;
        border: 1.5px solid #265329 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        border-radius: 10px !important;
        height: 44px !important;
    }
    div.stButton > button[kind="secondary"] * {
        color: #265329 !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #e2ede0 !important;
    }

    /* Heading Text Overrides for Non-White Typography */
    h1, h2, h3, h4, h5, label {
        color: #1e4620 !important;
    }
</style>
""", unsafe_allow_html=True)

# Ensure mock data exists
if not os.path.exists("data/sensor_readings.csv"):
    from generate_mock_data import generate_sensor_data
    generate_sensor_data()

# Session state initialization
if "current_tab" not in st.session_state:
    st.session_state["current_tab"] = "🏠 Home Menu"

# Header Banner
st.markdown("""
<div class="nav-container">
    <p class="nav-title">🌲 TIMBER AI: Forest Restoration DSS</p>
    <p class="nav-subtitle">Technology-Integrated Monitoring and Biodiversity Enhancement for Reforestation</p>
</div>
""", unsafe_allow_html=True)

# Top Bar Quick Navigation
nav_col0, nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([1.2, 1, 1, 1, 1])

with nav_col0:
    if st.button("🏠 Home Menu", type="primary" if st.session_state["current_tab"] == "🏠 Home Menu" else "secondary", use_container_width=True):
        st.session_state["current_tab"] = "🏠 Home Menu"
        st.rerun()
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

sensor_df = pd.read_csv("data/sensor_readings.csv")

# ---------------------------------------------------------
# MENU SCREEN (Home Page)
# ---------------------------------------------------------
if st.session_state["current_tab"] == "🏠 Home Menu":
    st.markdown("<h2 style='text-align: center; color: #1e4620; font-weight: 700;'>Select a System Module to Begin</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #2d5a27; font-size: 14.5px; font-weight: 500; margin-bottom: 30px;'>Choose one of the AI decision support components below to analyze reforestation data.</p>", unsafe_allow_html=True)

    # Upper Cards Row
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.markdown("""
        <div class="card-box">
            <div class="card-title">🗺️ Geospatial Priority Mapping</div>
            <div class="card-desc">Interactive GIS heatmap displaying forest restoration zones and priority levels across target sectors.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Geospatial Map", key="btn_map", type="primary", use_container_width=True):
            st.session_state["current_tab"] = "🗺️ Geospatial Map"
            st.rerun()

    with row1_col2:
        st.markdown("""
        <div class="card-box">
            <div class="card-title">🚁 Drone Image Canopy Analysis</div>
            <div class="card-desc">OpenCV green-space segmentation to process aerial drone images and compute vegetation cover percentage.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Drone Vision", key="btn_drone", type="primary", use_container_width=True):
            st.session_state["current_tab"] = "🚁 Drone Vision"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Lower Cards Row
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.markdown("""
        <div class="card-box">
            <div class="card-title">📊 Predictive Soil Telemetry</div>
            <div class="card-desc">Scikit-Learn Random Forest model forecasting future soil moisture trends under ambient temperatures.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Soil Telemetry", key="btn_soil", type="primary", use_container_width=True):
            st.session_state["current_tab"] = "📊 Soil Telemetry"
            st.rerun()

    with row2_col2:
        st.markdown("""
        <div class="card-box">
            <div class="card-title">🎯 Priority Index & Action Engine</div>
            <div class="card-desc">Multi-variable decision support engine formulating targeted irrigation and replanting strategies.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open Priority Engine", key="btn_engine", type="primary", use_container_width=True):
            st.session_state["current_tab"] = "🎯 Priority Engine"
            st.rerun()

# ---------------------------------------------------------
# MODULE CONTENT VIEWS
# ---------------------------------------------------------
elif st.session_state["current_tab"] == "🗺️ Geospatial Map":
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