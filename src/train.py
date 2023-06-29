import pandas as pd
import pickle
import yaml
from pathlib import Path
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer


# Path of the parameters file
params_path = Path("params.yaml")

# Path of the prepared data folder
input_folder_path = Path("data/processed")

# Read training dataset
X_train = pd.read_csv(input_folder_path / "X_train.csv")
y_train = pd.read_csv(input_folder_path / "y_train.csv")

# Read data preparation parameters
with open(params_path, "r") as params_file:
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

# For the sake of reproducibility, I set the `random_state`
iowa_model = algorithm(random_state=params["random_state"])

# Then I fit the model to the training data
iowa_model.fit(X_train, y_train)

# Eventually I save the model as a pickle file
Path("models").mkdir(exist_ok=True)
output_folder_path = Path("models")

with open(output_folder_path / "iowa_model.pkl", "wb") as pickle_file:
    pickle.dump(iowa_model, pickle_file)
