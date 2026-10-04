import pandas as pd


def missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Per column: number and percent of missing values.
    Blank or whitespace-only strings count as missing."""
    blank = df.apply(lambda col: col.astype("string").str.strip().eq(""))
    missing = (df.isna() | blank.fillna(False)).sum()
    return pd.DataFrame(
        {"missing": missing, "percent": (missing / len(df) * 100).round(2)}
    ).sort_values("missing", ascending=False)
