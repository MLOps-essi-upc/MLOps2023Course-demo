# Pytest demo <!-- omit in toc -->
In this demo we will see the main features of [Pytest](https://docs.pytest.org/en/latest/) to test a simple machine
learning project.

## Contents <!-- omit in toc -->
- [Install Pytest](#install-pytest)
- [Create the test file](#create-the-test-file)
- [Run the tests](#run-the-tests)

## Install Pytest
The first step is to install `pytest` and `pytest-cov` to measure the code coverage. To do this, we can run the
following command:
```bash
poetry add -G dev pytest pytest-cov
```

## Create the test file
We can now create a test file called [`test_models.py`](../tests/test_models.py) in the `tests` directory. In this file,
we will create a test to check that the `predict` function of a Logistic Regression model trained on the Iris dataset
returns the expected value.

To do this, we will create a fixture called `lr_model` that will load the model from the `models` directory. Then, we
will create a test function called `test_iris_lr_model` that will use the `model` fixture to load the model and check
that the prediction is correct.

In this case, we want to test the model for multiple inputs. To do this, we will use the `pytest.mark.parametrize`
decorator to parametrize the test function. This decorator receives the names of the parameters and a list of values.

Finally, we will add the following lines to the [`pyproject.toml`](../pyproject.toml) file to measure the code coverage:
```toml
[tool.coverage.run]
omit = ["src/prepare.py", "src/evaluate.py", "src/train.py", "src/train_api_demo_models.py"]

[tool.pytest.ini_options]
testpaths = "tests"
addopts = "--junitxml=out/tests-report.xml --cov=src --cov-report=html:out/coverage"
```

In detail:
- `omit` specifies the files that should be omitted from the coverage report;
- `testpaths` specifies the directory where the tests are located;
- `addopts` specifies the options to pass to `pytest`. In this case, we are specifying the path to the results file that
- can be read by continuous integration tools, the path to the module for the coverage report and the directory where
- the coverage report should be saved.

## Run the tests
We can now run the tests using the following command:
```bash
PYTHONPATH=. python3 -m pytest
```
