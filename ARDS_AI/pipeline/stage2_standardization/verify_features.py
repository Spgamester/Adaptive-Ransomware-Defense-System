import os
import pandas as pd

print("=" * 80)
print("ARDS FEATURE VERIFICATION")
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

bodmas = pd.read_parquet(BODMAS)
ember = pd.read_parquet(EMBER)

bodmas_features = [
    c for c in bodmas.columns
    if c.startswith("F")
]

ember_features = [
    c for c in ember.columns
    if c.startswith("F")
]

print()

print("BODMAS Feature Count :", len(bodmas_features))
print("EMBER Feature Count  :", len(ember_features))

print()

print("Feature Order Identical :", bodmas_features == ember_features)

print()

if bodmas_features == ember_features:
    print("SUCCESS: Features are perfectly aligned.")
else:
    print("ERROR: Feature order mismatch.")

print()

print("First 10 Features")

for i in range(10):
    print(
        i,
        bodmas_features[i],
        ember_features[i]
    )