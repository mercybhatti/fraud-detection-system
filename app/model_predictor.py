import json
from pathlib import Path

import joblib
import pandas as pd


# Project paths
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"


# Load saved artifacts
preprocessor = joblib.load(
    MODEL_DIR / "preprocessor.pkl"
)

model = joblib.load(
    MODEL_DIR / "xgboost_fraud_model.pkl"
)

with open(MODEL_DIR / "threshold_config.json", "r") as file:
    threshold_config = json.load(file)

FRAUD_THRESHOLD = threshold_config["fraud_threshold"]


def predict_fraud(transaction: dict) -> dict:
    """
    Predict whether a transaction is fraudulent.
    """

    # Convert input dictionary into DataFrame
    input_df = pd.DataFrame([transaction])

    # Apply the same preprocessing used during training
    processed_input = preprocessor.transform(input_df)

    # Generate fraud probability
    fraud_probability = model.predict_proba(processed_input)[0][1]

    # Apply selected threshold
    prediction = int(fraud_probability >= FRAUD_THRESHOLD)

    # Assign risk level
    if fraud_probability >= 0.80:
        risk_level = "High"
    elif fraud_probability >= 0.50:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "fraud_prediction": prediction,
        "fraud_probability": round(float(fraud_probability), 4),
        "risk_level": risk_level,
        "decision": (
            "Fraudulent"
            if prediction == 1
            else "Legitimate"
        ),
        "threshold_used": round(
            float(FRAUD_THRESHOLD), 4
        )
    }