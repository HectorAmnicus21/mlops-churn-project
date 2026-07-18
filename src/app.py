from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import os

from src.database import init_db, SessionLocal, PredictionLog

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, "../models/churn_model.pkl"))

@app.on_event("startup")
def startup_event():
    init_db()

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

    db = SessionLocal()
    log = PredictionLog(
        account_weeks=data.AccountWeeks,
        churn=int(prediction),
        probability=round(float(probability), 2)
    )
    db.add(log)
    db.commit()
    db.close()

    return {
        "churn": int(prediction),
        "probability": round(float(probability), 2)
    }

@app.get("/logs")
def get_logs():
    db = SessionLocal()
    logs = db.query(PredictionLog).order_by(PredictionLog.id.desc()).limit(20).all()
    db.close()
    return [
        {"id": l.id, "churn": l.churn, "probability": l.probability, "created_at": str(l.created_at)}
        for l in logs
    ]