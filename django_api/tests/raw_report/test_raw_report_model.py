from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from datetime import date
import json

from company_schema.models import Company
from report_schema.raw_report.models import RawReport, RawReportSerializer


class RawReportTests(TestCase):
    def test_can_create_raw_report(self):
        RawReport.objects.create(
            company=Company.objects.create(name='Google', cik='123456'),
            report_date=date.today(),
            excel_url='Google.com'
        )

        self.assertTrue(RawReport.objects.all())

    def test_can_retrieve_raw_report(self):
        company = Company.objects.create(name='Google', cik='123456')
        report = RawReport(
            company=company, report_date=date.today(), excel_url='Google')
        report.save()

        retrieved_report = RawReport.objects.get(company=company)

        self.assertEqual(str(retrieved_report), str(report))

    def test_can_delete_raw_report(self):
        company = Company.objects.create(name='Google', cik='123456')
        report = RawReport(
            company=company, report_date=date.today(), excel_url='Google')
        report.save()

        RawReport.objects.get(company=company).delete()

        self.assertFalse(RawReport.objects.all())

    def test_get_valid_raw_report(self):
        client = Client()
        report_to_get = RawReport.objects.create(
            company=Company.objects.create(name='Google', cik='123456'),
            report_date=date.today(),
            excel_url='Google.com'
        )

        response = client.get(
            reverse('raw-reports-detail', kwargs={'pk': report_to_get.pk})
        )

        report_expected = RawReport.objects.get(pk=report_to_get.pk)
        serializer = RawReportSerializer(report_expected)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_non_exist_raw_report(self):
        client = Client()
        RawReport.objects.create(
            company=Company.objects.create(name='Google', cik='123456'),
            report_date=date.today(),
            excel_url='Google.com'
        )

        response = client.get(
            reverse('raw-reports-detail', kwargs={'pk': 10})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_valid_raw_report(self):
        client = Client()
        Company.objects.create(name='Google', cik='123456')
        payload = {
            'company': 'Google',
            'report_date': '2020-05-22',
            'excel_url': 'https://www.google.com/'
        }

        response = client.post(
            reverse('raw-reports-list'),
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_raw_report(self):
        client = Client()
        Company.objects.create(name='Google', cik='123456')
        payload_1 = {
            'company': 'Google',
            'report_date': '2020-13-22',  # A non existent date
            'excel_url': 'https://www.google.com/'
        }
        payload_2 = {
            'company': 'Microsoft',  # A non existent company
            'report_date': '2020-05-22',
            'excel_url': 'https://www.google.com/'
        }
        payload_3 = {
            'company': 'Google',
            'report_date': '2020-05-22',
            'excel_url': 'google.com'  # Incorrectly formatted excel_url
        }
        payload_4 = {
            'company': ['Google'],  # Wrong type
            'report_date': '2020-05-22',
            'excel_url': 'https://www.google.com/'
        }

        response_1 = client.post(
            reverse('raw-reports-list'),
            data=json.dumps(payload_1),
            content_type='application/json'
        )
        response_2 = client.post(
            reverse('raw-reports-list'),
            data=json.dumps(payload_2),
            content_type='application/json'
        )
        response_3 = client.post(
            reverse('raw-reports-list'),
            data=json.dumps(payload_3),
            content_type='application/json'
        )
        response_4 = client.post(
            reverse('raw-reports-list'),
            data=json.dumps(payload_4),
            content_type='application/json'
        )

        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_4.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_valid_raw_report(self):
        client = Client()
        google = Company.objects.create(name='Google', cik='123456')
        Company.objects.create(name='Facebook', cik='9876524')
        report_1 = RawReport.objects.create(
            company=google, report_date='2020-05-22', excel_url='Http://Google.com')
        report_2 = RawReport.objects.create(
            company=google, report_date='2020-05-22', excel_url='Http://Google.com')

        payload_1 = {  # Change company
            'company': 'Facebook',
            'report_date': '2020-05-22',
            'excel_url': 'https://www.google.com/'
        }
        payload_2 = {  # Change excel_url and form
            'company': 'Google',
            'report_date': '2020-05-22',
            'excel_url': 'https://www.facebook.com/'
        }

        response_1 = client.put(
            reverse('raw-reports-detail', kwargs={'pk': report_1.pk}),
            data=json.dumps(payload_1),
            content_type='application/json'
        )
        response_2 = client.put(
            reverse('raw-reports-detail', kwargs={'pk': report_2.pk}),
            data=json.dumps(payload_2),
            content_type='application/json'
        )

        self.assertEqual(str(RawReport.objects.get(pk=report_1.pk)),
                         'Report from 2020-05-22 for Facebook')
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)

        self.assertEqual(RawReport.objects.get(
            pk=report_2.pk).excel_url, 'https://www.facebook.com/')
        self.assertEqual(str(RawReport.objects.get(pk=report_2.pk)),
                         'Report from 2020-05-22 for Google')
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)

    def test_put_invalid_raw_report(self):
        client = Client()
        google = Company.objects.create(name='Google', cik='123456')
        report_1 = RawReport.objects.create(
            company=google, report_date='2020-05-22', excel_url='Http://Google.com')
        report_2 = RawReport.objects.create(
            company=google, report_date='2020-05-22', excel_url='Http://Google.com')

        payload_1 = {  # Company doesn't exist
            'company': 'Microsoft',
            'report_date': '2020-05-22',
            'excel_url': 'https://www.google.com/'
        }
        payload_2 = {  # Date is invalid
            'company': 'Google',
            'report_date': '2020-13-22',
            'excel_url': 'https://www.facebook.com/'
        }

        response_1 = client.put(
            reverse('raw-reports-detail', kwargs={'pk': report_1.pk}),
            data=json.dumps(payload_1),
            content_type='application/json'
        )
        response_2 = client.put(
            reverse('raw-reports-detail', kwargs={'pk': report_2.pk}),
            data=json.dumps(payload_2),
            content_type='application/json'
        )

        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_existing_raw_report(self):
        client = Client()
        google = Company.objects.create(name='Google', cik='123456')
        report = RawReport.objects.create(
            company=google, report_date='2020-05-22', excel_url='Http://Google.com')

        response = client.delete(
            reverse('raw-reports-detail', kwargs={'pk': report.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_not_exist_raw_report(self):
        client = Client()
        google = Company.objects.create(name='Google', cik='123456')
        RawReport.objects.create(
            company=google, report_date='2020-05-22', excel_url='Http://Google.com')

        response = client.delete(
            reverse('raw-reports-detail', kwargs={'pk': 10})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_raw_reports_endpoint(self):
        client = Client()
        google = Company.objects.create(name='Google', cik='123456')
        RawReport.objects.create(company=google,
                                 report_date='2020-05-22',
                                 excel_url='Http://Google.com')

        payload_1 = {
            'company': 'Google',
            'cik': '123456',
            'years': ['2020'],
        }

        response = client.get(
            reverse('raw-reports-get-raw-reports'),
            data=payload_1,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        payload_2 = {  # CIK invalid
            'company': 'Google',
            'cik': 'dkfjs;d',
            'years': '2020',
        }

        response = client.get(
            reverse('raw-reports-get-raw-reports'),
            data=payload_2,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
