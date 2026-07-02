import os
import pandas as pd

print("=" * 80)
print("ARDS DATASET MERGER")
print("=" * 80)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

print("\nLoading datasets...\n")

bodmas = pd.read_parquet(BODMAS)
ember = pd.read_parquet(EMBER)

print("Loaded.")

print()

print("BODMAS Shape :", bodmas.shape)

print("EMBER Shape  :", ember.shape)

print()

print("Checking feature compatibility...")

bodmas_features = set(bodmas.columns)

ember_features = set(ember.columns)

common = sorted(
    list(
        bodmas_features.intersection(
            ember_features
        )
    )
)

only_bodmas = sorted(
    list(
        bodmas_features - ember_features
    )
)

only_ember = sorted(
    list(
        ember_features - bodmas_features
    )
)

print()

print("Common Features :", len(common))

print("Only BODMAS     :", len(only_bodmas))

print("Only EMBER      :", len(only_ember))

print()

print("First 20 Common Features")

print(common[:20])

print()

print("Saving reports...")

os.makedirs(
    "../reports",
    exist_ok=True
)

pd.DataFrame(
    common,
    columns=["Common_Features"]
).to_csv(
    "../reports/common_features.csv",
    index=False
)

pd.DataFrame(
    only_bodmas,
    columns=["Only_BODMAS"]
).to_csv(
    "../reports/bodmas_only.csv",
    index=False
)

pd.DataFrame(
    only_ember,
    columns=["Only_EMBER"]
).to_csv(
    "../reports/ember_only.csv",
    index=False
)

print()

print("Done.")