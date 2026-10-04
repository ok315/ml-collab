import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.config import PROJECT_ROOT, load_params

TRAIN_PATH = PROJECT_ROOT / "data" / "processed" / "train.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "model.joblib"


def build_pipeline(X: pd.DataFrame, model_params: dict, seed: int) -> Pipeline:
    numeric = X.select_dtypes(include="number").columns.tolist()
    categorical = [c for c in X.columns if c not in numeric]

    preprocess = ColumnTransformer(
        [
            (
                "num",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="median")),
                        ("scale", StandardScaler()),
                    ]
                ),
                numeric,
            ),
            (
                "cat",
                Pipeline(
                    [
                        ("impute", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                categorical,
            ),
        ]
    )
    clf = RandomForestClassifier(random_state=seed, **model_params)
    return Pipeline([("preprocess", preprocess), ("model", clf)])


def main():
    params = load_params()
    target = params["data"]["target_column"]
    seed = params["project"]["random_state"]
    model_params = {k: v for k, v in params["model"].items() if k != "algorithm"}

    train = pd.read_csv(TRAIN_PATH)
    X, y = train.drop(columns=[target]), train[target]

    pipeline = build_pipeline(X, model_params, seed)
    pipeline.fit(X, y)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)


if __name__ == "__main__":
    main()
