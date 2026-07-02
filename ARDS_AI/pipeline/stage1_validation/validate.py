import os
import pandas as pd

print("=" * 80)
print("ARDS STAGE 1 - DATA VALIDATION")
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

print("\nLoading datasets...\n")

bodmas = pd.read_parquet(BODMAS)
ember = pd.read_parquet(EMBER)

print("Datasets Loaded Successfully.\n")


def validate(df, name):

    print("=" * 80)
    print(name)
    print("=" * 80)

    print("\nShape")
    print(df.shape)

    print("\nMemory (MB)")
    print(round(df.memory_usage(deep=True).sum()/1024/1024,2))

    print("\nDuplicate Rows")
    print(df.duplicated().sum())

    print("\nMissing Values")
    missing = df.isnull().sum().sum()
    print(missing)

    print("\nData Types")
    print(df.dtypes.value_counts())

    print("\nPotential Label Columns")

    labels = []

    for col in df.columns:

        x = col.lower()

        if any(k in x for k in [
            "label",
            "family",
            "class",
            "target",
            "category",
            "malware"
        ]):

            labels.append(col)

    print(labels)

    for col in labels:

        print("\n", col)

        print(df[col].value_counts().head(20))


validate(bodmas,"BODMAS")

validate(ember,"EMBER TRAIN")