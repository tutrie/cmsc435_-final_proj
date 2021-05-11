from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
import json

from report_schema.generated_report.models import GeneratedReport, \
    GeneratedReportSerializer


class GeneratedReportTests(TestCase):
    def setUp(self):
        User.objects.create_user('developer1', 'developer1@example.com',
                                 'developerpassword123')
        User.objects.create_user('developer2', 'developer2@example.com',
                                 'developerpassword456')
        User.objects.create_user('admin', 'admin@example.com', 'admin')

        admin = User.objects.get(username='admin')
        admin.is_superuser = True
        admin.save()

    def test_generated_report_analysis_valid(self):
        GeneratedReport.objects.create(
            name='example name',
            created_by=User.objects.get(username='developer1'),
            json_schema='{}'
        )

        client = Client()
        client.login(username='developer1', password='developerpassword123')

        payload = {
            'report_id': 1
        }

        response = client.post(
            reverse('generated-reports-analysis'),
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

