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

# Contributions
Brady Snelson - 15% - Set up django backend framework that created an API that allows a user to GET and POST generated and raw report file urls.
Jason Hipkins - 15% - Worked on filtering and cleaning excel raw reports. worked on merging reports together, lot of research on accounting methods and line item names.
Preston Thomson - 15% - Set up the CI-CD pipeline for automatic building, testing, linting, and code coverage checks.
Josh Helperin - 15% - Fixed and tested querant, created proxy functions and tested proxy.
Gilbert Garcynski - 15% - made code to download reports from the webscraper.  Implemented a database storage (dict and lists) for the webscraper.  Made methods in company.py to search the database for URL's.   Tests for each.
Siyao Li - 15% - Worked on analyzing the pyedgar library, and contributed to adding features and testing the Edgar_Lite library, which retrieves the url for a company’s 10-K/10-Q excel reports with the company’s name and CIK number.
