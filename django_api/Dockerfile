FROM python:3

# These two environment variables prevent __pycache__/ files.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Prevents pip cache to reduce image size
ENV PIP_NO_CACHE_DIR 1

RUN pip install --upgrade pip

COPY wait-for-it.sh /usr/bin/
RUN chmod u+x /usr/bin/wait-for-it.sh

COPY requirements.txt requirements.txt
RUN pip install --upgrade -r requirements.txt

COPY . code
WORKDIR /code