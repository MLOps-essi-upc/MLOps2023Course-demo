from sklearn.metrics import mean_absolute_error, mean_squared_error
import pickle
import json
import pandas as pd
from pathlib import Path


# Path to the prepared data folder
input_folder_path = Path("data/processed")

# Path to the models folder
model_folder_path = Path("models")

# Path to the metrics folder
Path("metrics").mkdir(exist_ok=True)
metrics_folder_path = Path("metrics")

# Read validation dataset
X_valid = pd.read_csv(input_folder_path / "X_valid.csv")
y_valid = pd.read_csv(input_folder_path / "y_valid.csv")


# ================ #
# MODEL EVALUATION #
# ================ #

# Load the model
with open(model_folder_path / "iowa_model.pkl", "rb") as pickled_model:
    iowa_model = pickle.load(pickled_model)

# Compute predictions using the model
val_predictions = iowa_model.predict(X_valid)

# Compute the MAE value for the model
val_mae = mean_absolute_error(y_valid, val_predictions)
val_mean_squared_error = mean_squared_error(y_valid, val_predictions)

# Write MAE to file
with open(metrics_folder_path / "scores.json", "w") as scores_file:
    json.dump(
        {"mae": val_mae, "mean_squared_error": val_mean_squared_error},
        scores_file,
        indent=4,
    )

print("Evaluation completed.")
