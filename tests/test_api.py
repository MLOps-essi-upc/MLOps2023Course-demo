from http import HTTPStatus

import cv2
import pytest
from fastapi.testclient import TestClient

from src.app.api import app
from src.config import TEST_DATA_DIR


def read_image(image_path):
    image = cv2.imread(str(image_path))
    image_name = image_path.stem
    class_name = image_name[image_name.find("_") + 1 :]

    return image, class_name


@pytest.fixture(scope="module", autouse=True)
def client():
    # Use the TestClient with a `with` statement to trigger the startup and shutdown events.
    with TestClient(app) as client:
        yield client


@pytest.fixture
def payload():
    return {
        "sepal_length": 6.4,
        "sepal_width": 2.8,
        "petal_length": 5.6,
        "petal_width": 2.1,
    }


def test_root(client):
    response = client.get("/")
    json = response.json()
    assert response.status_code == 200
    assert (
        json["data"]["message"]
        == "Welcome to IRIS classifier! Please, read the `/docs`!"
    )
    assert json["message"] == "OK"
    assert json["status-code"] == 200


def test_get_all_models(client):
    response = client.get("/models/tabular")
    json = response.json()
    assert response.status_code == 200
    assert json["data"] == [
        {
            "type": "LogisticRegression",
            "parameters": {
                "C": 0.1,
                "max_iter": 20,
                "fit_intercept": True,
                "solver": "liblinear",
                "random_state": 0,
            },
            "accuracy": {"accuracy": 0.9145454545454547},
        },
        {
            "type": "SVC",
            "parameters": {"kernel": "linear", "random_state": 0},
            "accuracy": {"accuracy": 0.9818181818181818},
        },
    ]
    assert json["message"] == "OK"
    assert json["status-code"] == 200


def test_get_one_model(client):
    response = client.get("/models/tabular?model_type=SVC")
    json = response.json()
    assert response.status_code == 200
    assert json["data"] == [
        {
            "type": "SVC",
            "parameters": {"kernel": "linear", "random_state": 0},
            "accuracy": {"accuracy": 0.9818181818181818},
        }
    ]
    assert json["message"] == "OK"
    assert json["status-code"] == 200


def test_get_one_model_not_found(client):
    response = client.get("/models/tabular?model_type=RandomForestClassifier")
    assert response.status_code == 400
    assert response.json()["detail"] == "Type not found"


def test_model_prediction(client, payload):
    response = client.post("/predict/tabular/LogisticRegression", json=payload)
    json = response.json()
    assert response.status_code == 200
    assert json["data"]["prediction"] == 2
    assert json["message"] == "OK"
    assert json["status-code"] == 200


def test_model_prediction_not_found(client, payload):
    response = client.post("/predict/tabular/RandomForestClassifier", json=payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Model not found"


@pytest.mark.parametrize(
    ["sample", "expected"],
    [read_image(image_path) for image_path in TEST_DATA_DIR.glob("*.JPEG")],
)
def test_classify_image(client, sample, expected):
    response = client.post(
        "/predict/image",
        files={
            "file": (
                "image.jpg",
                cv2.imencode(".jpg", sample)[1].tobytes(),
                "image/jpeg",
            )
        },
        timeout=30,
    )

    json = response.json()
    assert response.status_code == 200
    assert json["message"] == "OK"
    assert json["status-code"] == 200
    assert json["data"]["predicted_class"] == expected
