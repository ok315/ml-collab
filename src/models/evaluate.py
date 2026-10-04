import json
import subprocess

import joblib
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from src.config import PROJECT_ROOT, load_params

TEST_PATH = PROJECT_ROOT / "data" / "processed" / "test.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "model.joblib"
METRICS_PATH = PROJECT_ROOT / "metrics.json"


def git_sha() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=PROJECT_ROOT, text=True
        ).strip()
    except (subprocess.CalledProcessError, OSError):
        return "unknown"


def main():
    target = load_params()["data"]["target_column"]
    test = pd.read_csv(TEST_PATH)
    X, y = test.drop(columns=[target]), test[target]

    model = joblib.load(MODEL_PATH)
    pred = model.predict(X)
    proba = model.predict_proba(X)[:, 1]

    metrics = {
        "accuracy": round(accuracy_score(y, pred), 4),
        "precision": round(precision_score(y, pred), 4),
        "recall": round(recall_score(y, pred), 4),
        "f1": round(f1_score(y, pred), 4),
        "roc_auc": round(roc_auc_score(y, proba), 4),
        "git_commit": git_sha(),
    }
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
