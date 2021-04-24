import unittest
from app import app


class AppTests(unittest.TestCase):

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
        data = {
            'username': 'myName',
            'password': "12345678",
            'email': '123456@gmail.com'
        }
        response = self.app.post('/register', follow_redirects=True, data=data)
        self.assertEqual(response.status_code, 200)

    def test_login_page_get(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_login_page_post(self):
        data = {
            'username': 'admin',
            'password': "admin",
        }
        response = self.app.post('/login', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_logout_page(self):
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_raw_report_page_get(self):
        data = {'username': 'admin'}
        response = self.app.get('/raw_report', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_raw_report_page_post(self):
        data = {
            'name': 'Walmart',
            'cik': '12345678',
            'report_date': '2021-04-02',
            'username': 'admin'
        }

        response = self.app.post('/raw_report', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_generated_report_page_get(self):
        data = {'username': 'admin'}
        response = self.app.get('/generated_report', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
