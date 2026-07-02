import os
import json
import pandas as pd
import numpy as np
from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import VarianceThreshold

print("=" * 80)
print("ARDS FEATURE ANALYSIS")
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
    "processed",
    "bodmas_clean.parquet"
)

EMBER = os.path.join(
    BASE,
    "datasets",
    "processed",
    "ember_clean.parquet"
)

REPORTS = os.path.join(
    BASE,
    "reports",
    "feature_analysis"
)

os.makedirs(
    REPORTS,
    exist_ok=True
)

print("\nLoading datasets...\n")

bodmas = pd.read_parquet(BODMAS)
ember = pd.read_parquet(EMBER)

print("Datasets Loaded.")

print()

print("BODMAS :", bodmas.shape)

print("EMBER  :", ember.shape)

feature_cols = [
    c
    for c in bodmas.columns
    if c.startswith("F")
]

print()

print("Feature Count :", len(feature_cols))

print()

X_bodmas = bodmas[feature_cols]

X_ember = ember[feature_cols]

X = pd.concat(
    [
        X_bodmas,
        X_ember
    ],
    ignore_index=True
)

print("\nSampling 150000 rows for feature analysis...")

X = X.sample(
    n=150000,
    random_state=42
).reset_index(drop=True)

print("Sample Shape :", X.shape)
print()

print("Merged Feature Matrix")

print(X.shape)

print()

print("Checking Missing Values...")

missing = X.isnull().sum().sum()

print("Missing :", missing)

print()

print("Checking Constant Features...")

constant = []

for col in feature_cols:

    if X[col].nunique() <= 1:

        constant.append(col)

print("Constant Features :", len(constant))

print()

selector = VarianceThreshold(threshold=0.0)

selector.fit(X)

selected = list(
    X.columns[
        selector.get_support()
    ]
)

removed = list(
    set(feature_cols) - set(selected)
)

print()

print("Variance Selected :", len(selected))

print("Variance Removed :", len(removed))

print()
print("=" * 80)
print("MUTUAL INFORMATION ANALYSIS")
print("=" * 80)

# -------------------------------------------------
# Prepare Labels
# -------------------------------------------------

y_bodmas = bodmas["Label"]

y_ember = ember["Label"]

y = pd.concat(
    [
        y_bodmas,
        y_ember
    ],
    ignore_index=True
)

# Same sampling used for X
y = y.loc[X.index].reset_index(drop=True)

print()

print("Calculating Mutual Information...")

mi = mutual_info_classif(
    X[selected],
    y,
    random_state=42,
    n_neighbors=5
)

mi_scores = pd.DataFrame({

    "Feature": selected,

    "MI": mi

})

mi_scores = mi_scores.sort_values(

    "MI",

    ascending=False

)

print()

print("Top 20 Features")

print(

    mi_scores.head(20)

)

mi_scores.to_csv(

    os.path.join(

        REPORTS,

        "mutual_information.csv"

    ),

    index=False

)

print()

print("Saved -> mutual_information.csv")