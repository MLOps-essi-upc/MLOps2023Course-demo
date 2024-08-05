import pandas as pd

import great_expectations as gx
from src.config import PROCESSED_DATA_DIR

# We import the existing DataContext
context = gx.get_context()

# We load our training data and create a pandas datasource with it
datasource = context.sources.add_or_update_pandas(name="iowa_dataset")

x_train = pd.read_csv(PROCESSED_DATA_DIR / "X_train.csv")
y_train = pd.read_csv(PROCESSED_DATA_DIR / "y_train.csv")

train = pd.concat([x_train, y_train], axis=1)

data_asset = datasource.add_dataframe_asset(name="training", dataframe=train)
batch_request = data_asset.build_batch_request()

# We create an expectation suite for our training data
context.add_or_update_expectation_suite("iowa_training_suite")

# Now, we can validate our training data defining some expectations
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name="iowa_training_suite",
    datasource_name="iowa_dataset",
    data_asset_name="training",
)

validator.expect_table_columns_to_match_ordered_list(
    column_list=[
        "MSSubClass",
        "LotFrontage",
        "LotArea",
        "OverallQual",
        "OverallCond",
        "YearBuilt",
        "YearRemodAdd",
        "MasVnrArea",
        "BsmtFinSF1",
        "BsmtFinSF2",
        "BsmtUnfSF",
        "TotalBsmtSF",
        "1stFlrSF",
        "2ndFlrSF",
        "LowQualFinSF",
        "GrLivArea",
        "BsmtFullBath",
        "BsmtHalfBath",
        "FullBath",
        "HalfBath",
        "BedroomAbvGr",
        "KitchenAbvGr",
        "TotRmsAbvGrd",
        "Fireplaces",
        "GarageYrBlt",
        "GarageCars",
        "GarageArea",
        "WoodDeckSF",
        "OpenPorchSF",
        "EnclosedPorch",
        "3SsnPorch",
        "ScreenPorch",
        "PoolArea",
        "MiscVal",
        "MoSold",
        "YrSold",
        "Id",
        "SalePrice",
    ]
)

validator.expect_column_values_to_be_unique("Id")
validator.expect_column_values_to_not_be_null("Id")
validator.expect_column_values_to_be_of_type("Id", "int64")

validator.expect_column_values_to_be_between("MSSubClass", auto=True)
validator.expect_column_values_to_be_of_type("MSSubClass", "float64")

validator.expect_column_values_to_not_be_null("SalePrice")
validator.expect_column_values_to_be_between("SalePrice", min_value=0)
validator.expect_column_values_to_be_of_type("SalePrice", "int64")

# We save our expectations in the expectation suite
validator.save_expectation_suite(discard_failed_expectations=False)

# We create a checkpoint to run our expectations and compile the results as Data Docs
checkpoint = context.add_or_update_checkpoint(
    name="my_checkpoint",
    validator=validator,
)

# Finally, we run our checkpoint and view the results on the browser
checkpoint_result = checkpoint.run()

context.build_data_docs()
# context.open_data_docs()
