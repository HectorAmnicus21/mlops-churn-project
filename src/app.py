from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, "../models/churn_model.pkl"))

class CustomerData(BaseModel):
    AccountWeeks: float
    ContractRenewal: float
    DataPlan: float
    DataUsage: float
    CustServCalls: float
    DayMins: float
    DayCalls: float
    MonthlyCharge: float
    OverageFee: float
    RoamMins: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(data: CustomerData):
    features = np.array([[
        data.AccountWeeks, data.ContractRenewal, data.DataPlan,
        data.DataUsage, data.CustServCalls, data.DayMins,
        data.DayCalls, data.MonthlyCharge, data.OverageFee, data.RoamMins
    ]])
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]
    return {
        "churn": int(prediction),
        "probability": round(float(probability), 2)
    }