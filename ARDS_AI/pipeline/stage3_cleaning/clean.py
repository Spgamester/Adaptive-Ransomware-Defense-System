import os
import pandas as pd

print("=" * 80)
print("ARDS DATA CLEANING")
print("=" * 80)

BASE = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

BODMAS = os.path.join(
    BASE,
    "datasets",
    "bodmas",
    "bodmas.parquet"
)

EMBER = os.path.join(
    BASE,
    "datasets",
    "ember",
    "train_ember_2018_v2_features.parquet"
)

OUTPUT = os.path.join(
    BASE,
    "datasets",
    "processed"
)

os.makedirs(
    OUTPUT,
    exist_ok=True
)

print("\nLoading datasets...")

bodmas = pd.read_parquet(BODMAS)

ember = pd.read_parquet(EMBER)

print("Loaded.")

print("\nCleaning EMBER...")

ember = ember[
    ember["Label"] != -1
]

print("EMBER Shape :", ember.shape)

print("\nCleaning BODMAS...")

bodmas["family"] = bodmas["family"].fillna("benign")

bodmas["category"] = bodmas["category"].fillna("benign")

print("BODMAS Shape :", bodmas.shape)

print("\nSaving cleaned datasets...")

bodmas.to_parquet(

    os.path.join(
        OUTPUT,
        "bodmas_clean.parquet"
    ),

    index=False

)

ember.to_parquet(

    os.path.join(
        OUTPUT,
        "ember_clean.parquet"
    ),

    index=False

)

print("\nDone.")

print("\nFiles Saved")

print(os.listdir(OUTPUT))