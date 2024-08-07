# Docker demo<!-- omit in toc -->
In this demo we will see how to create a Docker container and run our FastAPI app on it.

## Contents <!-- omit in toc -->
- [Install docker](#install-docker)
- [Create a Dockerfile](#create-a-dockerfile)
- [Build your docker image](#build-your-docker-image)
- [Run your Docker container:](#run-your-docker-container)
- [Try the API](#try-the-api)

## Install docker
Verify you have installed docker or follow this guide:

https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository

Verify your installation is ok:

```bash
sudo docker run hello-world
```

## Create a Dockerfile
Create a Dockerfile in the same directory as your app.py file:

Example:
```Dockerfile
FROM python:3.10
ENV PYTHONUNBUFFERED 1
EXPOSE 8000
WORKDIR /app
COPY ./requirements.txt .
COPY . /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app.api_code:app"]
```

## Build your docker image

```bash
docker build -t my-docker-fastapi .
```

## Run your Docker container:
```bash
docker run -d -p 8000:8000 --name my-container my-docker-fastapi
```
This command starts a Docker container named my-container and maps port 8000 on your local machine to port 8000 in the container.

## Try the API
See [fastapi-demo](./fastapi-demo.md/)
