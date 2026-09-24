from app.model_predictor import predict_fraud


sample_transaction = {
    "step": 1,
    "type": "PAYMENT",
    "amount": 1000.0,
    "oldbalanceOrg": 5000.0,
    "newbalanceOrig": 4000.0,
    "oldbalanceDest": 2000.0,
    "newbalanceDest": 3000.0,
    "isFlaggedFraud": 0
}


def test_predict_fraud_returns_result():
    result = predict_fraud(sample_transaction)

    assert result is not None


def test_prediction_response_contains_required_fields():
    result = predict_fraud(sample_transaction)

    required_fields = {
        "fraud_prediction",
        "fraud_probability",
        "risk_level",
        "decision",
        "threshold_used"
    }

    assert required_fields.issubset(result.keys())


def test_prediction_probability_is_valid():
    result = predict_fraud(sample_transaction)

    assert 0 <= result["fraud_probability"] <= 1


def test_prediction_risk_level_is_valid():
    result = predict_fraud(sample_transaction)

    assert result["risk_level"] in {
        "Low",
        "Medium",
        "High"
    }


def test_prediction_decision_is_valid():
    result = predict_fraud(sample_transaction)

    assert result["decision"] in {
        "Legitimate",
        "Fraudulent"
    }