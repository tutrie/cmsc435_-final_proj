from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from datetime import date
import json

from .models import RawReport, GeneratedReport
from company_schema.models import Company
from .serializers import RawReportSerializer, GeneratedReportSerializer


# Create your tests here.
class RawReportTests(TestCase):
    def test_can_create_raw_report(self):
        RawReport.objects.create(
            company=Company.objects.create(name='Google', cik='123456'),
            report_date=date.today(),
            report_type='10-Q',
            excel_url='Google.com'
        )

        self.assertTrue(RawReport.objects.all())

    def test_can_retrieve_raw_report(self):
        company = Company.objects.create(name='Google', cik='123456')
        report = RawReport(company=company, report_date=date.today(), report_type='10-Q', excel_url='Google')
        report.save()

        retrieved_report = RawReport.objects.get(company=company)

        self.assertEqual(str(retrieved_report), str(report))

    def test_can_delete_raw_report(self):
        company = Company.objects.create(name='Google', cik='123456')
        report = RawReport(company=company, report_date=date.today(), report_type='10-Q', excel_url='Google')
        report.save()

        RawReport.objects.get(company=company).delete()

        self.assertFalse(RawReport.objects.all())

    def test_get_valid_raw_report(self):
        client = Client()
        report_to_get = RawReport.objects.create(
            company=Company.objects.create(name='Google', cik='123456'),
            report_date=date.today(),
            report_type='10-Q',
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
            report_type='10-Q',
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
            'report_type': '10-Q',
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
            'report_type': '10-Q',
            'excel_url': 'https://www.google.com/'
        }
        payload_2 = {
            'company': 'Microsoft',  # A non existent company
            'report_date': '2020-05-22',
            'report_type': '10-Q',
            'excel_url': 'https://www.google.com/'
        }
        payload_3 = {
            'company': 'Google',
            'report_date': '2020-05-22',
            'report_type': '10-Q',
            'excel_url': 'google.com'  # Incorrectly formatted excel_url
        }
        payload_4 = {
            'company': ['Google'],  # Wrong type
            'report_date': '2020-05-22',
            'report_type': '10-Q',
            'excel_url': 'https://www.google.com/'
        }

        payload_5 = {
            'company': ['Google'],
            'report_date': '2020-05-22',
            'report_type': '10-J',  # Invalid report_type
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
        response_5 = client.post(
            reverse('raw-reports-list'),
            data=json.dumps(payload_5),
            content_type='application/json'
        )

        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_4.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_5.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_valid_raw_report(self):
        client = Client()
        google = Company.objects.create(name='Google', cik='123456')
        Company.objects.create(name='Facebook', cik='9876524')
        report_1 = RawReport.objects.create(company=google, report_date='2020-05-22', report_type='10-Q',
                                            excel_url='Http://Google.com')
        report_2 = RawReport.objects.create(company=google, report_date='2020-05-22', report_type='10-Q',
                                            excel_url='Http://Google.com')

        payload_1 = {  # Change company
            'company': 'Facebook',
            'report_date': '2020-05-22',
            'report_type': '10-Q',
            'excel_url': 'https://www.google.com/'
        }
        payload_2 = {  # Change excel_url and form
            'company': 'Google',
            'report_date': '2020-05-22',
            'report_type': '10-K',
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

        self.assertEqual(str(RawReport.objects.get(pk=report_1.pk)), 'Report 10-Q from 2020-05-22 for Facebook')
        self.assertEqual(response_1.status_code, status.HTTP_200_OK)

        self.assertEqual(RawReport.objects.get(pk=report_2.pk).excel_url, 'https://www.facebook.com/')
        self.assertEqual(str(RawReport.objects.get(pk=report_2.pk)), 'Report 10-K from 2020-05-22 for Google')
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)

    def test_put_invalid_raw_report(self):
        client = Client()
        google = Company.objects.create(name='Google', cik='123456')
        report_1 = RawReport.objects.create(company=google, report_date='2020-05-22', report_type='10-Q',
                                            excel_url='Http://Google.com')
        report_2 = RawReport.objects.create(company=google, report_date='2020-05-22', report_type='10-Q',
                                            excel_url='Http://Google.com')

        payload_1 = {  # Company doesn't exist
            'company': 'Microsoft',
            'report_date': '2020-05-22',
            'report_type': '10-Q',
            'excel_url': 'https://www.google.com/'
        }
        payload_2 = {  # Date is invalid
            'company': 'Google',
            'report_date': '2020-13-22',
            'report_type': '10-Q',
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
        report_to_delete = RawReport.objects.create(company=google, report_date='2020-05-22', report_type='10-Q',
                                                    excel_url='Http://Google.com')

        response = client.delete(
            reverse('raw-reports-detail', kwargs={'pk': report_to_delete.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_not_exist_raw_report(self):
        client = Client()
        google = Company.objects.create(name='Google', cik='123456')
        RawReport.objects.create(company=google, report_date='2020-05-22',
                                 report_type='10-Q', excel_url='Http://Google.com')

        response = client.delete(
            reverse('raw-reports-detail', kwargs={'pk': 10})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GeneratedReportTests(TestCase):
    def setUp(self):
        User.objects.create_user('developer1', 'developer1@example.com', 'developerpassword123')

    def test_can_create_generated_report(self):
        GeneratedReport.objects.create(
            name='example name',
            created_by=User.objects.get(username='developer1'),
            path='./EdgarScraper'
        )

        self.assertTrue(GeneratedReport.objects.all())

    def test_can_retrieve_generated_report(self):
        report = GeneratedReport(name='example name', created_by=User.objects.get(username='developer1'),
                                 path='./EdgarScraper')
        report.save()

        retrieved_report = GeneratedReport.objects.get(name='example name')
        self.assertEqual(str(retrieved_report), str(report))

        retrieved_report = GeneratedReport.objects.get(path='./EdgarScraper')
        self.assertEqual(str(retrieved_report), str(report))

    def test_can_delete_generated_report(self):
        report = GeneratedReport(name='example name', created_by=User.objects.get(username='developer1'),
                                 path='./EdgarScraper')
        report.save()

        GeneratedReport.objects.get(name='example name').delete()

        self.assertFalse(RawReport.objects.all())

    def test_get_valid_generated_report(self):
        client = Client()
        report_to_get = GeneratedReport.objects.create(
            name='example name',
            created_by=User.objects.get(username='developer1'),
            path='./EdgarScraper'
        )

        response = client.get(
            reverse('generated-reports-detail', kwargs={'pk': report_to_get.pk})
        )

        report_expected = GeneratedReport.objects.get(pk=report_to_get.pk)
        serializer = GeneratedReportSerializer(report_expected)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_non_exist_raw_report(self):
        client = Client()
        GeneratedReport.objects.create(
            name='example name',
            created_by=User.objects.get(username='developer1'),
            path='./EdgarScraper'
        )

        response = client.get(
            reverse('generated-reports-detail', kwargs={'pk': 10})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_valid_generated_report(self):
        client = Client()
        payload = {
            'name': 'example name',
            'created_by': User.objects.get(username='developer1').pk,
            'path': './EdgarScraper'
        }

        response = client.post(
            reverse('generated-reports-list'),
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_generated_report(self):
        client = Client()
        payload_1 = {
            'name': 'example name',
            'created_by': 10,  # Non-existent user
            'path': './EdgarScraper'
        }
        payload_2 = {
            'name': 'example name',
            'created_by': User.objects.get(username='developer1').pk,
            'path': './example'  # Path to file that doesn't exist
        }
        payload_3 = {
            'name': '',  # No name
            'created_by': User.objects.get(username='developer1').pk,
            'path': './EdgarScraper'
        }
        payload_4 = {
            'name': ['example name'],  # Incorrect name type
            'created_by': User.objects.get(username='developer1').pk,
            'path': './EdgarScraper'
        }

        response_1 = client.post(
            reverse('generated-reports-list'),
            data=json.dumps(payload_1),
            content_type='application/json'
        )
        response_2 = client.post(
            reverse('generated-reports-list'),
            data=json.dumps(payload_2),
            content_type='application/json'
        )
        response_3 = client.post(
            reverse('generated-reports-list'),
            data=json.dumps(payload_3),
            content_type='application/json'
        )
        response_4 = client.post(
            reverse('generated-reports-list'),
            data=json.dumps(payload_4),
            content_type='application/json'
        )

        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_4.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_valid_raw_report(self):
        client = Client()
        report = GeneratedReport(name='example name', created_by=User.objects.get(username='developer1'),
                                 path='./EdgarScraper')
        report.save()
        payload = {  # Change name of report
            'name': 'a different name',
            'created_by': User.objects.get(username='developer1').pk,
            'path': './EdgarScraper'
        }

        response = client.put(
            reverse('generated-reports-detail', kwargs={'pk': report.pk}),
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(str(GeneratedReport.objects.get(pk=report.pk)),
                         'Report created by developer1, named: a different name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_invalid_raw_report(self):
        client = Client()
        report = GeneratedReport.objects.create(name='example name', created_by=User.objects.get(username='developer1'),
                                                path='./EdgarScraper')

        payload_1 = {
            'name': 'example name',
            'created_by': 10,  # Non-existent user
            'path': './EdgarScraper'
        }
        payload_2 = {
            'name': 'example name',
            'created_by': User.objects.get(username='developer1').pk,
            'path': './example'  # Path to file that doesn't exist
        }
        payload_3 = {
            'name': '',  # No name
            'created_by': User.objects.get(username='developer1').pk,
            'path': './EdgarScraper'
        }
        payload_4 = {
            'name': ['example name'],  # Incorrect name type
            'created_by': User.objects.get(username='developer1').pk,
            'path': './EdgarScraper'
        }

        response_1 = client.put(
            reverse('generated-reports-detail', kwargs={'pk': report.pk}),
            data=json.dumps(payload_1),
            content_type='application/json'
        )
        response_2 = client.put(
            reverse('generated-reports-detail', kwargs={'pk': report.pk}),
            data=json.dumps(payload_2),
            content_type='application/json'
        )
        response_3 = client.put(
            reverse('generated-reports-detail', kwargs={'pk': report.pk}),
            data=json.dumps(payload_3),
            content_type='application/json'
        )
        response_4 = client.put(
            reverse('generated-reports-detail', kwargs={'pk': report.pk}),
            data=json.dumps(payload_4),
            content_type='application/json'
        )

        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_4.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_existing_raw_report(self):
        client = Client()
        report_to_delete = GeneratedReport.objects.create(name='example name',
                                                          created_by=User.objects.get(username='developer1'),
                                                          path='./EdgarScraper')

        response = client.delete(
            reverse('generated-reports-detail', kwargs={'pk': report_to_delete.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_not_exist_company(self):
        client = Client()
        GeneratedReport.objects.create(name='example name',
                                       created_by=User.objects.get(username='developer1'), path='./EdgarScraper')

        response = client.delete(
            reverse('generated-reports-detail', kwargs={'pk': 10})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
