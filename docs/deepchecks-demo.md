# Deepchecks demo <!-- omit in toc -->
In this demo we will see the main features of [Deepchecks](https://deepchecks.com/) to validate the data of a simple computer vision project.

## Contents <!-- omit in toc -->
- [Install Deepchecks for computer vision](#install-deepchecks-for-computer-vision)
- [Create a data validation script](#create-a-data-validation-script)
  - [Loading the data](#loading-the-data)
  - [Create the validation suite](#create-the-validation-suite)
  - [Run the suite and save the results](#run-the-suite-and-save-the-results)


## Install Deepchecks for computer vision
The first step is to install Deepchecks. To do this, we can run the following command:
```bash
poetry add deepchecks[vision]
```

## Create a data validation script
The next step is to create a data validation script. To do this, we create a file called
[`deepchecks_validation.py`](../src/features/deepchecks_validation.py) in the `src/features` folder.

In this script we will validate that our processed data meets a set of requirements. Specifically, rely on pre-defined
suites to check the data integrity and ensure the correct split of the data.

### Loading the data
Deepchecks provides the built-in function `classification_dataset_from_directory` to load data from a structured directory.
We can use this function to load the data into a `VisionData` object. Note that this function requires the `torchvision` package.

```python
from deepchecks.vision import classification_dataset_from_directory

from src.config import PROCESSED_DATA_DIR

train_ds, test_ds = classification_dataset_from_directory(
    PROCESSED_DATA_DIR / 'euroSAT', object_type="VisionData", image_extension="jpg"
)
```
If you want to use a different structure, you can use the `VisionData` class to load the data manually.
See the [Deepchecks documentation](https://docs.deepchecks.com/stable/vision/usage_guides/visiondata_object.html) for more information.

### Create the validation suite
Deepchecks provides a set of pre-defined suites that can be used as a starting point for validating the data.
In this case, we will create our own suite by combining the `data_integrity` and `train_test_validation` suites.

```python
from deepchecks.vision.suites import data_integrity, train_test_validation

custom_suite = data_integrity()

custom_suite.add(
    train_test_validation()
)
```

Notice how we can easily add a validation suite to another suite using the `add` method.

In case you want to add additional checks, you just need to add them to the suite using the `add` method.
For more information on how to add and customize checks, see the [Deepchecks documentation](https://docs.deepchecks.com/stable/general/usage/customizations/auto_examples/index.html).

### Run the suite and save the results
Finally, we can run the validation by calling the `run` method on the suite. Then, we can save the results as an HTML report.

```python
result = custom_suite.run(train_ds, test_ds)

result.save_as_html(str(REPORTS_DIR / "deepchecks_validation.html"))
```