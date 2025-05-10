FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN apt-get update && apt-get install libpq-dev python3-dev -y

COPY ./app /app

ENV PYTHONPATH=/app
