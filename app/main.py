import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.logger import (
    PREDICTION_LOG_FILE,
    log_error,
    log_prediction
)
from app.model_predictor import predict_fraud
from app.schemas import TransactionInput, PredictionResponse


app = FastAPI(
    title="Fraud Detection API",
    description="API for detecting fraudulent financial transactions.",
    version="1.0.0"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Fraud Detection API is running",
        "status": "healthy"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "fraud-detection-api",
        "model_loaded": True
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(transaction: TransactionInput):
    try:
        transaction_data = transaction.model_dump()

        result = predict_fraud(transaction_data)

        log_prediction(transaction_data, result)

        return result

    except Exception as error:
        log_error(str(error))

        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the transaction."
        ) from error


@app.get("/history")
def prediction_history():
    if not PREDICTION_LOG_FILE.exists():
        return {
            "total_predictions": 0,
            "predictions": []
        }

    predictions = []

    with open(
        PREDICTION_LOG_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        for line in file:
            if line.strip():
                predictions.append(json.loads(line))

    return {
        "total_predictions": len(predictions),
        "predictions": predictions[-20:]
    }

@app.get("/stats")
def prediction_stats():
    if not PREDICTION_LOG_FILE.exists():
        return {
            "total_predictions": 0,
            "fraud_predictions": 0,
            "legitimate_predictions": 0,
            "fraud_percentage": 0.0
        }

    predictions = []

    with open(
        PREDICTION_LOG_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        for line in file:
            if line.strip():
                predictions.append(json.loads(line))

    total_predictions = len(predictions)

    fraud_predictions = sum(
        record["prediction"]["fraud_prediction"] == 1
        for record in predictions
    )

    legitimate_predictions = (
        total_predictions - fraud_predictions
    )

    fraud_percentage = (
        (fraud_predictions / total_predictions) * 100
        if total_predictions > 0
        else 0.0
    )

    return {
        "total_predictions": total_predictions,
        "fraud_predictions": fraud_predictions,
        "legitimate_predictions": legitimate_predictions,
        "fraud_percentage": round(fraud_percentage, 2)
    }