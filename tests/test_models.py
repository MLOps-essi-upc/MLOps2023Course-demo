import pickle

import pytest

from src import MODELS_DIR


@pytest.fixture
def lr_model():
    with open(MODELS_DIR / "iris_LogisticRegression_model.pkl", "rb") as f:
        return pickle.load(f)["model"]


@pytest.mark.parametrize(
    "input, expected",
    [
        ([[6.4, 2.8, 5.6, 2.1]], 2),
        ([[5.0, 2.3, 3.3, 1.0]], 1),
        ([[4.9, 2.5, 4.5, 1.7]], 2),
    ],
)
def test_iris_lr_model(lr_model, input, expected):
    assert lr_model.predict(input) == expected
