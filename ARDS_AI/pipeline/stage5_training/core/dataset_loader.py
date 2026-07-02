"""
ARDS Dataset Loader
===================

Loads the canonical dataset and creates:

Train
Validation
Test

Also supports benchmark sampling.
"""

import os
import pandas as pd

from sklearn.model_selection import train_test_split


class DatasetLoader:

    def __init__(self):

        BASE = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__)
                    )
                )
            )
        )

        self.dataset_path = os.path.join(

            BASE,

            "datasets",

            "processed",

            "ards_training_dataset.parquet"

        )

    def load(self):

        print("\nLoading Canonical Dataset...\n")

        df = pd.read_parquet(

            self.dataset_path

        )

        print("Loaded.")

        print(df.shape)

        return df

    def split(

        self,

        benchmark=False,

        benchmark_size=100000,

        random_state=42

    ):

        df = self.load()

        if benchmark:

            print("\nCreating Benchmark Dataset...\n")

            df, _ = train_test_split(

                df,

                train_size=benchmark_size,

                random_state=random_state,

                stratify=df["Label"]

            )
            print(df.shape)

        X = df.drop(

            columns=["Label"]

        )

        y = df["Label"]

        X_train, X_temp, y_train, y_temp = train_test_split(

            X,

            y,

            test_size=0.30,

            random_state=random_state,

            stratify=y

        )

        X_valid, X_test, y_valid, y_test = train_test_split(

            X_temp,

            y_temp,

            test_size=0.50,

            random_state=random_state,

            stratify=y_temp

        )

        print()

        print("Train :", X_train.shape)

        print("Valid :", X_valid.shape)

        print("Test  :", X_test.shape)

        return (

            X_train,

            X_valid,

            X_test,

            y_train,

            y_valid,

            y_test

        )