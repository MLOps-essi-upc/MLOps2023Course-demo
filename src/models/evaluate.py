import json
import pickle
from pathlib import Path

import mlflow
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

from src import METRICS_DIR, PROCESSED_DATA_DIR

# Path to the prepared data folder
input_folder_path = PROCESSED_DATA_DIR

# Path to the models folder
model_folder_path = Path("models")

# Path to the metrics folder
Path("metrics").mkdir(exist_ok=True)
metrics_folder_path = METRICS_DIR

# Read validation dataset
X_valid = pd.read_csv(input_folder_path / "X_valid.csv")
y_valid = pd.read_csv(input_folder_path / "y_valid.csv")

# ================ #
# MODEL EVALUATION #
# ================ #
mlflow.set_experiment("iowa-house-prices")

with mlflow.start_run():
    # Load the model
    with open(model_folder_path / "iowa_model.pkl", "rb") as pickled_model:
        iowa_model = pickle.load(pickled_model)

    # Compute predictions using the model
    val_predictions = iowa_model.predict(X_valid)

    # Compute the MAE and MSE values for the model
    val_mae = mean_absolute_error(y_valid, val_predictions)
    val_mean_squared_error = mean_squared_error(y_valid, val_predictions)

    # Save the evaluation metrics to a dictionary to be reused later
    metrics_dict = {"mae": val_mae, "mean_squared_error": val_mean_squared_error}

    # Log the evaluation metrics to MLflow
    mlflow.log_metrics(metrics_dict)

    # Save the evaluation metrics to a JSON file
    with open(metrics_folder_path / "scores.json", "w") as scores_file:
        json.dump(
            metrics_dict,
            scores_file,
            indent=4,
        )

    print("Evaluation completed.")
