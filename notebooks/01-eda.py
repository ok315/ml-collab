# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
# cell 1: setup (finds the repo root so imports work from notebooks/)
import sys
from pathlib import Path

import pandas as pd

ROOT = next(
    p for p in [Path.cwd(), *Path.cwd().parents] if (p / "params.yaml").exists()
)
sys.path.insert(0, str(ROOT))

# %%
# cell 2: load and look
df = pd.read_csv(ROOT / "data" / "raw" / "Telco-Customer-Churn.csv")
print(df.shape)
print(df.dtypes)

# %%
# cell 3: target balance
df["Churn"].value_counts(normalize=True)


# %%
# cell 4: helper, written here first and moved to src/ in step 4
def missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Per column: number and percent of missing values.
    Blank or whitespace-only strings count as missing."""
    blank = df.apply(lambda col: col.astype("string").str.strip().eq(""))
    missing = (df.isna() | blank.fillna(False)).sum()
    return pd.DataFrame(
        {"missing": missing, "percent": (missing / len(df) * 100).round(2)}
    ).sort_values("missing", ascending=False)


missing_summary(df).head()

# %%
# cell 5: one plot
df.groupby("Contract")["Churn"].apply(lambda s: (s == "Yes").mean()).plot.bar()
