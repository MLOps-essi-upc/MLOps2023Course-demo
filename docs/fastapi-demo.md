# FastAPI demo for the MLOps 2023-24 course <!-- omit in toc -->
In this demo we will see the main features of [FastAPI](https://fastapi.tiangolo.com/) to create an API for a simple
machine learning project.

The scrips used in this project are based on the [SE4AI2021Course_FastAPI-demo](https://github.com/se4ai2122-cs-uniba/SE4AI2021Course_FastAPI-demo) GitHub project.

## Contents <!-- omit in toc -->
- [Install FastAPI](#install-fastapi)
- [Start the server](#start-the-server)
- [Try the API](#try-the-api)
  - [Access the API documentation](#access-the-api-documentation)
  - [Try some requests](#try-some-requests)


## Install FastAPI
The first step is to install FastAPI and Uvicorn, which is a fast ASGI server (it can run asynchronous code in a single
process) to launch our application. To do this, we can run the following command:

### Using poetry <!-- omit in toc -->
```bash
poetry add fastapi "uvicorn[standard]"
```

### Using pdm <!-- omit in toc -->
```bash
pdm add fastapi "uvicorn[standard]"
```

### Using pipenv <!-- omit in toc -->

```bash
pipenv install fastapi "uvicorn[standard]"
```

### Using pip <!-- omit in toc -->
```bash
pip install fastapi "uvicorn[standard]"
```

## Start the server
Use the following command to start the server:

```bash
uvicorn src.app.api:app \
    --host 0.0.0.0 \
    --port 5000 \
    --reload \
    --reload-dir src/app \
    --reload-dir models
```
In detail:

- `uvicorn src.app.api:app` is the location of app (`src` directory > `app` directory > `api.py` script > `app` object);
- `--reload` makes the server reload every time we update;
- `--reload-dir app` makes it only reload on updates to the `app/` directory;
- `--reload-dir models` makes it also reload on updates to the `models/` directory;

## Try the API
We can now test that the application is working. These are some of the possibilities:

- Visit [localhost:5000](http://localhost:5000/)
- Use `curl`

  ```bash
  curl -X GET http://localhost:5000/
  ```

- Access the API programmatically, e.g.:

  ```python
  import json
  import requests

  response = requests.get("http://localhost:5000/")
  print (json.loads(response.text))
  ```

- Use an external tool like [Postman](https://www.postman.com), which lets you execute and manage tests that can be 
saved and shared with others.

### Access the API documentation
You can access the [Swagger UI](https://swagger.io/tools/swagger-ui/) in http://localhost:5000/docs for documentation
endpoint and select one of the models. The documentation generated via [Redoc](https://github.com/Redocly/redoc) is
accessible at the `/redoc` endpoint.


<center><figure>
  <img
  src="static/deployment/api/01_api_ui.png"
</figure></center>
<p style="text-align: center;">API User Interface in localhost:5000/docs endpoint.</p>

### Try some requests
To try an API request, click on the "Try it out" button and click execute.

For example:
#### Virginica (2) <!-- omit in toc -->

```json
{
  "sepal_length": 6.4,
  "sepal_width": 2.8,
  "petal_length": 5.6,
  "petal_width": 2.1
}
```

#### Setosa (0) <!-- omit in toc -->

```json
{
  "sepal_length": 5.7,
  "sepal_width": 3.8,
  "petal_length": 1.7,
  "petal_width": 0.3
}
```
