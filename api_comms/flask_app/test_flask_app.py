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


# not working bc cant send it to the django server
def test_login():
    url = BASE_URL + 'login'
    package = {'username': 'admin',
               'password': 'admin'}

    response = requests.post(url, data=json.dumps(package))
    assert response.status_code == 200


def test_logout():
    url = BASE_URL + 'logout'
    response = requests.get(url)
    assert response.status_code == 200

# def test_register(client):

