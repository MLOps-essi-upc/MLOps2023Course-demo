"""Definitions for the objects used by our resource endpoints."""

from enum import Enum

from pydantic import BaseModel


class IrisPredictionPayload(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

    model_config: dict = {
        "json_schema_extra": {
            "example": {
                "sepal_length": 6.4,
                "sepal_width": 2.8,
                "petal_length": 5.6,
                "petal_width": 2.1,
            }
        }
    }


class IrisType(Enum):
    SETOSA = 0
    VERSICOLOR = 1
    VIRGINICA = 2
