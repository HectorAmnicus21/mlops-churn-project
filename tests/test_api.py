import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))
from app import app
from fastapi.testclient import TestClient

client = TestClient(app)
client.__enter__()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_predict_valid():
    response = client.post("/predict", json={
        "AccountWeeks": 128,
        "ContractRenewal": 1,
        "DataPlan": 1,
        "DataUsage": 2.7,
        "CustServCalls": 1,
        "DayMins": 265.1,
        "DayCalls": 110,
        "MonthlyCharge": 89.0,
        "OverageFee": 9.87,
        "RoamMins": 10.0
    })
    assert response.status_code == 200
    assert "churn" in response.json()
    assert "probability" in response.json()

def test_predict_missing_field():
    response = client.post("/predict", json={
        "AccountWeeks": 128
    })
    assert response.status_code == 422