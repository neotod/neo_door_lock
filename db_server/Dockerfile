FROM python:3.8-buster

COPY ./requirements.txt /db_server/requirements.txt
WORKDIR /db_server

RUN pip install -r requirements.txt

COPY . /db_server

ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:80", "-w", "2", "run:app" ]