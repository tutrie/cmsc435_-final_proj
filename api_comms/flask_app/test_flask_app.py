import json
import requests
import os
import unittest
from app import app

BASE_URL = 'http://127.0.0.1:5000/'


class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    def test_main_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register_page_get(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_register_page_post(self):
        data = {'username': 'myName',
                'password': "12345678",
                'email': '123456@gmail.com'}
        response = self.app.post('/register', follow_redirects=True, data=data)
        self.assertEqual(response.status_code, 200)

    def test_login_page_get(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)


# # make sure pages load correctly
# def test_main():
#     response = requests.get(BASE_URL)
#     assert response.status_code == 200
#     response = requests.get(BASE_URL + 'login')
#     assert response.status_code == 200
#     response = requests.get(BASE_URL + 'register')
#     assert response.status_code == 200
#     response = requests.get(BASE_URL + 'logout')
#     assert response.status_code == 200
#     response = requests.get(BASE_URL + 'asdasas')
#     assert response.status_code != 200
#
#
# def test_login():
#     url = BASE_URL + 'login'
#     package = {'username': 'admin',
#                'password': 'admin'}
#
#     response = requests.get(url, data=json.dumps(package))
#     assert response.status_code == 200
#
#
# def test_register():
#     url = BASE_URL + 'register'
#     package = {'username': 'q',
#                'password1': 'q',
#                "'email": 'q@gmail.com'}
#
#     response = requests.post(url, data=json.dumps(package))
#     assert response.status_code == 200
#
#
# def test_logout():
#     url = BASE_URL + 'logout'
#     response = requests.get(url)
#     assert response.status_code == 200
