FROM python:3

# These two environment variables prevent __pycache__/ files.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip
COPY ./requirements.txt /code/requirements.txt
RUN pip install --user --upgrade -r requirements.txt

COPY . /code/