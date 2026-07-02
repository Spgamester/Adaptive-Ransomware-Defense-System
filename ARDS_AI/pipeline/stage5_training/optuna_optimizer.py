import optuna
import joblib
import json
import os

from sklearn.metrics import f1_score

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import ExtraTreesClassifier

from core.dataset_loader import DatasetLoader


loader = DatasetLoader()

X_train, X_valid, X_test, y_train, y_valid, y_test = loader.split(
    benchmark=True,
    benchmark_size=100000
)

print("=" * 80)
print("ARDS OPTUNA")
print("=" * 80)

MODEL = "extratrees"     # xgboost / lightgbm / extratrees
TRIALS = 100

def objective(trial):
    if MODEL == "xgboost":
        model = XGBClassifier(
            n_estimators=trial.suggest_int("n_estimators", 200, 700),
            max_depth=trial.suggest_int("max_depth", 4, 14),
            learning_rate=trial.suggest_float("learning_rate", 0.01, 0.3),
            subsample=trial.suggest_float("subsample", 0.6, 1.0),
            colsample_bytree=trial.suggest_float("colsample_bytree", 0.6, 1.0),
            eval_metric="logloss",
            tree_method="hist",
            random_state=42
        )

    elif MODEL == "lightgbm":
        model = LGBMClassifier(
            n_estimators=trial.suggest_int("n_estimators", 200, 700),
            max_depth=trial.suggest_int("max_depth", 4, 14),
            learning_rate=trial.suggest_float("learning_rate", 0.01, 0.3),
            random_state=42
        )

    else:
        model = ExtraTreesClassifier(
            n_estimators=trial.suggest_int("n_estimators", 200, 700),
            max_depth=trial.suggest_int("max_depth", 10, 40),
            n_jobs=-1,
            random_state=42
        )

    model.fit(X_train, y_train)

    pred = model.predict(X_valid)

    return f1_score(y_valid, pred)

study = optuna.create_study(
    direction="maximize"
)

study.optimize(
    objective,
    n_trials=TRIALS
)

print()

print("=" * 80)

print("BEST SCORE")

print(study.best_value)

print()

print("BEST PARAMETERS")

print(study.best_params)

results_dir = "results"

os.makedirs(
    results_dir,
    exist_ok=True
)

with open(

    os.path.join(

        results_dir,

        f"{MODEL}_best.json"

    ),

    "w"

) as f:

    json.dump(

        study.best_params,

        f,

        indent=4

    )

joblib.dump(

    study.best_params,

    os.path.join(

        results_dir,

        f"{MODEL}_best.pkl"

    )

)