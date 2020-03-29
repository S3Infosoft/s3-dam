FROM python:3.7-slim-buster
MAINTAINER S3-Infosoft

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt && rm -rf /root/.cache/pip/

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser --disabled-password --gecos "" user
USER user
