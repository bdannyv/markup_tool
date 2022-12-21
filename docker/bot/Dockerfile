FROM python:3.10

ENV PYTHONUNBUFFERED=1

COPY ./docker/bot/requirements.txt .
COPY ./docker/common-requirements.txt .

RUN /usr/local/bin/python -m pip install --upgrade pip && pip install -r requirements.txt -r common-requirements.txt

COPY ./bot ./app

WORKDIR ./app

CMD python main.py
