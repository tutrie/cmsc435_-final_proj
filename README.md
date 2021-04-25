# User Documentation

### Setting up the Docker Container
* cd into the middleware directory.
  ```bash
  cd middleware
  ```
* Build the Docker image.
  ```bash
  docker build -t report-runner .
  ```

* Starting the Docker container.
  
  **Windows:**
  ```bash
  docker run -it -v %cd%:/code report-runner bash
  ```
  
  **Linux:** 
  
  ```bash
  docker run -it -v $(pwd):/code report-runner bash
  ```

* Once the container terminal starts, run the following command:

  ```bash
  python middleware/query_engine/report_runner.py
  ```

* Once the program starts, you will be prompted to choose an option.
 * Enter - 1 to Retrieve a Raw Report
 * Enter - 2 to Generate a new Report
 * Enter "done" to stop the program

For retieving a Raw Report, enter the follwing when prompted
* CIK: 0000010329
* YEARS: 2020
* REPORT TYPE: 10-K

Once you are prompted to save the file, enter to save as json:
* Username
* test
* json

to save as xlsx workbook enter: 
* Username/
* test
* xlsx

Generating a New Report:
* CIK: 0000010329
* YEARS: 2020
* REPORT TYPE: 10-K
* SHEETS: Document And Entity Information
* ROWS: 1

Once you are prompted to save the file, enter to save as json:
* Username/
* test
* json

to save as xlsx workbook enter: 
* Username/
* test
* xlsx

### Usage of the Frontend UI
* Visit http://18.217.8.244:5000/ to access the frontend UI.
* There are five tabs at the top of the page:
  
  ```Home```, ```Raw Reports```, ```Generated Reports```, ```Login```, ```Register```
* To create an account, go to ```Register``` tab to register an account in our system.
* To log into your account, go to ```Login``` tab to log into your registered account.
* To get a raw report of a company's 10K documentation, go to ```Raw Reports```, fill in the information and submit request.
* To get the existing generated report in the current account, go to ```Generated Reports```.


### Accessing Cloud Instance
* Download the scraper.pem security key

* SSH into the instance
    ```bash
    ssh -i "scraper.pem" ec2-user@ec2-13-58-133-36.us-east-2.compute.amazonaws.com
    ```

## Running Tests
### Django Tests
* Run the following command in the terminal to run the tests.
```bash
  cd django_api
  python manage.py migrate
  python manage.py test
```
### Query Engine Tests
* Run the following command in the terminal to run the tests.
  ```bash
  python middleware/query_engine/tests_query_engine/test_report_runner.py
  ```

### Frontend Flask Tests
* Run the following command in the terminal to run the tests.
    ```bash
    python api_comms/flask_app/test_flask_app.py
    ```

## System Architecture
### Flask Frontend Routes

* ```/```
  
  The index route, which is the welcome page for the website. It has links to navigate to the Login and Register pages.

* ```/register```
  
  The register route, which takes in a username, password, and email address from the user's input and sends a POST request to http://18.217.8.244:8000/api/users/create_user/.  Assuming a successful response is received(ie no duplicate users or network connectivity issues), there will be a user created with the given credentials and email ready for a login.

* ```/login```

  The login route, which takes in a username and password from the user's input and renders the login template, setting the username and password to their respective variables in the session object.

* ```/logout```

  The logout route which logout the current user from the session and displays a logout message when the user has logged out of their account.

* ```/raw_report```

  The raw report route which displays the form of raw reports request and allow logged-in user to retrieve new raw reports. 

* ```/generated_report```

  The generated report route which displays the generated reports for the logged-in user.  

Note:  Timeout errors will be the result of network and internet speeds dropping.


# Contributions, Sprint 1
- Brady Snelson - 15% - Added authentication to generated-reports endpoint. Updated GET/POST/PUT routes to only allow requests from the owner of each report. Created EC2 cloud instance and set up dockerized django container to run on it.
- Jason Hipkins - 15% - Worked on filtering and cleaning excel raw reports. worked on merging reports together, lot of research on accounting methods and line item names.
- Preston Thomson - 15% - Set up the CI-CD pipeline for automatic building, testing, linting, and code coverage checks.
- Josh Helperin - 15% - Fixed and tested querant, created proxy functions and tested proxy.
- Gilbert Garczynski - 15% - made code to download reports from the webscraper.  Implemented a database storage (dict and lists) for the webscraper.  Made methods in company.py to search the database for URL's.   Tests for each.
- Siyao Li - 15% - Worked on analyzing the pyedgar library, and contributed to adding features and testing the Edgar_Lite library, which retrieves the url for a company’s 10-K/10-Q excel reports with the company’s name and CIK number.
- Patrick Donnelly - 15% - Created a class query which handles taking user input and returns an ActiveReport. Implemented QueryEngine to handle Query creation based on user input. Added functionality in our data API to handle taking requests from users and send to proxy which sends it to QueryEngine. Updated report_runner to take user input and make calls to our data api for creating new report and getting raw reports. Created tests for report_runner. Updated docker files and docker-compose file.



# Contributions, Sprint 2
- Brady Snelson - 15% -  Added authentication to generated-reports endpoint. Updated GET/POST/PUT routes to only allow requests from the owner of each report. Created EC2 cloud instance and set up dockerized django container to run on it.
- Jason Hipkins - 15% - got generated report working and saving locally, fixed bugs in josh's code, merged and fixed bugs, got filtering working and merging reports fully functional, almost did code coverage for all of report_runner but it works on console.
- Preston Thomson - 15% - 
- Josh Helperin - 15% - 
- Gilbert Garczynski - 15% - Created frontend server for the User Interface.  Implemented login, registration, logout, and viewing of reports along with HTML for each.
- Siyao Li - 15% - Worked on designing frontend UI pages and navigation. Wrote tests for frontend flask app.py. Implemented the feature of storing user's login state. Formatted the README.md file.
- Patrick Donnelly - 15% - Reviewed/approved merge requests. Improved CI/CD pipeline build times by using caching. Updated CI/CD to get all of the tests and coverage. Created Sphinx documentation. Created Dockerfiles for flask_ui and added a service to the docker-compose file. Also created a dockerfile for the report_runner.py so the can be ran from any os. Coded the proxy and helped debug errors.
