FROM python:3

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

COPY . .

# CMD ["python", "auth.py"]
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]