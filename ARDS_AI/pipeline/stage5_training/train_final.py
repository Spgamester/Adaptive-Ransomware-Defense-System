"""
ARDS Production Builder
=======================

Official production model builder.

This script:

• Loads canonical dataset
• Trains production model
• Evaluates performance
• Saves deployment artifacts
• Generates metadata
"""

import os
import json
import time
import joblib
import platform
import pandas as pd
import numpy as np

from datetime import datetime

from lightgbm import LGBMClassifier

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix
)

print("="*80)
print("ARDS PRODUCTION BUILDER")
print("="*80)

BASE = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

DATASET = os.path.join(
    BASE,
    "datasets",
    "processed",
    "ards_training_dataset.parquet"
)

RESULTS = os.path.join(
    BASE,
    "pipeline",
    "stage5_training",
    "results"
)

OUTPUT = os.path.join(
    BASE,
    "pipeline",
    "stage5_training",
    "production"
)

os.makedirs(
    OUTPUT,
    exist_ok=True
)
print()

print("Loading Champion...")

with open(
    os.path.join(
        RESULTS,
        "champion.json"
    )
) as f:

    champion = json.load(f)

params = champion["parameters"]

print(champion["model"])

print()

print("Loading Dataset...")

df = pd.read_parquet(DATASET)

print(df.shape)

X = df.drop(
    columns=["Label"]
)

y = df["Label"]

feature_columns = list(X.columns)

print()

print("Splitting Dataset...")

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    stratify=y,

    random_state=42

)

print()

print("Train :", X_train.shape)

print("Test  :", X_test.shape)

print()

print("=" * 80)
print("TRAINING PRODUCTION MODEL")
print("=" * 80)

model = LGBMClassifier(

    n_estimators=params["n_estimators"],

    max_depth=params["max_depth"],

    learning_rate=params["learning_rate"],

    objective="binary",

    random_state=42,

    n_jobs=-1,

    verbosity=-1

)

start = time.time()

model.fit(

    X_train,

    y_train

)

training_time = time.time() - start

print()

print(f"Training Time : {training_time:.2f} seconds")

print()

print("=" * 80)
print("MODEL EVALUATION")
print("=" * 80)

prediction = model.predict(X_test)

probability = model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, prediction)

precision = precision_score(y_test, prediction)

recall = recall_score(y_test, prediction)

f1 = f1_score(y_test, prediction)

roc = roc_auc_score(y_test, probability)

print()

print(f"Accuracy  : {accuracy:.6f}")

print(f"Precision : {precision:.6f}")

print(f"Recall    : {recall:.6f}")

print(f"F1 Score  : {f1:.6f}")

print(f"ROC AUC   : {roc:.6f}")

report = classification_report(

    y_test,

    prediction,

    output_dict=True

)

matrix = confusion_matrix(

    y_test,

    prediction
)

print()

print("=" * 80)
print("SAVING ARTIFACTS")
print("=" * 80)

joblib.dump(

    model,

    os.path.join(

        OUTPUT,

        "ards_model.pkl"

    )

)

joblib.dump(

    feature_columns,

    os.path.join(

        OUTPUT,

        "feature_columns.pkl"

    )

)

with open(

    os.path.join(

        OUTPUT,

        "feature_columns.json"

    ),

    "w"

) as f:

    json.dump(

        feature_columns,

        f,

        indent=2

    )

with open(

    os.path.join(

        OUTPUT,

        "classification_report.json"

    ),

    "w"

) as f:

    json.dump(

        report,

        f,

        indent=4

    )

metrics = {

    "model": champion["model"],

    "training_time_seconds": training_time,

    "accuracy": float(accuracy),

    "precision": float(precision),

    "recall": float(recall),

    "f1_score": float(f1),

    "roc_auc": float(roc),

    "samples": int(len(df)),

    "features": int(X.shape[1]),

    "python": platform.python_version(),

    "created": datetime.now().isoformat()

}

with open(

    os.path.join(

        OUTPUT,

        "training_metrics.json"

    ),

    "w"

) as f:

    json.dump(

        metrics,

        f,

        indent=4

    )

pd.DataFrame(

    matrix,

    columns=["Predicted Benign", "Predicted Malware"],

    index=["Actual Benign", "Actual Malware"]

).to_csv(

    os.path.join(

        OUTPUT,

        "confusion_matrix.csv"

    )

)

print()

print("=" * 80)

print("ARDS PRODUCTION BUILD COMPLETE")

print("=" * 80)

print()

print("Artifacts Saved")

print()

for file in sorted(os.listdir(OUTPUT)):

    print("•", file)