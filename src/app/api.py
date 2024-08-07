"""Main script: it includes our API initialization and endpoints."""

import logging
import pickle
from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import Dict

import tensorflow as tf
import tensorflow_hub as hub
from codecarbon import track_emissions
from fastapi import FastAPI, HTTPException, UploadFile

from src.app.schemas import IrisPredictionPayload, IrisType
from src.config import METRICS_DIR, MODELS_DIR

# Initialize the dictionary to group models by "tabular" or "image" and then by model type
model_wrappers_dict: Dict[str, Dict[str, dict]] = {"tabular": {}, "image": {}}


def file_to_image(file: bytes):
    """
    Reads an image file and formats it for the model.

    Parameters
    ----------
    file:
        bytes: The image file to classify.

    Returns
    -------
    Tensor: The image formatted for the model.
    """
    image = tf.io.decode_image(file, channels=3, dtype=tf.float32)
    return tf.image.resize(image, [224, 224])


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
            model_wrappers_dict["tabular"][model_wrapper["type"]] = model_wrapper

    cv_model = hub.KerasLayer(
        "https://www.kaggle.com/models/google/mobilenet-v3/TensorFlow2/small-075-224-classification/1"
    )
    model_wrappers_dict["image"]["mobilenet_v3"] = {
        "model": cv_model,
        "type": "mobilenet_v3",
    }

    yield

    # Clear the list of models to avoid memory leaks
    del model_wrappers_dict["tabular"]
    del model_wrappers_dict["image"]


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


@app.get("/models/tabular", tags=["Prediction"])
def _get_tabular_models_list(model_type: str | None = None):
    """Return the list of available models"""

    if model_type is not None:
        model = model_wrappers_dict["tabular"].get(model_type, None)
        if model is None:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Type not found"
            )
        available_models = [
            {
                "type": model["type"],
                "parameters": model["params"],
                "accuracy": model["metrics"],
            }
        ]
    else:
        available_models = [
            {
                "type": model["type"],
                "parameters": model["params"],
                "accuracy": model["metrics"],
            }
            for model in model_wrappers_dict["tabular"].values()
        ]

    return {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": available_models,
    }


@app.post("/predict/tabular/{model_type}", tags=["Prediction"])
@track_emissions(
    project_name="iris-prediction",
    measure_power_secs=1,
    save_to_file=True,
    output_dir=METRICS_DIR,
)
def _predict_tabular(model_type: str, payload: IrisPredictionPayload):
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

    model_wrapper = model_wrappers_dict["tabular"].get(model_type, None)

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


# Create and endpoint to classify an image
@track_emissions(
    project_name="cats-and-dogs-prediction",
    measure_power_secs=1,
    save_to_file=True,
    output_dir=METRICS_DIR,
)
@app.post("/predict/image/", tags=["Prediction"])
async def _predict_image(file: UploadFile):
    """
    Classifies ImageNet images using a pre-trained MobileNetV3 model.

    Parameters
    ----------
    file : UploadFile
        The image to classify.
    """
    # Read the image file and format it for the model
    image_stream = await file.read()
    image = file_to_image(image_stream)
    await file.close()

    cv_model = model_wrappers_dict["image"]["mobilenet_v3"]["model"]
    predictions = cv_model(tf.expand_dims(image, axis=0))
    predicted_label = tf.keras.applications.mobilenet_v3.decode_predictions(
        predictions[:, 1:], top=1
    )[0][0][1]

    logging.info("Predicted class %s", predicted_label)

    response = {
        "message": HTTPStatus.OK.phrase,
        "status-code": HTTPStatus.OK,
        "data": {
            "model-type": "mobilenet_v3",
            "prediction": predictions,
            "predicted_class": predicted_label,
        },
    }

    return response
