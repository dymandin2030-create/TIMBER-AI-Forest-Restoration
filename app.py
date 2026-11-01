import streamlit as st
import pandas as pd
import os
from streamlit_folium import st_folium

from models.moisture_model import predict_future_moisture
from processing.image_processing import analyze_vegetation_coverage
from processing.spatial_mapping import generate_spatial_map
from recommendations.restoration_engine import calculate_restoration_index

st.set_page_config(page_title="TIMBER AI - Forest Restoration DSS", layout="wide")

if not os.path.exists("data/sensor_readings.csv"):
    from generate_mock_data import generate_sensor_data
    generate_sensor_data()

st.title("🌲 TIMBER AI: Forest Restoration Decision Support System")
st.markdown("### Technology-Integrated Monitoring and Biodiversity Enhancement for Reforestation")

st.sidebar.header("System Controls")
selected_tab = st.sidebar.radio("Navigation", [
    "1. Forest Health Map", 
    "2. Drone Vision Processing", 
    "3. Soil Telemetry & ML Forecasting",
    "4. AI Restoration Priority Index"
])

sensor_df = pd.read_csv("data/sensor_readings.csv")

if selected_tab == "1. Forest Health Map":
    st.subheader("Geospatial Priority Zones")
    map_obj = generate_spatial_map(sensor_df)
    st_folium(map_obj, width=1100, height=500)

elif selected_tab == "2. Drone Vision Processing":
    st.subheader("Drone Image Canopy Analysis")
    uploaded_file = st.file_uploader("Upload Drone/Aerial Image", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        veg_pct, preview_img = analyze_vegetation_coverage(uploaded_file)
        with col1:
            st.image(uploaded_file, caption="Original Aerial Image", use_container_width=True)
        with col2:
            st.image(preview_img, caption="Vegetation Segmentation Overlay", use_container_width=True)
        st.metric("Detected Vegetation Cover", f"{veg_pct}%")

elif selected_tab == "3. Soil Telemetry & ML Forecasting":
    st.subheader("Predictive Soil Moisture Model")
    c1, c2 = st.columns(2)
    with c1:
        prev_m = st.slider("Current Soil Moisture (%)", 10.0, 90.0, 32.0)
        temp_val = st.slider("Ambient Temperature (°C)", 20.0, 45.0, 31.0)
    
    predicted_m = predict_future_moisture(prev_m, temp_val)
    with c2:
        st.metric("Predicted Next-Cycle Soil Moisture", f"{predicted_m:.2f}%", 
                  delta=f"{predicted_m - prev_m:.2f}%")
        if predicted_m < 25.0:
            st.warning("⚠️ Critical Moisture Stress Predicted! Prepare Irrigation.")

elif selected_tab == "4. AI Restoration Priority Index":
    st.subheader("AI Decision Support Recommendation Engine")
    col1, col2 = st.columns(2)
    with col1:
        veg_in = st.number_input("Canopy Density (%)", 0.0, 100.0, 35.0)
        moist_in = st.number_input("Soil Moisture (%)", 0.0, 100.0, 22.0)
    
    res = calculate_restoration_index(veg_in, moist_in)
    with col2:
        st.metric("Restoration Priority Index", f"{res['index_score']} / 100")
        if res['status_color'] == 'red':
            st.error(f"Status: {res['status']}")
        else:
            st.success(f"Status: {res['status']}")
        
    st.markdown("---")
    st.write(f"**Action Plan:** {res['action_plan']}")
    st.write(f"**Irrigation Strategy:** {res['irrigation_plan']}")