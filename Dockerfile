FROM python:3.14.0a7-bookworm

RUN pip install poetry

WORKDIR /app
