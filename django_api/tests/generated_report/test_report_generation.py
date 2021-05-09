from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
import json

from report_schema.generated_report import utils

class ReportCreationTests(TestCase):
    def setUp(self):
        User.objects.create_user('developer1', 'developer1@example.com', 'developerpassword123')
        User.objects.create_user('developer2', 'developer2@example.com', 'developerpassword456')
        User.objects.create_user('admin', 'admin@example.com', 'admin')
        
        admin = User.objects.get(username='admin')
        admin.is_superuser = True
        admin.save()

    def test_get_form_data_endpoint_1(self):
        client = Client()
        client.login(username='developer1', password='developerpassword123')

        payload = {
            'report_name': 'test report',
            'company': 'Bassett',
            'cik': '0000010329',
            'years': '2016,2017,2018'
        }

        response = client.post(
            reverse('generated-reports-get-form-data'),
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_form_data_endpoint_2(self):
        client = Client()
        client.login(username='developer1', password='developerpassword123')

        payload = {
            'report_name': 'test report',
            'company': 'Bassett',
            'cik': '0000010329',
            'years': '2016,2019'
        }

        response = client.post(
            reverse('generated-reports-get-form-data'),
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_form_data_endpoint_3(self):
        client = Client()
        client.login(username='developer1', password='developerpassword123')

        payload = {
            'report_name': 'test report',
            'company': 'Facebook',
            'cik': '1326801',
            'years': '2020'
        }

        response = client.post(
            reverse('generated-reports-get-form-data'),
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_report_endpoint_1(self):
        client = Client()
        client.login(username='developer1', password='developerpassword123')
        utils.get_sheets_and_rows(
            User.objects.get(username='developer1'),
            'test report',
            'Bassett',
            '0000010329',
            '2016,2017'
        )

        payload = {
            'report_name': 'test report',
            'form_data': json.dumps({'Document And Entity Information': [0, 1]}),
            'type': 'json',
        }

        response = client.post(
            reverse('generated-reports-create-report'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_report_endpoint_2(self):
        client = Client()
        client.login(username='developer2', password='developerpassword456')
        utils.get_sheets_and_rows(
            User.objects.get(username='developer2'),
            'test report',
            'Facebook',
            '1326801',
            '2016,2020'
        )

        payload = {
            'report_name': 'test report',
            'form_data': json.dumps({'CONSOLIDATED STATEMENTS OF INCOME': [0, 1, 2]}),
            'type': 'xlsx',
        }

        response = client.post(
            reverse('generated-reports-create-report'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_full_creation_pipeline(self):
        client = Client()
        client.login(username='developer1', password='developerpassword123')

        # Get form data
        payload_1 = {
            'report_name': 'test report',
            'company': 'Facebook',
            'cik': '1326801',
            'years': '2020'
        }

        response_1 = client.post(
            reverse('generated-reports-get-form-data'),
            data=json.dumps(payload_1),
            content_type='application/json'
        )

        # Mock filtering of the form data
        new_form_data = {}
        i = 0
        for sheet in json.loads(response_1.json()['form_data']):
            if i == 3:
                new_form_data[sheet] = [0, 1, 2]
            i += 1
        
        # Filter report
        payload_2 = {
            'report_name': 'test report',
            'form_data': json.dumps(new_form_data),
            'type': 'json'
        }

        response_2 = client.post(
            reverse('generated-reports-create-report'),
            data=json.dumps(payload_2),
            content_type='application/json'
        )
        
        self.assertEqual(response_2.status_code, status.HTTP_201_CREATED)