# User Documentation

### Setting up and Running the Django Docker Container
####NOTE: You can skip this step if running the application in production mode
Start Docker
```bash
sudo service docker start
```
Build the Docker container for django
```bash
docker-compose up --build -d
```
Run the Docker container
```bash
docker-compose up -d
```
Super user login for the admin panel is

username: admin

password: admin

If you are having trouble logging in with these credentials run
```bash
docker-compose run web python3 manage.py createsuperuser
```
## Running the Application


# Developer Documentation
## Setting up Development Environment

### Dependency Setup
```bash
pip install -r requirements.txt
```

### Django Backend Setup
Create local database
```bash
python manage.py migrate
```
Create superuser for admin panel, follow the prompts to create an admin account.
```bash
python manage.py createsuperuser
```
Run the server locally on port 8000
```bash
python manage.py runserver
```
You can now browse the api and use the admin panel by going to the following links

Admin panel: http://localhost:8000/admin/

API: http://localhost:8000/api/

### Frontend Setup
Put what we have to do here for the UI/services

### Accessing Cloud Instance
Download the scraper.pem security key

SSH into the instance
```bash
ssh -i "scraper.pem" ec2-user@ec2-13-58-133-36.us-east-2.compute.amazonaws.com
```

## Running Tests
### Django tests
### Query Engine tests


## System Architecture
### Flask Frontend
#### Server:
To run the server:
1. cd into ```team-project-xrbl-scraper\api_comms\flask_app```
2. run ```python3 -m flask run```
3. visit http://127.0.0.1:5000/


#### Testing:
To run the tests:
1. Do the above to make sure the server is running or else the tests will not work as they are supposed to.



#### Functions 

```def main_page()```

Located at http://127.0.0.1:5000/, this method renders the welcome page for the website.  It has links to navigate to the Login and Register pages.

```def register()```
Located at http://127.0.0.1:5000/register, this method takes in a username, password, and email address from the user's input and sends a POST request to http://18.217.8.244:8000/api/users/create_user/.  Assuming a successful response is received(ie no duplicate users or network connectivity issues), there will be a redirect to the login page for the user to login with their credentials.

```def login()```

Located at http://127.0.0.1:5000/login, this method takes in a username and password from the user's input and sends a GET request to http://18.217.8.244:8000/api/generated-reports/ and http://18.217.8.244:8000/api/raw-reports/.  Assuming valid credentials, the user will be taken to their account page where they can view their reports.

```def logout()```

Located at http://127.0.0.1:5000/logout, this method displays a logout message when the user has logged out of their account.

```def raw_report()```

Located at http://127.0.0.1:5000/raw_report, this method will display the raw
reports for the logged-in user. 


```def generated_report()```

Located at http://127.0.0.1:5000/generated_report, this method will display the generated reports for the logged-in user.  

Note:  Timeout errors will be the result of network and internet speeds dropping.


### Django Backend API


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
docker-compose run web python3 manage.py makemigrations
docker-compose run web python3 manage.py migrate
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

# Running the data API and report runner
```bash
cd middleware/flask_api
pip install -r requirements.txt
python app.py

OR from main folder
PYTHONPATH=./ python middleware/flask_api/app.py
```
(wait a few seconds to get it started)

Using the Report Runner:
```bash
cd middleware/query_engine
python report_runner.py
```

If you run into any issues with the previous command, run the following instead from main folder
```bash
PYTHONPATH=./ python middleware/query_engine/report_runner.py
```

Once the program starts, you will be prompted to choose an option.
 Enter - 1 to Retrieve a Raw Report
 Enter - 2 to Generate a new Report
 Enter "done" to stop the program

Retieving a Raw Report:
For this Enter the follwing when prompted
CIK: 0000010329
YEARS: 2020
REPORT TYPE: 10-K

Once you are prompted to save the file, enter to save as json:
Username/
test
json

to save as xlsx workbook enter: 
Username/
test
xlsx

Generating a New Report:
CIK: 0000010329
YEARS: 2020
REPORT TYPE: 10-K
SHEETS: Document And Entity Information
ROWS: 1

Once you are prompted to save the file, enter to save as json:
Username/
test
json

to save as xlsx workbook enter: 
Username/
test
xlsx

# Contributions, Sprint 1
- Brady Snelson - 15% - Added authentication to generated-reports endpoint. Updated GET/POST/PUT routes to only allow requests from the owner of each report. Created EC2 cloud instance and set up dockerized django container to run on it. 
- Jason Hipkins - 15% - Worked on filtering and cleaning excel raw reports. worked on merging reports together, lot of research on accounting methods and line item names.
- Preston Thomson - 15% - Set up the CI-CD pipeline for automatic building, testing, linting, and code coverage checks.
- Josh Helperin - 15% - Fixed and tested querant, created proxy functions and tested proxy.
- Gilbert Garcynski - 15% - made code to download reports from the webscraper.  Implemented a database storage (dict and lists) for the webscraper.  Made methods in company.py to search the database for URL's.   Tests for each.
- Siyao Li - 15% - Worked on analyzing the pyedgar library, and contributed to adding features and testing the Edgar_Lite library, which retrieves the url for a company’s 10-K/10-Q excel reports with the company’s name and CIK number.
- Patrick Donnelly - 15% - Created a class query which handles taking user input and returns an ActiveReport. Implemented QueryEngine to handle Query creation based on user input. Added functionality in our data API to handle taking requests from users and send to proxy which sends it to QueryEngine. Updated report_runner to take user input and make calls to our data api for creating new report and getting raw reports. Created tests for report_runner. Updated docker files and docker-compose file.



# Contributions, Sprint 2
- Brady Snelson - 15% -  
- Jason Hipkins - 15% - 
- Preston Thomson - 15% - 
- Josh Helperin - 15% - 
- Gilbert Garcynski - 15% - 
- Siyao Li - 15% - 
- Patrick Donnelly - 15% -
