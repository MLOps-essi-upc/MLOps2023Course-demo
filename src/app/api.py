"""Main script: it includes our API initialization and endpoints."""

from contextlib import asynccontextmanager
import pickle
from datetime import datetime
from functools import wraps
from http import HTTPStatus
from typing import List

from fastapi import FastAPI, HTTPException, Request
from codecarbon import track_emissions

from src.config import METRICS_DIR, MODELS_DIR
from src.app.schemas import IrisType, PredictPayload

model_wrappers_list: List[dict] = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Loads all pickled models found in `MODELS_DIR` and adds them to `models_list`"""

    model_paths = [
        filename
        for filename in MODELS_DIR.iterdir()
        if filename.suffix == ".pkl" and filename.stem.startswith("iris")
    ]

    for path in model_paths:
        with open(path, "rb") as file:
            model_wrapper = pickle.load(file)
            model_wrappers_list.append(model_wrapper)

    yield

    # Clear the list of models to avoid memory leaks
    model_wrappers_list.clear()


# Define application
app = FastAPI(
    title="Yet another Iris example",
    description="This API lets you make predictions on the Iris dataset using a couple of simple models.",
    version="0.1",
    lifespan=lifespan,
)


@app.get("/", tags=["General"])  # path operation decorator
async def _index():
    """Root endpoint."""

    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {"message": "Welcome to IRIS classifier! Please, read the `/docs`!"},
    }
    return response


@app.get("/models", tags=["Prediction"])
def _get_models_list(model_type: str | None = None):
    """Return the list of available models"""

    available_models = [
        {
            "type": model["type"],
            "parameters": model["params"],
            "accuracy": model["metrics"],
        }
        for model in model_wrappers_list
        if model["type"] == model_type or model_type is None
    ]

    if not available_models and model_type is not None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Type not found")

    return {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": available_models,
    }


@app.post("/models/{model_type}", tags=["Prediction"])
@track_emissions(
    project_name="iris-prediction",
    measure_power_secs=1,
    save_to_file=True,
    output_dir=METRICS_DIR,
)
def _predict(model_type: str, payload: PredictPayload):
    """Classifies Iris flowers based on sepal and petal sizes."""

    # sklearn's `predict()` methods expect a 2D array of shape [n_samples, n_features]
    # therefore, we need to convert our single data point into a 2D array
    features = [
        [
            payload.sepal_length,
            payload.sepal_width,
            payload.petal_length,
            payload.petal_width,
        ]
    ]

    model_wrapper = next(
        (m for m in model_wrappers_list if m["type"] == model_type), None
    )

    if model_wrapper:
        prediction = model_wrapper["model"].predict(features)
        prediction = int(prediction[0])
        predicted_type = IrisType(prediction).name

        response = {
            "message": HTTPStatus.OK.phrase,
            "status-code": HTTPStatus.OK,
            "data": {
                "model-type": model_wrapper["type"],
                "features": {
                    "sepal_length": payload.sepal_length,
                    "sepal_width": payload.sepal_width,
                    "petal_length": payload.petal_length,
                    "petal_width": payload.petal_width,
                },
                "prediction": prediction,
                "predicted_type": predicted_type,
            },
        }
    else:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Model not found"
        )
    return response
