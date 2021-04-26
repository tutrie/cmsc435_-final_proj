FROM python:3

COPY . /code

ENV PYTHONPATH=/code \
    TERM=xterm

RUN pip install --user --upgrade -r /code/report_runner_requirements.txt

WORKDIR /code