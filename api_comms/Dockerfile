FROM python:3


RUN mkdir /code
WORKDIR /code

RUN pip install --upgrade pip
COPY ./requirements.txt /code/requirements.txt

RUN pip install --user --upgrade -r requirements.txt

COPY . /code/

WORKDIR /code/flask_app