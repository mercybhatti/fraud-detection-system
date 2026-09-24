import json
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"

PREDICTION_LOG_FILE = LOG_DIR / "prediction_logs.jsonl"
ERROR_LOG_FILE = LOG_DIR / "error_logs.jsonl"


def log_prediction(transaction: dict, result: dict) -> None:
    """
    Store transaction input and prediction result
    in JSON Lines format.
    """

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "transaction": transaction,
        "prediction": result
    }

    with open(
        PREDICTION_LOG_FILE,
        "a",
        encoding="utf-8"
    ) as file:
        file.write(json.dumps(log_entry) + "\n")


def log_error(error_message: str) -> None:
    """
    Store application errors in JSON Lines format.
    """

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    error_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "error": error_message
    }

    with open(
        ERROR_LOG_FILE,
        "a",
        encoding="utf-8"
    ) as file:
        file.write(json.dumps(error_entry) + "\n")