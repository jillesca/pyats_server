FROM python:3.9-slim

ARG PYATS_SERVER_PORT=57000

ENV PYATS_SERVER_PORT=${PYATS_SERVER_PORT}

WORKDIR /app

COPY . .

RUN apt-get update \
    && apt-get install -y openssh-server \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PYATS_SERVER_PORT}"]
