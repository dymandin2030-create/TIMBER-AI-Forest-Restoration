import pandas as pd
import numpy as np
import os

def generate_sensor_data(filename="data/sensor_readings.csv", num_samples=150):
    np.random.seed(42)
    zones = ["Zone A", "Zone B", "Zone C", "Zone D", "Zone E"]
    base_lat, base_lon = 8.9492, 125.5430
    
    data = []
    for i in range(num_samples):
        zone = np.random.choice(zones)
        lat = base_lat + np.random.uniform(-0.02, 0.02)
        lon = base_lon + np.random.uniform(-0.02, 0.02)
        prev_moisture = np.random.uniform(15.0, 70.0)
        temp = np.random.uniform(24.0, 36.0)
        
        current_moisture = prev_moisture * np.random.uniform(0.85, 0.98) - (temp * 0.15) + np.random.normal(0, 1)
        current_moisture = np.clip(current_moisture, 10.0, 80.0)
        
        data.append({
            "Sensor_ID": f"SENSOR-{i+101:03d}",
            "Zone": zone,
            "Latitude": round(lat, 6),
            "Longitude": round(lon, 6),
            "Temperature_C": round(temp, 1),
            "Previous_Moisture_Pct": round(prev_moisture, 1),
            "Current_Moisture_Pct": round(current_moisture, 1)
        })

    df = pd.DataFrame(data)
    os.makedirs("data", exist_ok=True)
    df.to_csv(filename, index=False)
    print(f"Dataset successfully created at {filename}")

if __name__ == "__main__":
    generate_sensor_data()