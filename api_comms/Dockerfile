FROM python:3

# These two environment variables prevent __pycache__/ files.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ADD wait-for-it.sh /usr/bin/
RUN chmod u+x /usr/bin/wait-for-it.sh

RUN mkdir /code
WORKDIR /code

RUN pip install --upgrade pip
COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade -r requirements.txt

COPY . /code/

WORKDIR /code/flask_app