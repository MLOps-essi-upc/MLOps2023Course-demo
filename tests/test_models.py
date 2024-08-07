import pickle

import pytest
from sklearn.metrics import mean_absolute_error, mean_squared_error

from src.config import MODELS_DIR, PROCESSED_DATA_DIR
from src.models.evaluate import load_validation_data


@pytest.fixture
def lr_model():
    with open(MODELS_DIR / "iris_LogisticRegression_model.pkl", "rb") as f:
        return pickle.load(f)["model"]


@pytest.fixture
def iowa_model():
    with open(MODELS_DIR / "iowa_model.pkl", "rb") as f:
        return pickle.load(f)


@pytest.fixture
def iowa_validation_data():
    return load_validation_data(PROCESSED_DATA_DIR)


@pytest.mark.parametrize(
    "sample, expected",
    [
        ([[6.4, 2.8, 5.6, 2.1]], 2),
        ([[5.0, 2.3, 3.3, 1.0]], 1),
        ([[4.9, 2.5, 4.5, 1.7]], 2),
    ],
)
def test_iris_lr_model(lr_model, sample, expected):
    assert lr_model.predict(sample) == expected


def test_iowa_model(iowa_model, iowa_validation_data):
    x, y = iowa_validation_data

    val_predictions = iowa_model.predict(x)

    # Compute the MAE and MSE values for the model
    assert mean_absolute_error(y, val_predictions) == pytest.approx(0.0, rel=0.1)
    assert mean_squared_error(y, val_predictions) == pytest.approx(0.0, rel=0.1)
