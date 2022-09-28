FROM python:3.9-alpine
LABEL maintainer="kowe.io"

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./api /api
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /env && \
    /env/bin/pip install --upgrade pip && \
    /env/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = 'true' ]; \
        then /env/bin/pip install -r /tmp/requirements.dev.txt; \
    fi &&\
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/env/bin:$PATH"
USER django-user