from pathlib import Path

import pandas as pd


def validate_dataset(data_path: str, target_column: str) -> pd.DataFrame:
    """Load a CSV dataset and perform basic validation."""
    path = Path(data_path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    if path.suffix.lower() != ".csv":
        raise ValueError("Expected a CSV dataset.")

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("Dataset is empty.")

    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' is missing.")

    if df[target_column].isna().any():
        raise ValueError(f"Target column '{target_column}' contains missing values.")

    return df


if __name__ == "__main__":
    print("Dataset validation module is ready.")
