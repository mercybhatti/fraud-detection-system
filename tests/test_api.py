from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


sample_transaction = {
    "step": 1,
    "type": "CASH_IN",
    "amount": 1000.0,
    "oldbalanceOrg": 5000.0,
    "newbalanceOrig": 4000.0,
    "oldbalanceDest": 2000.0,
    "newbalanceDest": 3000.0,
    "isFlaggedFraud": 0
}


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert "message" in data


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "fraud-detection-api"
    assert data["model_loaded"] is True


def test_predict_endpoint():
    response = client.post(
        "/predict",
        json=sample_transaction
    )

    assert response.status_code == 200

    data = response.json()

    assert "fraud_prediction" in data
    assert "fraud_probability" in data
    assert "risk_level" in data
    assert "decision" in data
    assert "threshold_used" in data


def test_prediction_probability_is_valid():
    response = client.post(
        "/predict",
        json=sample_transaction
    )

    assert response.status_code == 200

    data = response.json()

    assert 0 <= data["fraud_probability"] <= 1


def test_history_endpoint():
    response = client.get("/history")

    assert response.status_code == 200

    data = response.json()

    assert "total_predictions" in data
    assert "predictions" in data
    assert isinstance(data["predictions"], list)


def test_stats_endpoint():
    response = client.get("/stats")

    assert response.status_code == 200

    data = response.json()

    assert "total_predictions" in data
    assert "fraud_predictions" in data
    assert "legitimate_predictions" in data
    assert "fraud_percentage" in data