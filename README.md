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