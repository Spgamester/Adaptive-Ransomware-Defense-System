"""
ARDS Production Detector

Compatibility wrapper around the new ML predictor.
Every old module can continue calling predict_file().
"""

from src.ml.predictor import Predictor

# Load model only once
_predictor = Predictor()


def predict_file(file_path: str):
    """
    Predict whether a file is malicious.

    Returns:
        {
            prediction,
            is_malware,
            malware_probability,
            benign_probability,
            features
        }
    """
    return _predictor.predict(file_path)