FROM python:3.13

RUN apt update && \
    apt upgrade -y && \
    pip install poetry

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y 

WORKDIR /app
