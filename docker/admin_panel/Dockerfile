FROM python:3.10

RUN apt-get update && apt-get install -y netcat

ENV PYTHONUNBUFFERED=1

COPY ./docker/admin_panel/requirements.txt .
COPY ./docker/common-requirements.txt .

RUN /usr/local/bin/python -m pip install --upgrade pip && pip install -r requirements.txt -r common-requirements.txt

COPY ./admin_panel ./app

WORKDIR ./app

COPY ./docker/admin_panel/docker-entrypoint.sh ./docker-entrypoint.sh

RUN chmod +x ./docker-entrypoint.sh

ENTRYPOINT [ "./docker-entrypoint.sh" ]
