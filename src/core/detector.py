import numpy as np
import joblib
import os
import sys

def get_model_path():
    if getattr(sys, 'frozen', False):
        # Running in EXE
        base_path = sys._MEIPASS
    else:
        # Running normally
        base_path = os.path.abspath(".")

    return os.path.join(base_path, "models", "ransomware_model.pkl")


model = joblib.load(get_model_path())


def extract_simple_features(file_path):
    """
    Convert file into basic features (temporary mapping)
    """
    try:
        size = os.path.getsize(file_path)

        # Create dummy feature vector (same size as training)
        features = np.random.rand(2381)

        # Inject real info (size influence)
        features[0] = size / 1000000  

        return features

    except:
        return np.zeros(2381)


def predict_file(file_path):
    features = extract_simple_features(file_path)

    features = features.reshape(1, -1)

    prediction = model.predict(features)[0]

    if prediction == 1:
        return "ML: MALWARE"
    else:
        return "ML: SAFE"