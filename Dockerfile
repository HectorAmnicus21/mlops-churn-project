FROM python:3.13-slim

WORKDIR /app

COPY src/ ./src/
COPY models/ ./models/
COPY data/ ./data/

RUN pip install fastapi uvicorn scikit-learn joblib numpy pandas

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]