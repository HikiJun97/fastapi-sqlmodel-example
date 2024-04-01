FROM python:3.11.8-slim-bookworm as build

RUN apt-get update && apt-get upgrade

COPY requirements.txt /workspace/requirements.txt

RUN pip install -r /workspace/requirements.txt

COPY app /workspace

WORKDIR /workspace

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
