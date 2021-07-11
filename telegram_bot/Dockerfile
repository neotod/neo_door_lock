FROM python:3.8-buster

COPY ./requirements.txt /bot/requirements.txt
WORKDIR /bot

RUN pip install -r requirements.txt

RUN ln -sf /usr/share/zoneinfo/Asia/Tehran /etc/localtime
RUN date

COPY . /bot

ENTRYPOINT [ "python", "bot.py" ]