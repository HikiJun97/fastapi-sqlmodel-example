FROM python:3.11.8-slim-bookworm as build

RUN apt-get update

RUN apt-get upgrade -y

COPY requirements.txt /workspace/requirements.txt

RUN pip install -r /workspace/requirements.txt

COPY app /workspace/app

WORKDIR /workspace

ENV DB_HOST="host.docker.internal"

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
