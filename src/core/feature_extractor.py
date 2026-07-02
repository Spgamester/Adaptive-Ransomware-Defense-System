"""
ARDS Feature Extractor
======================

Uses the official EMBER PE feature extractor to generate the
2381-dimensional feature vector and reduces it to the exact
800 features used during model training.
"""

import json
from pathlib import Path

import numpy as np
from src.ml.ember.features import PEFeatureExtractor


class FeatureExtractor:
    """
    Production feature extractor.
    """

    def __init__(self):

        self.extractor = PEFeatureExtractor()

        project_root = Path(__file__).resolve().parents[2]

        feature_file = (
            project_root
            / "ARDS_AI"
            / "pipeline"
            / "stage5_training"
            / "production"
            / "feature_columns.json"
        )

        with open(feature_file, "r") as f:
            feature_names = json.load(f)

        # Convert:
        # F1061 -> 1060
        self.indices = [
            int(name[1:]) - 1
            for name in feature_names
        ]

    def extract(self, file_path):

        with open(file_path, "rb") as f:
            bytez = f.read()

        vector = self.extractor.feature_vector(bytez)

        vector = np.asarray(vector, dtype=np.float32)

        selected = vector[self.indices]

        return selected.reshape(1, -1)