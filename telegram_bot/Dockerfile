FROM python:latest

COPY ./requirements.txt /bot/requirements.txt
WORKDIR /bot

RUN pip install -r requirements.txt

COPY . /bot

ENTRYPOINT [ "python", "bot.py" ]