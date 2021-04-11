## Setting up local dev environment
Until we get conda set up for a standard virtual environment, run 
```bash
pip install django
pip install djangorestframework
```
to install the neccessary dependencies.

Then we need to initialize the local database so navigate into the root directory of the repo and run
```bash
python manage.py migrate
```
This will create a local database that you can use for testing the application.

You should also create a local superuser so that you can login to the admin panel
```bash
python manage.py createsuperuser --email admin@example.com
```
Follow the prompts to create a username and password.

You can run the server locally by running
```bash
python manage.py runserver
```

## Run using Docker

First, get the containers up and running in the background
```bash
docker-compose up -d
```

# If the images need to be built, run this instead
```bash
docker-compose up --build -d
```

Now run the following commands to migrate the database
```bash
docker-compose run web python3 manage.py migrate
docker-compose run web python3 manage.py makemigrations
```

If you are unable to login to admin using the credentials below, run the following command. This will prompt you to set up a new admin superuser for testing. If you have any trouble, start a bash shell and run the command.

```bash
docker-compose run web python3 manage.py createsuperuser
```

# Run a bash interactive shell instead
```bash
docker exec -it django-server bash

python3 manage.py migrate
python3 manage.py makemigrations

python3 manage.py createsuperuser --email admin@admin.com
username: admin
password: admin
```