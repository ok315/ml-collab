import pandas as pd
import pytest

from src.data.validate import validate_dataset


def _write(tmp_path, df, name="data.csv"):
    path = tmp_path / name
    df.to_csv(path, index=False)
    return str(path)


def test_valid_dataset_is_returned(tmp_path):
    path = _write(tmp_path, pd.DataFrame({"x": [1, 2], "Churn": ["Yes", "No"]}))
    df = validate_dataset(path, "Churn")
    assert list(df.columns) == ["x", "Churn"]


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        validate_dataset(str(tmp_path / "nope.csv"), "Churn")


def test_wrong_extension_raises(tmp_path):
    path = tmp_path / "data.txt"
    path.write_text("x,Churn\n1,Yes\n")
    with pytest.raises(ValueError, match="CSV"):
        validate_dataset(str(path), "Churn")


def test_empty_dataset_raises(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("x,Churn\n")
    with pytest.raises(ValueError, match="empty"):
        validate_dataset(str(path), "Churn")


def test_missing_target_column_raises(tmp_path):
    path = _write(tmp_path, pd.DataFrame({"x": [1, 2]}))
    with pytest.raises(ValueError, match="is missing"):
        validate_dataset(path, "Churn")


def test_missing_target_values_raises(tmp_path):
    path = _write(tmp_path, pd.DataFrame({"x": [1, 2], "Churn": ["Yes", None]}))
    with pytest.raises(ValueError, match="missing values"):
        validate_dataset(path, "Churn")
