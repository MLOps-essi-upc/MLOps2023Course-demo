import pickle
from pathlib import Path

import mlflow
import pandas as pd
import yaml
from codecarbon import EmissionsTracker
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor

from src.config import METRICS_DIR, MODELS_DIR, PROCESSED_DATA_DIR

mlflow.set_experiment("iowa-house-prices")
mlflow.sklearn.autolog(log_model_signatures=False, log_datasets=False)

with mlflow.start_run():
    # Path of the parameters file
    params_path = Path("params.yaml")

    # Path of the prepared data folder
    input_folder_path = PROCESSED_DATA_DIR

    # Read training dataset
    X_train = pd.read_csv(input_folder_path / "X_train.csv")
    y_train = pd.read_csv(input_folder_path / "y_train.csv")

    # Read data preparation parameters
    with open(params_path, "r", encoding="utf8") as params_file:
        try:
            params = yaml.safe_load(params_file)
            params = params["train"]
        except yaml.YAMLError as exc:
            print(exc)

    # ============== #
    # MODEL TRAINING #
    # ============== #

    # Specify the model
    if params["algorithm"] == "DecisionTreeRegressor":
        algorithm = DecisionTreeRegressor
    elif params["algorithm"] == "RandomForestRegressor":
        algorithm = RandomForestRegressor

    # For the sake of reproducibility, set the `random_state`
    iowa_model = algorithm(random_state=params["random_state"])

    # Track the CO2 emissions of training the model
    emissions_output_folder = METRICS_DIR
    with EmissionsTracker(
        project_name="iowa-house-prices",
        measure_power_secs=1,
        tracking_mode="process",
        output_dir=emissions_output_folder,
        output_file="emissions.csv",
        on_csv_write="append",
        default_cpu_power=45,
    ):
        # Then fit the model to the training data
        iowa_model.fit(X_train, y_train)

    # Log the CO2 emissions to MLflow
    emissions = pd.read_csv(emissions_output_folder / "emissions.csv")
    emissions_metrics = emissions.iloc[-1, 4:13].to_dict()
    emissions_params = emissions.iloc[-1, 13:].to_dict()
    mlflow.log_params(emissions_params)
    mlflow.log_metrics(emissions_metrics)

    # Save the model as a pickle file
    Path("models").mkdir(exist_ok=True)

    with open(MODELS_DIR / "iowa_model.pkl", "wb") as pickle_file:
        pickle.dump(iowa_model, pickle_file)
