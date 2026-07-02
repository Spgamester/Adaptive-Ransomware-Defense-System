import pandas as pd
import os

print("=" * 80)
print("ARDS AI DATASET INSPECTOR")
print("=" * 80)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BODMAS_PATH = os.path.join(
    BASE,
    "datasets",
    "bodmas",
    "bodmas.parquet"
)

EMBER_TRAIN = os.path.join(
    BASE,
    "datasets",
    "ember",
    "train_ember_2018_v2_features.parquet"
)

EMBER_TEST = os.path.join(
    BASE,
    "datasets",
    "ember",
    "test_ember_2018_v2_features.parquet"
)

print("\nLoading datasets...\n")

bodmas = pd.read_parquet(BODMAS_PATH)
ember_train = pd.read_parquet(EMBER_TRAIN)
ember_test = pd.read_parquet(EMBER_TEST)


def inspect(df, name):

    print("\n")
    print("=" * 80)
    print(name)
    print("=" * 80)

    print("\nShape")
    print(df.shape)

    print("\nMemory Usage (MB)")
    print(round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2))

    print("\nColumns")
    print(len(df.columns))

    print("\nColumn Names")
    print(list(df.columns))

    print("\nData Types")
    print(df.dtypes)

    print("\nMissing Values")
    print(df.isnull().sum().sort_values(ascending=False).head(20))

    print("\nDuplicate Rows")
    print(df.duplicated().sum())

    print("\nFirst Five Rows")
    print(df.head())

    print("\nStatistics")
    print(df.describe(include="all"))


inspect(bodmas, "BODMAS")

inspect(ember_train, "EMBER TRAIN")

inspect(ember_test, "EMBER TEST")

print("\n")
print("=" * 80)
print("COMPARISON")
print("=" * 80)

print("\nBODMAS Features :", len(bodmas.columns))

print("EMBER Features :", len(ember_train.columns))

common = set(bodmas.columns).intersection(
    ember_train.columns
)

print("\nCommon Features :", len(common))

print("\n")

print(sorted(list(common)))

print("\nInspection Finished")
