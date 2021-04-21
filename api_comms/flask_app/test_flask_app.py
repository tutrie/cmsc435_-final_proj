import json
import requests

BASE_URL = 'http://127.0.0.1:5000/'


# send a request with the right json body


# make sure pages load correctly
def test_main():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    response = requests.get(BASE_URL + 'login')
    assert response.status_code == 200
    response = requests.get(BASE_URL + 'register')
    assert response.status_code == 200
    response = requests.get(BASE_URL + 'logout')
    assert response.status_code == 200
    response = requests.get(BASE_URL + 'asdasas')
    assert response.status_code != 200


def test_login():
    url = BASE_URL + 'login'
    package = {'username': 'admin',
               'password': 'admin'}

    response = requests.get(url, data=json.dumps(package))
    assert response.status_code == 200


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
