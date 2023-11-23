from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from src.app.api import app


@pytest.fixture(scope="module", autouse=True)
def client():
    # Use the TestClient with a `with` statement to trigger the startup and shutdown events.
    with TestClient(app) as client:
        return client


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
    assert json["method"] == "GET"
    assert json["url"] == "http://testserver/"
    assert json["timestamp"] is not None


def test_get_all_models(client):
    response = client.get("/models")
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
    assert json["method"] == "GET"
    assert json["url"] == "http://testserver/models"
    assert json["timestamp"] is not None


def test_get_one_model(client):
    response = client.get("/models?type=SVC")
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
    assert json["method"] == "GET"
    assert json["url"] == "http://testserver/models?type=SVC"
    assert json["timestamp"] is not None


def test_get_one_model_not_found(client):
    response = client.get("/models?type=RandomForestClassifier")
    assert response.status_code == 400
    assert response.json()["detail"] == "Type not found"


def test_model_prediction(client, payload):
    response = client.post("/models/LogisticRegression", json=payload)
    json = response.json()
    assert response.status_code == 200
    assert json["data"]["prediction"] == 2
    assert json["message"] == "OK"
    assert json["status-code"] == 200
    assert json["method"] == "POST"
    assert json["url"] == "http://testserver/models/LogisticRegression"
    assert json["timestamp"] is not None


def test_model_prediction_not_found(client, payload):
    response = client.post("/models/RandomForestClassifier", json=payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Model not found"
