FROM python:3

# These two environment variables prevent __pycache__/ files.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt .

RUN pip install --user --upgrade -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
