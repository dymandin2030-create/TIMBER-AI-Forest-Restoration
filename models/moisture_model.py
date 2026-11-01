import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os

MODEL_PATH = "models/saved_moisture_model.pkl"

def train_moisture_model(data_path="data/sensor_readings.csv"):
    df = pd.read_csv(data_path)
    X = df[["Previous_Moisture_Pct", "Temperature_C"]]
    y = df["Current_Moisture_Pct"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return model

def predict_future_moisture(prev_moisture, temperature):
    if not os.path.exists(MODEL_PATH):
        train_moisture_model()
    model = joblib.load(MODEL_PATH)
    input_data = np.array([[prev_moisture, temperature]])
    return float(model.predict(input_data)[0])