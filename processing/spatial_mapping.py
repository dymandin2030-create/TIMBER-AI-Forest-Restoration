import folium
from recommendations.restoration_engine import calculate_restoration_index

def generate_spatial_map(df):
    center_lat = df["Latitude"].mean()
    center_lon = df["Longitude"].mean()
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=14, tiles="OpenStreetMap")
    
    for _, row in df.iterrows():
        simulated_veg = min(100.0, row["Current_Moisture_Pct"] * 1.2)
        res = calculate_restoration_index(simulated_veg, row["Current_Moisture_Pct"])
        color_map = {"red": "red", "yellow": "orange", "green": "green"}
        
        popup_html = f"""
        <b>Sensor ID:</b> {row['Sensor_ID']}<br>
        <b>Zone:</b> {row['Zone']}<br>
        <b>Moisture:</b> {row['Current_Moisture_Pct']}%<br>
        <b>Restoration Index:</b> {res['index_score']}/100<br>
        <b>Priority:</b> {res['status']}<br>
        <b>Action:</b> {res['action_plan']}
        """
        
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=8,
            popup=folium.Popup(popup_html, max_width=300),
            color=color_map[res["status_color"]],
            fill=True,
            fill_color=color_map[res["status_color"]],
            fill_opacity=0.7
        ).add_to(m)
        
    return m