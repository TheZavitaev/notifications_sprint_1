FROM python:3.9.1-slim

ENV PYTHONUNBUFFERED 1

ARG ROOT_APP=/app/

RUN
    mkdir -p $ROOT_APP/static && \
    mkdir $ROOT_APP/media

COPY admin/requirements.txt $ROOT_APP/requirements.txt

WORKDIR $ROOT_APP

RUN pip install -r requirements.txt

COPY admin/entrypoint.sh $ROOT_APP/entrypoint.sh
COPY admin/gunicorn.conf.py $ROOT_APP/gunicorn.conf.py
COPY admin/src $ROOT_APP

RUN chmod +x entrypoint.sh

ENTRYPOINT ['./entrypoint.sh']