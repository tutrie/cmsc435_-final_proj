from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
import json

from .models import GeneratedReport, GeneratedReportSerializer
from report_schema.raw_report.models import RawReport


class GeneratedReportTests(TestCase):
    def setUp(self):
        User.objects.create_user('developer1', 'developer1@example.com', 'developerpassword123')

    def test_can_create_generated_report(self):
        GeneratedReport.objects.create(
            name='example name',
            created_by=User.objects.get(username='developer1'),
            path='./main_app'
        )

        self.assertTrue(GeneratedReport.objects.all())

    def test_can_retrieve_generated_report(self):
        report = GeneratedReport(name='example name', created_by=User.objects.get(username='developer1'),
                                 path='./main_app')
        report.save()

        retrieved_report = GeneratedReport.objects.get(name='example name')
        self.assertEqual(str(retrieved_report), str(report))

        retrieved_report = GeneratedReport.objects.get(path='./main_app')
        self.assertEqual(str(retrieved_report), str(report))

    def test_can_delete_generated_report(self):
        report = GeneratedReport(name='example name', created_by=User.objects.get(username='developer1'),
                                 path='./main_app')
        report.save()

        GeneratedReport.objects.get(name='example name').delete()

        self.assertFalse(GeneratedReport.objects.all())

    def test_get_valid_generated_report(self):
        client = Client()
        client.login(username='developer1', password='developerpassword123')
        report_to_get = GeneratedReport.objects.create(
            name='example name',
            created_by=User.objects.get(username='developer1'),
            path='./main_app'
        )

        response = client.get(
            reverse('generated-reports-detail', kwargs={'pk': report_to_get.pk})
        )

        report_expected = GeneratedReport.objects.get(pk=report_to_get.pk)
        serializer = GeneratedReportSerializer(report_expected)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_non_exist_generated_report(self):
        client = Client()
        client.login(username='developer1', password='developerpassword123')
        GeneratedReport.objects.create(
            name='example name',
            created_by=User.objects.get(username='developer1'),
            path='./main_app'
        )

        response = client.get(
            reverse('generated-reports-detail', kwargs={'pk': 10})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_valid_generated_report(self):
        client = Client()
        client.login(username='developer1', password='developerpassword123')
        payload = {
            'name': 'example name',
            'path': './main_app'
        }

        response = client.post(
            reverse('generated-reports-list'),
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_generated_report(self):
        client = Client()
        client.login(username='developer1', password='developerpassword123')
        payload_1 = {
            'name': 'example namedssaaaaaaaaaaaaaaaaaaaaaaaaaaasdfasdkjhasdfkljghadskjhgakjhdsfakjhdsgdsfhhsfkjlasdfkljhlkdfaksfajdshkjhsdfkjlahsdfkashfhfkhsdfssdfaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', # Name that's too long
            'path': './main_app'
        }
        payload_2 = {
            'name': 'example name',
            'path': './example'  # Path to file that doesn't exist
        }
        payload_3 = {
            'name': '',  # No name
            'path': './main_app'
        }
        payload_4 = {
            'name': ['example name'],  # Incorrect name type
            'path': './main_app'
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

    # def test_put_valid_raw_report(self):
    #     client = Client()
    #     client.login(username='developer1', password='developerpassword123')
    #     report = GeneratedReport(name='example name', created_by=User.objects.get(username='developer1'),
    #                              path='./report_schema')
    #     report.save()
    #     payload = {  # Change name of report
    #         'name': 'a different name',
    #         'path': './report_schema'
    #     }

    #     response = client.put(
    #         reverse('generated-reports-detail', kwargs={'pk': report.pk}),
    #         data=json.dumps(payload),
    #         content_type='application/json'
    #     )

    #     self.assertEqual(str(GeneratedReport.objects.get(pk=report.pk)),
    #                      'Report created by developer1, named: a different name')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_invalid_generated_report(self):
        client = Client()
        client.login(username='developer1', password='developerpassword123')
        report = GeneratedReport.objects.create(name='example name', created_by=User.objects.get(username='developer1'),
                                                path='./main_app')

        payload_1 = {
            'name': 'example name',
            'path': './main_app'
        }
        payload_2 = {
            'name': 'example name',
            'path': './example'  # Path to file that doesn't exist
        }
        payload_3 = {
            'name': '',  # No name
            'path': './main_app'
        }
        payload_4 = {
            'name': ['example name'],  # Incorrect name type
            'path': './main_app'
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

    def test_delete_existing_generated_report(self):
        client = Client()
        client.login(username='developer1', password='developerpassword123')
        report_to_delete = GeneratedReport.objects.create(name='example name',
                                                          created_by=User.objects.get(username='developer1'),
                                                          path='./main_app')

        response = client.delete(
            reverse('generated-reports-detail', kwargs={'pk': report_to_delete.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_not_exist_company(self):
        client = Client()
        client.login(username='developer1', password='developerpassword123')
        GeneratedReport.objects.create(name='example name',
                                       created_by=User.objects.get(username='developer1'), path='./main_app')

        response = client.delete(
            reverse('generated-reports-detail', kwargs={'pk': 10})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
