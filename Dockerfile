FROM python:3.12-slim-bookworm as build

RUN apt-get update

RUN apt-get upgrade -y

COPY requirements.txt /workspace/requirements.txt

RUN pip install -r /workspace/requirements.txt

COPY app /workspace/app

WORKDIR /workspace/app

ENV DB_HOST="host.docker.internal"

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
