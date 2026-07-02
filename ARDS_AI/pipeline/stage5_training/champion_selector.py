"""
ARDS Champion Selector
======================

Compares optimized models and selects
the production champion.

Author : ARDS
"""

import json
import os

print("=" * 80)
print("ARDS CHAMPION SELECTOR")
print("=" * 80)

BASE = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

RESULTS = os.path.join(
    BASE,
    "pipeline",
    "stage5_training",
    "results"
)

MODELS = {

    "xgboost": {

        "f1": 0.966660000,

        "training_time": 23.3,

        "inference": 0.069

    },

    "lightgbm": {

        "f1": 0.966691848,

        "training_time": 10.4,

        "inference": 0.059

    },

    "extratrees": {

        "f1": 0.954536018,

        "training_time": 24.9,

        "inference": 0.302

    }

}
print()

print("Scoring Models...\n")

scores = {}

for name, info in MODELS.items():

    score = (

        info["f1"] * 0.80 +

        (1 / info["training_time"]) * 0.10 +

        (1 / info["inference"]) * 0.10

    )

    scores[name] = score

winner = max(

    scores,

    key=scores.get

)

print()

print("Champion :", winner)

print()

print("Score :", scores[winner])

parameter_file = os.path.join(

    RESULTS,

    f"{winner}_best.json"

)

with open(parameter_file) as f:

    parameters = json.load(f)

champion = {

    "model": winner,

    "parameters": parameters

}

with open(

    os.path.join(

        RESULTS,

        "champion.json"

    ),

    "w"

) as f:

    json.dump(

        champion,

        f,

        indent=4

    )

print()

print("Champion configuration saved.")

print()

print(champion)