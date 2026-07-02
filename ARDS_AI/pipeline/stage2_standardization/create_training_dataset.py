import os
import pandas as pd

print("=" * 80)
print("ARDS CANONICAL DATASET CREATOR")
print("=" * 80)

BASE = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

REPORTS = os.path.join(
    BASE,
    "reports",
    "feature_analysis",
    "mutual_information.csv"
)

BODMAS = os.path.join(
    BASE,
    "datasets",
    "processed",
    "bodmas_clean.parquet"
)

EMBER = os.path.join(
    BASE,
    "datasets",
    "processed",
    "ember_clean.parquet"
)

OUTPUT = os.path.join(
    BASE,
    "datasets",
    "processed",
    "ards_training_dataset.parquet"
)

print("\nLoading...")

mi = pd.read_csv(REPORTS)

bodmas = pd.read_parquet(BODMAS)

ember = pd.read_parquet(EMBER)

print("Loaded.")

# -------------------------------------------------------
# Select Top Features
# -------------------------------------------------------

TOP_FEATURES = 800

selected = mi.head(TOP_FEATURES)["Feature"].tolist()

print()

print("Selected Features :", len(selected))

# -------------------------------------------------------
# Build Dataset
# -------------------------------------------------------

bodmas_df = bodmas[selected].copy()
bodmas_df["Label"] = bodmas["Label"]

ember_df = ember[selected].copy()
ember_df["Label"] = ember["Label"]

dataset = pd.concat(
    [
        bodmas_df,
        ember_df
    ],
    ignore_index=True
)

print()

print("Final Dataset Shape")

print(dataset.shape)

print()

print("Saving...")

dataset.to_parquet(
    OUTPUT,
    index=False
)

print()

print("Saved Successfully")

print(OUTPUT)