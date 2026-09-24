from typing import Literal

from pydantic import BaseModel, Field


class TransactionInput(BaseModel):
    step: int = Field(..., ge=0)

    type: Literal[
        "CASH_IN",
        "CASH_OUT",
        "DEBIT",
        "PAYMENT",
        "TRANSFER"
    ]

    amount: float = Field(..., ge=0)
    oldbalanceOrg: float = Field(..., ge=0)
    newbalanceOrig: float = Field(..., ge=0)
    oldbalanceDest: float = Field(..., ge=0)
    newbalanceDest: float = Field(..., ge=0)

    isFlaggedFraud: int = Field(..., ge=0, le=1)


class PredictionResponse(BaseModel):
    fraud_prediction: int = Field(..., ge=0, le=1)
    fraud_probability: float = Field(..., ge=0, le=1)
    risk_level: Literal["Low", "Medium", "High"]
    decision: Literal["Fraudulent", "Legitimate"]
    threshold_used: float = Field(..., ge=0, le=1)