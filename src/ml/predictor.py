"""
ARDS Predictor
End-to-end malware prediction pipeline.
"""

from src.ml.feature_extractor import FeatureExtractor
from src.ml.model_service import ModelService


class Predictor:

    def __init__(self):
        self.extractor = FeatureExtractor()
        self.model_service = ModelService()

    def predict(self, exe_path):

        features = self.extractor.extract(exe_path)

        prediction, probability = self.model_service.predict(features)

        if probability is not None:
            malware_probability = float(probability[1])
            benign_probability = float(probability[0])
        else:
            malware_probability = None
            benign_probability = None

        return {
    "prediction": int(prediction),
    "is_malware": bool(prediction),
    "malware_probability": malware_probability,
    "benign_probability": benign_probability,
}