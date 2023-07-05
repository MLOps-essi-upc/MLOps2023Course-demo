# MLflow demo for the MLOps 2023-24 course
In this demo we will see the main features of [MLflow](https://mlflow.org/) to track the experiments of a simple machine
learning project.

## Install MLflow
First, we need to install MLflow. We can do this by running the following command:

### Using poetry
```bash
poetry add mlflow
```

### Using pdm
```bash
pdm add mlflow
```

### Using pipenv
```bash
pipenv install mlflow
```

### Using pip
```bash
pip install mlflow
```

## Configure a tracking server
By default MLflow stores the tracking data locally in an `mlruns` subdirectory of where you ran the code. However, we
can configure MLflow to use a shared storage in a remote server.

In this demo we will use Dagshub  as it provides an easy
way to configure a tracking server. To do this, we first need to create a repository in Dagshub or to link our GitHub
repository to Dagshub. Then, we can easily configure MLflow to use Dagshub as its tracking server by setting the environment
valiables shown in the Dagshub repository.

<p align="center">
    <img src="static/dagshub-mlflow-config.png" width="700" alt="Dagshub MLflow configuration">
</p>

To add the environment variables to our project we can use a `.env` file the following content:

```bash
MLFLOW_TRACKING_URI=https://dagshub.com/<DagsHub-user-name>/<reposytory-name>.mlflow
MLFLOW_TRACKING_USERNAME=your_username
MLFLOW_TRACKING_PASSWORD=your_token
```

Then, we can load the environment variables adding the following code to our `__init__.py` file:

```python
from dotenv import load_dotenv

load_dotenv()
```

**Remember to include the `.env` file in the `.gitignore` file to avoid committing your credentials to the repository.**

## Add MLflow tracking to the code
MLflow comes with automatic logging APIs for several machine learning frameworks. In these cases, we can use the
[`mlflow.<framework>.autolog()`](https://mlflow.org/docs/latest/tracking.html#automatic-logging) function to automatically
log the parameters, metrics, and model artifacts from our machine learning code.

> **Note:** Autologging is only supported for certain versions of the frameworks. If you are using the latest version of
some of these frameworks you might get some errors. See the [MLflow documentation](https://mlflow.org/docs/latest/tracking.html#automatic-logging) for more details.




