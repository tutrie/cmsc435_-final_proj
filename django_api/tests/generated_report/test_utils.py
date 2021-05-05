from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
import json

from report_schema.generated_report.models import GeneratedReport, GeneratedReportSerializer


class UtilTests(TestCase):
    def setUp(self):
        User.objects.create_user('developer1', 'developer1@example.com', 'developerpassword123')
        User.objects.create_user('developer2', 'developer2@example.com', 'developerpassword456')
        User.objects.create_user('admin', 'admin@example.com', 'admin')
        
        admin = User.objects.get(username='admin')
        admin.is_superuser = True
        admin.save()

    def test_validate_get_form_data_request(self):
        pass

    def validate_create_report_request(self):
        pass