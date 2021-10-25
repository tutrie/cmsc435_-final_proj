from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
import json

from report_schema.generated_report import utils
from report_schema.generated_report.models import GeneratedReport, \
    GeneratedReportSerializer


class GeneratedReportAnalysisTests(TestCase):
    def setUp(self):
        User.objects.create_user('developer1', 'developer1@example.com',
                                 'developerpassword123')
        User.objects.create_user('developer2', 'developer2@example.com',
                                 'developerpassword456')
        User.objects.create_user('admin', 'admin@example.com', 'admin')

        admin = User.objects.get(username='admin')
        admin.is_superuser = True
        admin.save()

        utils.get_sheets_and_rows(
            User.objects.get(username='developer1'),
            'test report',
            'Facebook',
            '1326801',
            '2016,2017'
        )

        utils.create_generated_report(
            User.objects.get(username='developer1'),
            'test report',
            json.dumps({'CONSOLIDATED STATEMENTS OF INCOME': [0, 1, 2]}),
            'json'
        )

    def test_generated_report_analysis_valid(self):
        client = Client()
        client.login(username='developer1', password='developerpassword123')

        response = client.post(
            reverse('generated-reports-analysis'),
            user=User.objects.get(username='developer1'),
            data=json.dumps({"report_id": 1}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_generated_report_analysis_bad_request(self):
        client = Client()
        client.login(username='developer1', password='developerpassword123')

        missing_report_id = client.post(
            reverse('generated-reports-analysis'),
            user=User.objects.get(username='developer1'),
            data=json.dumps({"other_key": 1}),
            content_type='application/json'
        )

        incorrect_report_id_type = client.post(
            reverse('generated-reports-analysis'),
            user=User.objects.get(username='developer1'),
            data=json.dumps({"report_id": "string"}),
            content_type='application/json'
        )

        empty_data = client.post(
            reverse('generated-reports-analysis'),
            user=User.objects.get(username='developer1'),
            data=json.dumps({}),
            content_type='application/json'
        )

        self.assertEqual(missing_report_id.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(incorrect_report_id_type.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(empty_data.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generated_report_analysis_forbidden(self):
        invalid_user_client = Client()

        invalid_user = invalid_user_client.post(
            reverse('generated-reports-analysis'),
            user=None,
            data=json.dumps({"report_id": 1}),
            content_type='application/json'
        )

        self.assertEqual(invalid_user.status_code, status.HTTP_403_FORBIDDEN)

    def test_generated_report_analysis_not_found(self):
        valid_user_client = Client()
        valid_user_client.login(username='developer1', password='developerpassword123')

        invalid_user_client = Client()
        invalid_user_client.login(username='developer2',
                                 password='developerpassword456')

        wrong_user = invalid_user_client.post(
            reverse('generated-reports-analysis'),
            data=json.dumps({"report_id": 1}),
            content_type='application/json'
        )

        wrong_report_id = valid_user_client.post(
            reverse('generated-reports-analysis'),
            data=json.dumps({"report_id": 100}),
            content_type='application/json'
        )

        self.assertEqual(wrong_user.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(wrong_report_id.status_code, status.HTTP_404_NOT_FOUND)

