from fastapi import FastAPI
import pandas as pd
import joblib
from src.businesslogic.business_logic import get_risk_level, get_retention_action

app = FastAPI(title="Customer Churn Prediction API")

# Load the trained model
model = joblib.load("customer_churn_model.pkl")

@app.post("/churn/predict")
def predict_churn(customer: dict):
    df = pd.DataFrame([customer])
    prob = model.predict_proba(df)[0][1]
    risk = get_risk_level(prob)
    action = get_retention_action(risk)
    return {
        "churn_probability": round(float(prob), 2),
        "risk_level": risk,
        "recommended_action": action
    }
