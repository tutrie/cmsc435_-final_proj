## Server:
To run the server:
1. cd into api_comms\flask_app
2. run python3 -m flask run
3. visit http://127.0.0.1:5000/


## Testing:
To run the tests:
1. Do the above to make sure the server is running or else the tests will not work as they are supposed to.



## Functions 

```def main_page()```

Located at http://127.0.0.1:5000/, this method renders the welcome page for the website.  It has links to navigate to the Login and Register pages.

```def register()```
Located at http://127.0.0.1:5000/register, this method takes in a username, password, and email address from the user's input and sends a POST request to http://18.217.8.244:8000/api/users/create_user/.  Assuming a successful response is received(ie no duplicate users or network connectivity issues), there will be a redirect to the login page for the user to login with their credentials.

```def login()```

Located at http://127.0.0.1:5000/login, this method takes in a username and password from the user's input and sends a GET request to http://18.217.8.244:8000/api/generated-reports/.  Assuming valid credentials, the user will be taken to their account page where they can view their reports.

```def logout()```


Note:  Timeout errors will be the result of network and internet speeds dropping.