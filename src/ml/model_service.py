"""
ARDS Model Service

Loads the trained LightGBM model once and provides prediction methods.
"""

from pathlib import Path
import joblib

from src.ml.config import MODEL_PATH


class ModelService:

    def __init__(self):

        model_path = Path(MODEL_PATH)

        if not model_path.exists():
            raise FileNotFoundError(model_path)

        self.model = joblib.load(model_path)

    def predict(self, features):

        prediction = self.model.predict(features)[0]

        probability = None

        if hasattr(self.model, "predict_proba"):

            probability = self.model.predict_proba(features)[0]

        return prediction, probability