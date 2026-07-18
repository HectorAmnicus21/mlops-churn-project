## How to Run

# Customer Churn Prediction API

![CI](https://github.com/HectorAmnicus21/mlops-churn-project/actions/workflows/ci.yml/badge.svg)

ML-сервис для предсказания оттока клиентов (customer churn) на FastAPI...

### Local
```bash
cd src
python -m uvicorn app:app --reload
```

### Docker
```bash
docker build -t churn-api .
docker run -p 8000:8000 churn-api
```

## API Endpoints
- `GET /health` — Health check
- `POST /predict` — Predict customer churn

## Example Request
```json
{
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
}
```

## Example Response
```json
{
  "churn": 0,
  "probability": 0.02
}
```




























