FROM python:3

# These two environment variables prevent __pycache__/ files.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY wait-for-it.sh /usr/bin/
RUN chmod u+x /usr/bin/wait-for-it.sh

RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN pip install --upgrade -r requirements.txt

COPY . .

WORKDIR ./flask_app