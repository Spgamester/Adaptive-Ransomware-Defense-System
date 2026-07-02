"""
ARDS Production Feature Extractor

Converts a PE executable into the exact 800-dimensional feature vector
used by the trained LightGBM model.
"""

import json
from pathlib import Path

import numpy as np

from src.ml.config import FEATURE_COLUMNS
from src.ml.ember.features import PEFeatureExtractor


class FeatureExtractor:
    """
    Extracts EMBER features and reduces them to the selected 800 features.
    """

    def __init__(self):

        self.extractor = PEFeatureExtractor()

        with open(FEATURE_COLUMNS, "r") as f:
            feature_names = json.load(f)

        # Convert:
        # F1061 -> 1060
        self.selected_indices = [
            int(name[1:]) - 1
            for name in feature_names
        ]

    def extract(self, exe_path: str):

        exe_path = Path(exe_path)

        if not exe_path.exists():
            raise FileNotFoundError(exe_path)

        with open(exe_path, "rb") as f:
            bytez = f.read()

        full_vector = self.extractor.feature_vector(bytez)

        full_vector = np.asarray(full_vector, dtype=np.float32)

        selected = full_vector[self.selected_indices]

        return selected.reshape(1, -1)