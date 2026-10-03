import pandas as pd

from src.data.quality import missing_summary


def test_counts_nan_and_blank_strings():
    df = pd.DataFrame({"a": [1, None, 3], "b": ["x", " ", ""], "c": [1, 2, 3]})
    out = missing_summary(df)
    assert out.loc["a", "missing"] == 1
    assert out.loc["b", "missing"] == 2
    assert out.loc["c", "missing"] == 0


def test_percent_is_rounded():
    df = pd.DataFrame({"a": [None, 1, 2]})
    assert missing_summary(df).loc["a", "percent"] == 33.33