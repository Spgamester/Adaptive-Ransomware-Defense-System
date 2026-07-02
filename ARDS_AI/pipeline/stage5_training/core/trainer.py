"""
ARDS Universal Trainer
"""

import time

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier


class Trainer:

    def __init__(self):

        self.models = {

            "Random Forest":

                RandomForestClassifier(

                    n_estimators=300,

                    random_state=42,

                    n_jobs=-1

                ),

            "Extra Trees":

                ExtraTreesClassifier(

                    n_estimators=300,

                    random_state=42,

                    n_jobs=-1

                ),

            "XGBoost":

                XGBClassifier(

                    n_estimators=300,

                    max_depth=8,

                    learning_rate=0.05,

                    tree_method="hist",

                    random_state=42,

                    eval_metric="logloss"

                ),

            "LightGBM":

                LGBMClassifier(

                    n_estimators=300,

                    learning_rate=0.05,

                    random_state=42

                ),

            "CatBoost":

                CatBoostClassifier(

                    iterations=300,

                    learning_rate=0.05,

                    verbose=False,

                    random_state=42

                )

        }

    def train(

        self,

        name,

        model,

        X_train,

        y_train

    ):

        print()

        print("="*70)

        print(name)

        print("="*70)

        start = time.time()

        model.fit(

            X_train,

            y_train

        )

        end = time.time()

        print(

            f"Training Time : {end-start:.2f} sec"

        )

        return model