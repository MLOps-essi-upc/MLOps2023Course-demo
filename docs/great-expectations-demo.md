# Great Expectations demo<!-- omit in toc -->
In this demo we will see the main features of [Great Expectations](https://greatexpectations.io/) to validate data.

## Contents <!-- omit in toc -->
- [Install Great Expectations](#install-great-expectations)
- [Create a data validation script](#create-a-data-validation-script)
  - [Get the data context](#get-the-data-context)
  - [Create an Expectation Suite](#create-an-expectation-suite)
  - [Add a Pandas datasource to our context](#add-a-pandas-datasource-to-our-context)
  - [Create a validator and configure the expectations](#create-a-validator-and-configure-the-expectations)
  - [Create a checkpoint and run the validation](#create-a-checkpoint-and-run-the-validation)
- [Persistence](#persistence)

## Install Great Expectations
The first step is to install Great Expectations. To do this, we can run the following command:
```bash
poetry add great_expectations
```

## Create a data validation script
The next step is to create a data validation script. To do this, we create a file called
[`validate.py`](../src/features/validate.py) in the `src/features` folder.

In this script we will validate that our processed data meets a set of requirements. Specifically, we will check that:
- The number of rows is greater than 0.
- The columns are the expected ones.
- There are no null values in the labels.
- The labels are in the expected range.
- The IDs are unique and not null.
- The features have the expected data type.

### Get the data context
To do this, we first need to get the DataContext object. This object is the main entry point for interacting with Great
Expectations. It is used to configure datasources, stores, and actions. It also provides access to the suite of methods
for validating data.

```python
import great_expectations as gx

context = gx.get_context()
```

### Create an Expectation Suite
Next, we need to create a new Expectation Suite. An Expectation Suite is a collection of Expectations that can be saved
and reused across multiple batches of data. It is a container for Expectations and stores metadata about the Expectations,
such as a name, a description, and the batch of data the Expectations were computed on.

```python
context.add_or_update_expectation_suite("iowa_training_suite")
```

### Add a Pandas datasource to our context
Now, we create a datasource. A datasource is a configuration object that defines how to connect to a data store. It is
used to create batches of data for validation. In this case, we will use a PandasDatasource, which is a datasource that
connects to a Pandas DataFrame.

```python
datasource = context.sources.add_or_update_pandas(name="iowa_dataset")
```

Next, we need to add the dataframe to the datasource. To do this, we first load the data into a Pandas DataFrame and
then add it to the datasource.

```python
x_train = pd.read_csv(PROCESSED_DATA_DIR / "X_train.csv")
y_train = pd.read_csv(PROCESSED_DATA_DIR / "y_train.csv")

train = pd.concat([x_train, y_train], axis=1)

data_asset = datasource.add_dataframe_asset(name="training", dataframe=train)
```

### Create a validator and configure the expectations
Now, we can request a validator from the context. Validators are responsible for running an expectations suite against
data. To do this, we need to specify the name of the Expectation Suite and the batch request.

```python
batch_request = data_asset.build_batch_request()
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name="iowa_training_suite",
    datasource_name="iowa_dataset",
    data_asset_name="training",
)
```

Once we have our validator, we can start adding expectations to it. For a complete list of expectations, see the
[Great Expectations page](https://greatexpectations.io/expectations/).

```python
validator.expect_table_columns_to_match_ordered_list(
    column_list=[
        "MSSubClass",
        ...
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
```

Now that we have all our expectations, we can tell the validator to save the Expectation Suite for future use.

```python
validator.save_expectation_suite(discard_failed_expectations=False)
```

### Create a checkpoint and run the validation
Finally, we create a checkpoint that will use our validator to run the expectation suite against the batch request and
compile a Data Docs where we can easely see the results of the validation process.

```python
checkpoint = context.add_or_update_checkpoint(
    name="my_checkpoint",
    validator=validator,
)

checkpoint_result = checkpoint.run()
context.view_validation_result(checkpoint_result)
```

## Persistence
By default, Great Expectations uses ephemeral data contexts which don't persist beyond the current Python session. If you want to persist your data context you will need a Filesystem Data Context or other persisting contexts. To create a Filesystem Data Context, you can run the following command:

```bash
great_expectations init
```

This will create a `great_expectations` folder in your project. Inside this folder, you will find a `great_expectations.yml` file. This file contains the configuration for your data context. You can modify this file to change the configuration of your data context.

Once Great Expectations detects a `great_expectations.yml` file in your project, it will automatically use it to configure the data context.

For more information on how to configure your data context, see the [Great Expectations documentation](https://docs.greatexpectations.io/docs/guides/setup/configure_data_contexts_lp).
