from core.dataset_loader import DatasetLoader
from core.trainer import Trainer
from core.evaluator import Evaluator

print("=" * 80)
print("ARDS MODEL BENCHMARK")
print("=" * 80)

loader = DatasetLoader()

X_train, X_valid, X_test, y_train, y_valid, y_test = loader.split(
    benchmark=True,
    benchmark_size=100000
)

trainer = Trainer()
evaluator = Evaluator()

results = []

for name, model in trainer.models.items():

    trained = trainer.train(
        name,
        model,
        X_train,
        y_train
    )

    metrics = evaluator.evaluate(
        trained,
        X_valid,
        y_valid
    )

    metrics["Model"] = name

    results.append(metrics)

print("\n")
print("=" * 80)
print("FINAL LEADERBOARD")
print("=" * 80)

results = sorted(
    results,
    key=lambda x: x["F1"],
    reverse=True
)

for r in results:

    print()

    print(r)