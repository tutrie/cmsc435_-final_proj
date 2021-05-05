from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
import json

from report_schema.generated_report.models import GeneratedReport, GeneratedReportSerializer
from report_schema.generated_report import utils

class GenReportUtilTests(TestCase):
    def test_validate_get_form_data_request_with_valid_requests(self):
        request_1 = {
            'report_name': 'test report',
            'company': 'Bassett',
            'cik': '0000010329',
            'years': '2016,2017,2018'
        }
        request_2 = {
            'report_name': 'test report',
            'company': 'Bassett',
            'cik': '0000010329',
            'years': '2016,2017'
        }
        request_3 = {
            'report_name': 'test report',
            'company': 'Bassett',
            'cik': '0000010329',
            'years': '2016,2017'
        }
        request_4 = {
            'report_name': 'test report',
            'company': 'Bassett',
            'cik': '0000010329',
            'years': '2016,2017'
        }

        res_1, _ = utils.validate_get_form_data_request(request_1)
        res_2, _ = utils.validate_get_form_data_request(request_2)
        res_3, _ = utils.validate_get_form_data_request(request_3)
        res_4, _ = utils.validate_get_form_data_request(request_4)

        print(res_1)
        print(res_2)
        print(res_3)
        print(res_4)

        self.assertTrue(res_1)
        self.assertTrue(res_2)
        self.assertTrue(res_3)
        self.assertFalse(res_4)
        self.assertFalse(True)
        

    def test_validate_get_form_data_request_with_valid_requests(self):
        pass

    def validate_create_report_request(self):
        pass