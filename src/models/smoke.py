"""Smoke train: run cleaning, split, training and scoring on the committed sample.

Proves the code runs end to end in CI without DagsHub access. It writes nothing to
data/processed, models/ or metrics.json, because those are tracked by DVC.
"""

import sys

import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

from src.config import PROJECT_ROOT, load_params
from src.models.train import build_pipeline

SAMPLE_PATH = PROJECT_ROOT / "data" / "sample" / "telco_sample.csv"


def main():
    params = load_params()
    target = params["data"]["target_column"]
    seed = params["project"]["random_state"]
    model_params = {k: v for k, v in params["model"].items() if k != "algorithm"}
    model_params["n_estimators"] = 20

    df = pd.read_csv(SAMPLE_PATH).drop(columns=["customerID"], errors="ignore")
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df[target] = (df[target] == "Yes").astype(int)

    train_df, test_df = train_test_split(
        df, test_size=params["data"]["test_size"], random_state=seed, stratify=df[target]
    )
    x_train, y_train = train_df.drop(columns=[target]), train_df[target]
    x_test, y_test = test_df.drop(columns=[target]), test_df[target]

    pipeline = build_pipeline(x_train, model_params, seed)
    pipeline.fit(x_train, y_train)
    auc = roc_auc_score(y_test, pipeline.predict_proba(x_test)[:, 1])

    print(f"Smoke train on {len(df)} rows: roc_auc={auc:.3f}")
    if not 0.5 < auc <= 1.0:
        print("Smoke train FAILED: model is no better than chance")
        sys.exit(1)


if __name__ == "__main__":
    main()
