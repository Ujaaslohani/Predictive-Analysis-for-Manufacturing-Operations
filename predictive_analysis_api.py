from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel
from typing import Dict
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
import os


app = FastAPI()


model = None
data = None


MODEL_FILE = "model.pkl"

class PredictionInput(BaseModel):
    Hydraulic_Pressure: float
    Coolant_Pressure: float
    Air_System_Pressure: float
    Coolant_Temperature: float
    Hydraulic_Oil_Temperature: float
    Spindle_Bearing_Temperature: float
    Spindle_Vibration: float
    Tool_Vibration: float
    Spindle_Speed: int
    Voltage: float
    Torque: float
    Cutting: float

@app.post("/upload")
async def upload(file: UploadFile):
    try:
        global data
        
        df = pd.read_csv(file.file)

        
        df.rename(columns={
            "Hydraulic_Pressure(bar)": "Hydraulic_Pressure",
            "Coolant_Pressure(bar)": "Coolant_Pressure",
            "Air_System_Pressure(bar)": "Air_System_Pressure",
            "Coolant_Temperature": "Coolant_Temperature",
            "Hydraulic_Oil_Temperature(?C)": "Hydraulic_Oil_Temperature",
            "Spindle_Bearing_Temperature(?C)": "Spindle_Bearing_Temperature",
            "Spindle_Vibration(?m)": "Spindle_Vibration",
            "Tool_Vibration(?m)": "Tool_Vibration",
            "Spindle_Speed(RPM)": "Spindle_Speed",
            "Voltage(volts)": "Voltage",
            "Torque(Nm)": "Torque",
            "Cutting(kN)": "Cutting",
            "Downtime": "Downtime"
        }, inplace=True)

        
        df["Downtime"] = df["Downtime"].apply(lambda x: 1 if x == "Machine_Failure" else 0)

        data = df
        return {"message": "Data uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/train")
async def train():
    try:
        global model, data
        if data is None:
            raise HTTPException(status_code=400, detail="No data uploaded. Use the /upload endpoint first.")

        
        feature_columns = [
            "Hydraulic_Pressure", "Coolant_Pressure", "Air_System_Pressure",
            "Coolant_Temperature", "Hydraulic_Oil_Temperature", "Spindle_Bearing_Temperature",
            "Spindle_Vibration", "Tool_Vibration", "Spindle_Speed", "Voltage", "Torque", "Cutting"
        ]
        X = data[feature_columns]
        y = data["Downtime"]

        
        X.fillna(X.mean(), inplace=True)

        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        
        model = LogisticRegression()
        model.fit(X_train, y_train)

        
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        
        joblib.dump(model, MODEL_FILE)

        return {
            "message": "Model trained successfully.",
            "accuracy": accuracy,
            "f1_score": f1
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict")
async def predict(input_data: PredictionInput):
    try:
        global model
        if model is None:
            if os.path.exists(MODEL_FILE):
                model = joblib.load(MODEL_FILE)
            else:
                raise HTTPException(status_code=400, detail="No model found. Train the model using /train endpoint.")

        
        input_df = pd.DataFrame([input_data.dict()])
        prediction = model.predict(input_df)[0]
        confidence = max(model.predict_proba(input_df)[0])

        return {
            "Downtime": "Yes" if prediction == 1 else "No",
            "Confidence": round(confidence, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
