FROM python:3

# These two environment variables prevent __pycache__/ files.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Prevents pip cache to reduce image size
ENV PIP_NO_CACHE_DIR 1

RUN pip install --upgrade pip

COPY wait-for-it.sh /usr/bin/
RUN chmod u+x /usr/bin/wait-for-it.sh

WORKDIR /code

# Cache installed dependencies between builds
COPY requirements.txt /code/
RUN pip install --upgrade -r requirements.txt

# Mounts the application code to the image
COPY . /code/