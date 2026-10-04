"""Data quality checks: schema, value ranges and null counts.

CI runs this on the committed sample. To check the full dataset:
    python -m src.data.checks data/raw/Telco-Customer-Churn.csv
"""

import sys
from pathlib import Path

import pandas as pd

from src.config import PROJECT_ROOT, load_params
from src.data.validate import validate_dataset

DEFAULT_PATH = PROJECT_ROOT / "data" / "sample" / "telco_sample.csv"
REQUIRED_COLUMNS = {"customerID", "tenure", "MonthlyCharges", "TotalCharges", "Contract", "Churn"}
NUMERIC_RANGES = {"tenure": (0, 80), "MonthlyCharges": (0, 200)}
MAX_BLANK_TOTAL_CHARGES = 0.02


def run_checks(path: Path = DEFAULT_PATH) -> list[str]:
    """Return a list of problems. An empty list means every check passed."""
    target = load_params()["data"]["target_column"]
    df = validate_dataset(str(path), target)
    problems = []

    missing_cols = REQUIRED_COLUMNS - set(df.columns)
    if missing_cols:
        return [f"missing columns: {sorted(missing_cols)}"]

    nulls = df.isna().sum()
    for col, count in nulls[nulls > 0].items():
        problems.append(f"{col} has {count} null values")

    total = pd.to_numeric(df["TotalCharges"], errors="coerce")
    if total.isna().mean() > MAX_BLANK_TOTAL_CHARGES:
        problems.append(
            f"TotalCharges is blank or non-numeric in {total.isna().mean():.1%} of rows"
        )

    for col, (low, high) in NUMERIC_RANGES.items():
        values = pd.to_numeric(df[col], errors="coerce")
        if values.isna().any():
            problems.append(f"{col} contains non-numeric values")
        elif values.min() < low or values.max() > high:
            problems.append(f"{col} outside [{low}, {high}]: {values.min()} to {values.max()}")

    bad_labels = set(df[target].unique()) - {"Yes", "No"}
    if bad_labels:
        problems.append(f"unexpected {target} values: {sorted(bad_labels)}")
    if "SeniorCitizen" in df.columns and not set(df["SeniorCitizen"].unique()) <= {0, 1}:
        problems.append("SeniorCitizen must be 0 or 1")
    return problems


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PATH
    problems = run_checks(path)
    if problems:
        print("Data checks FAILED:")
        for problem in problems:
            print(f" - {problem}")
        sys.exit(1)
    print(f"Data checks passed for {path}")


if __name__ == "__main__":
    main()
