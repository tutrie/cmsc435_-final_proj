import json
import requests

BASE_URL = 'http://127.0.0.1:5000/'


def test_main():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    response = requests.post(BASE_URL)
    assert response.status_code != 200
    response = requests.get(BASE_URL)
    assert response.status_code == 200


def test_login():
    url = BASE_URL + 'login'
    package = {'username': 'admin',
               'password': 'admin'}

    response = requests.get(url, data=json.dumps(package))
    assert response.status_code == 200


# not working bc cant send it to the django server, so a != 200  code
def test_register():
    url = BASE_URL + 'register'
    package = {"username": "q",
               "password1": "q",
               "email": "q@gmail.com"}

    response = requests.post(url, data=json.dumps(package))
    assert response.status_code == 200


def test_logout():
    url = BASE_URL + 'logout'
    response = requests.get(url)
    assert response.status_code == 200


def register_failure_duplicate_user():
    url = BASE_URL + 'register'
    package = {'username': 'admin',
               'password': 'admin',
               "email": "q@gmail.com"}

    response = requests.get(url, data=json.dumps(package))
    assert b'A user with that' in response

# def login_failure_no_user():
#     url = BASE_URL + 'logout'
#     package = {'username': 'asdfadsfdsaf',
#                'password': 'dfsafsdfsda'}
#     response = requests.get(url, data=json.dumps(package))
#     assert response
#
#

