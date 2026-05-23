import joblib
import os
import numpy as np

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')


def load_model():
    model_path = os.path.join(MODEL_DIR, 'phishing_model.pkl')
    if not os.path.exists(model_path):
        raise FileNotFoundError("Model not found. Please train the model first via the Results page.")
    return joblib.load(model_path)


def load_scaler():
    scaler_path = os.path.join(MODEL_DIR, 'scaler.pkl')
    if not os.path.exists(scaler_path):
        raise FileNotFoundError("Scaler not found. Please train the model first via the Results page.")
    return joblib.load(scaler_path)


def get_threat_level(proba: float) -> tuple:
    """Map prediction probability to a threat label and color."""
    if proba < 0.35:
        return "Legitimate", "#00f5a0", "✅"
    elif proba < 0.65:
        return "Suspicious", "#f5a623", "⚠️"
    else:
        return "Phishing", "#f54242", "🚨"


def format_percentage(val: float) -> str:
    return f"{val * 100:.2f}%"


def model_exists() -> bool:
    return os.path.exists(os.path.join(MODEL_DIR, 'phishing_model.pkl'))
