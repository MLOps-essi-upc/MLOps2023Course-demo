# CodeCarbon Demo
In this demo we will see the main features of [CodeCarbon](https://mlco2.github.io/codecarbon/index.html), a Python package
to track the carbon emissions of machine learning projects.

## Install CodeCarbon
First, we need to install CodeCarbon. We can do this by running the following command:

### Using poetry
```bash
poetry add codecarbon
```

### Using pdm
```bash
pdm add codecarbon
```

### Using pipenv
```bash
pipenv install codecarbon
```

### Using pip
```bash
pip install codecarbon
```

## Tracking emissions
There are three ways to track the emissions of a machine learning project with CodeCarbon:

### Using the `EmissionsTracker` class
```python
from codecarbon import EmissionsTracker

tracker = EmissionsTracker()
tracker.start()
# Your training code here
tracker.stop()
```

### Using the `EmissionsTracker` context manager
```python
from codecarbon import EmissionsTracker

with EmissionsTracker() as tracker:
    # Your training code here
```

### Using the `track_emissions` decorator
```python
from codecarbon import track_emissions

@track_emissions
def training_function():
    # Your training code here
```


For an example on how to use CodeCarbon and log the emissions to MLflow, see the [`train.py`](../src/train.py) file.

For more information on each of these methods and their parameters, see the [CodeCarbon documentation](https://mlco2.github.io/codecarbon/usage.html)
