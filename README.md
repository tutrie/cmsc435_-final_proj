# User Documentation
### Usage 
* Visit http://18.217.8.244:5000/ to access the frontend UI.
* There are six tabs at the top of the page:
  
  ```Home```, ```Raw Reports```, ```Generated Reports```, ```Report Generation```, ```Login```, ```Register```
* To create an account, go to ```Register``` tab to register an account in our system.
* To log into your account, go to ```Login``` tab to log into your registered account.
  * (Add the info for zoom meeting)
* To get a raw report of a company's 10K documentation, go to ```Raw Reports```, fill in the information and submit request.
* To create a customized generate report, go to ```Report Generation```. 
  * First fill in the general information for the report you want to create, and click the next step button. (Note that the report name needs to be distinct for each generated report) 
  * On the next page, pick the sheets and rows you want to include in the generated report, then submit the information.
* To get the existing generated report in the current account, go to ```Generated Reports```.
  * You can press the analysis button to run a min/max/avg analysis on the report
  * You can press the download button to download the report to your computer (note that this is pending on Gil's completion of that story)
* To create a generated report go to the report generation tab and enter the information for the company you want to generate a report for
  * On the next screen, you can select which rows you want to pull from the raw reports for each sheet.

#### Links
##### Admin Panel
http://18.217.8.244:8000/admin

(login with admin,admin)
##### Visual API
http://18.217.8.244:8000/api
##### Frontend
http://18.217.8.244:5000/

### Sphinx Documentation
The following commands will create an index.html file in docs/build/html/index.html
```bash
  cd docs
  make.bat html
```

# Developer Documentation

### Accessing Cloud Instance
* Download the scraper.pem security key

* SSH into the instance
    ```bash
    chmod 400 scraper.pem
    ssh -i "scraper.pem" ec2-user@ec2-18-217-8-244.us-east-2.compute.amazonaws.com
    ```

### Starting the Production Containers
```bash
docker-compose up --build -d
```

### Setup database
```bash
docker exec django-server python3 manage.py makemigrations
docker exec django-server python3 manage.py migrate
```

### Setup superuser
```bash
docker exec -it django-server python3 manage.py createsuperuser
```

### Running Tests

#### Starting Test Containers
```bash
docker-compose -f testing-compose.yaml build --build-arg TESTING="True"
docker-compose -f testing-compose.yaml up -d
```

#### Backend Tests
```bash
docker exec django-test-server python manage.py test
```

#### Backend Tests with coverage

```bash
docker exec django-test-server coverage run --omit venv/*,*/migrations*,*test* --source company_schema,report_schema manage.py test

docker exec django-test-server coverage report
```

#### Frontend Tests
```bash
docker exec flask-test-server pytest flask_app/test_flask_app.py
```

#### Frontend Tests with coverage
```bash
docker exec flask-test-server coverage run --omit venv/*,*test* -m pytest flask_app/test_flask_app.py

docker exec flask-test-server coverage report
```

### System Architecture
#### Flask Frontend Routes

* ```/```
  
  The index route, which is the welcome page for the website. It has links to navigate to the Login and Register pages.

* ```/register```
  
  The register route, which takes in a username, password, and email address from the user's input and sends a POST request to http://18.217.8.244:8000/api/users/create-user/.  Assuming a successful response is received(ie no duplicate users or network connectivity issues), there will be a user created with the given credentials and email ready for a login.

* ```/login```

  The login route, which takes in a username and password from the user's input and renders the login template, setting the username and password to their respective variables in the session object.

* ```/logout```

  The logout route which logout the current user from the session and displays a logout message when the user has logged out of their account.

* ```/raw_report```

  The raw report route which displays the form of raw reports request and allow logged-in user to retrieve new raw reports. 

* ```/generated_report```

  The generated report route which displays the generated reports for the logged-in user.  
* ```/zoom_link```

  The zoom link route which takes a user to a page where they may decide to login to their own zoom account to host a meeting
  or use the public multi-user link
  
* ```/report_generation```

  The report generation route which allows the logged-in user to create generated reports.  

Note:  Timeout errors will be the result of network and internet speeds dropping.

#### Django API Endpoints

* ```/users/create-user```
  Create a user by sending a POST request to this route.

* ```/users/validate-user```
  Will return a 200 if the user's login information is valid and 403 if it is not.

* ```/raw-reports```
  Can make GET/POST/PUT/DELETE to this endpoint to manipulate raw reports.

* ```/generated-reports```
  Can make GET/POST/PUT/DELETE to this endpoint to manipulate generated reports.

* ```/generated-reports/get-form-data```
  Make a post request to this endpoint to begin the report generation process and retrieve the rows/sheets in the merged raw report

* ```/generated-reports/create-report```
  Make a post request with the filtered form data to finish the report generation process.

* ```/generated-reports/analysis```
  Make a post request to this endpoint with a generated report to run a min/max/avg analysis on it.

# Contributions
### Sprint 1
- Brady Snelson - 15% - Added authentication to generated-reports endpoint. Updated GET/POST/PUT routes to only allow requests from the owner of each report. Created EC2 cloud instance and set up dockerized django container to run on it.
- Jason Hipkins - 15% - Worked on filtering and cleaning excel raw reports. worked on merging reports together, lot of research on accounting methods and line item names.
- Preston Thomson - 15% - Set up the CI-CD pipeline for automatic building, testing, linting, and code coverage checks.
- Josh Helperin - 15% - Fixed and tested querant, created proxy functions and tested proxy.
- Gilbert Garczynski - 15% - made code to download reports from the webscraper.  Implemented a database storage (dict and lists) for the webscraper.  Made methods in company.py to search the database for URL's.   Tests for each.
- Siyao Li - 15% - Worked on analyzing the pyedgar library, and contributed to adding features and testing the Edgar_Lite library, which retrieves the url for a company’s 10-K/10-Q excel reports with the company’s name and CIK number.
- Patrick Donnelly - 15% - Created a class query which handles taking user input and returns an ActiveReport. Implemented QueryEngine to handle Query creation based on user input. Added functionality in our data API to handle taking requests from users and send to proxy which sends it to QueryEngine. Updated report_runner to take user input and make calls to our data api for creating new report and getting raw reports. Created tests for report_runner. Updated docker files and docker-compose file.



### Sprint 2
- Brady Snelson - 15% -  Added authentication to generated-reports endpoint. Updated GET/POST/PUT routes to only allow requests from the owner of each report. Created EC2 cloud instance and set up dockerized django container to run on it.
- Jason Hipkins - 15% - got generated report working and saving locally, fixed bugs in josh's code, merged and fixed bugs, got filtering working and merging reports fully functional, almost did code coverage for all of report_runner but it works on console.
- Preston Thomson - 15% - 
- Joshua Helperin - 15% - Integrated report_runner.py and EdgarScraper.py into django_api direcotry, enabled saving raw reports to database and local user directory after pulling from edgar.sec.gov, debugged models.py, EdgarScraper.py, utils.py, and report_runner.py, changed and fixed implementation of active_reports.py and report_runner.py, made tests for utils.py and report_runner.py.
- Gilbert Garczynski - 15% - Created frontend server for the User Interface.  Implemented login, registration, logout, and viewing of reports along with HTML for each.
- Siyao Li - 15% - Worked on designing frontend UI pages and navigation. Wrote tests for frontend flask app.py. Implemented the feature of storing user's login state. Formatted the README.md file.
- Patrick Donnelly - 15% - Reviewed/approved merge requests. Improved CI/CD pipeline build times by using caching. Updated CI/CD to get all of the tests and coverage. Created Sphinx documentation. Created Dockerfiles for flask_ui and added a service to the docker-compose file. Also created a dockerfile for the report_runner.py so the can be ran from any os. Coded the proxy and helped debug errors.

### Sprint 3
- Brady Snelson - 15% - Refactored/transferred the functionality that existed within the report runner file (the core of report generation) into endpoints on the django backed. Rewrote tests for all of said functionality. Engineered a new solution to creating a report through a from instead of prompting for user input. Added an authentication endpoint to the user model.
- Gilbert Garczynski - 15% - Added download report button for raw reports.  Added zoom link for the company and to login to your personal zoom.  Fixes to website tests and other design fixes to various other files.
- Siyao Li - 15% - Created frontend report generation page with dynamic multiselect forms. Integreated frontend report generation page with Django server. Integrated login page with django authentication endpoint, and fixed bug on registration page. Added tests for the report generation. Worked on styling the frontend UI. 
- Jason Hipkins - 15% - Fixed an issue with excel spreadsheets not saving correclty. Assisted in refactoring functionality of report runner and manually merging active report and object conversions to the backend. Added backend coding for converting reports from database json to downloadable excel files. Added more functionality to active_report.py by removing duplicated columns and information. 
- Patrick Donnelly - 15% - Created endpoints in the frontend flask app and backend django api to handle report analysis. Made improvements to docker setup and created a docker compose file specifically for testing. Added validation methods for analysis endpoints and helper methods for running the analysis. Added tests for frontend and backend endpoints and analysis helper methods.
- Preston Thomson - 15% - Cleaned up CI-CD pipeline and wrote documentation for it.  Spent an unfortunately long amount of time trying to get docker commands to work in the pipeline for easy deployment into AWS.  Was forced to abondon this effort in favor of making sure all tests were passing and leaving AWS deployment to a manual task.  Worked with other group members to make sure all tests were passing in the pipeline before final submission.
- Joshua Helperin - 15% - Enabled the viewing of generated reports with JQuery plugin Datatables and wrote routes, templates, CSS, and JS files to facilitate this functionality. Additionally tested said routes and fixed miscellaneous errors/bugs on both backend and frontend. 
   
