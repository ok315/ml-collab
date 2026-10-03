import pandas as pd
from sklearn.model_selection import train_test_split

from src.config import PROJECT_ROOT, load_params
from src.data.validate import validate_dataset

RAW_PATH = PROJECT_ROOT / "data" / "raw" / "Telco-Customer-Churn.csv"
OUT_DIR = PROJECT_ROOT / "data" / "processed"


def main():
    params = load_params()
    target = params["data"]["target_column"]
    seed = params["project"]["random_state"]

    df = validate_dataset(str(RAW_PATH), target)
    df = df.drop(columns=["customerID"], errors="ignore")
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df[target] = (df[target] == "Yes").astype(int)

    train_df, test_df = train_test_split(
        df,
        test_size=params["data"]["test_size"],
        random_state=seed,
        stratify=df[target],
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    train_df.to_csv(OUT_DIR / "train.csv", index=False)
    test_df.to_csv(OUT_DIR / "test.csv", index=False)


if __name__ == "__main__":
    main()