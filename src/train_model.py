import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

# Загружаем данные
df = pd.read_csv("../data/telecom_churn.csv")

# Разделяем на признаки и целевую переменную
X = df.drop("Churn", axis=1)
y = df["Churn"]

# Разделяем на train и test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучаем модель
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Проверяем точность
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy:.2f}")

# Сохраняем модель
os.makedirs("../models", exist_ok=True)
joblib.dump(model, "../models/churn_model.pkl")
print("Model saved to models/churn_model.pkl")