from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Models
MODEL_DIR = PROJECT_ROOT / "models"

MODEL_PATH = MODEL_DIR / "ards_model.pkl"

FEATURE_COLUMNS = MODEL_DIR / "feature_columns.json"