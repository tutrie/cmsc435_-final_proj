FROM python:3

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt .

RUN pip install --user --upgrade -r requirements.txt

COPY auth.py .

CMD ["python", "auth.py"]
