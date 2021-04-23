from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
import json

from .models import GeneratedReport, GeneratedReportSerializer


class GeneratedReportTests(TestCase):
    def setUp(self):
        User.objects.create_user('developer1', 'developer1@example.com', 'developerpassword123')
        User.objects.create_user('developer2', 'developer2@example.com', 'developerpassword456')
        User.objects.create_user('admin', 'admin@example.com', 'admin')
        
        admin = User.objects.get(username='admin')
        admin.is_superuser = True
        admin.save()

    def test_can_create_generated_report(self):
        GeneratedReport.objects.create(
            name='example name',
            created_by=User.objects.get(username='developer1'),
            json_schema='{}'
        )

        self.assertTrue(GeneratedReport.objects.all())

    def test_can_retrieve_generated_report(self):
        report = GeneratedReport(name='example name', created_by=User.objects.get(username='developer1'),
                                 json_schema='{}')
        report.save()

        retrieved_report = GeneratedReport.objects.get(name='example name')
        self.assertEqual(str(retrieved_report), str(report))

        retrieved_report = GeneratedReport.objects.get(json_schema='{}')
        self.assertEqual(str(retrieved_report), str(report))

    def test_can_delete_generated_report(self):
        report = GeneratedReport(name='example name', created_by=User.objects.get(username='developer1'),
                                 json_schema='{}')
        report.save()

        GeneratedReport.objects.get(name='example name').delete()

        self.assertFalse(GeneratedReport.objects.all())

    def test_get_valid_generated_report(self):
        client = Client()
        client.login(username='developer1', password='developerpassword123')
        report_to_get = GeneratedReport.objects.create(
            name='example name',
            created_by=User.objects.get(username='developer1'),
            json_schema='{}'
        )

        response = client.get(
            reverse('generated-reports-detail', kwargs={'pk': report_to_get.pk})
        )

        report_expected = GeneratedReport.objects.get(pk=report_to_get.pk)
        serializer = GeneratedReportSerializer(report_expected)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_generated_reports(self):
        client = Client()
        client.login(username='developer1', password='developerpassword123')
        GeneratedReport.objects.create(
            name='example name 1',
            created_by=User.objects.get(username='developer1'),
            json_schema='{}'
        )
        GeneratedReport.objects.create(
            name='example name 2',
            created_by=User.objects.get(username='developer1'),
            json_schema='{}'
        )

        response = client.get(
            reverse('generated-reports-list')
        )

        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_non_exist_generated_report(self):
        client = Client()
        client.login(username='developer1', password='developerpassword123')
        GeneratedReport.objects.create(
            name='example name',
            created_by=User.objects.get(username='developer1'),
            json_schema='{}'
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
            'json_schema': '{}'
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
            'name': '''
            namedssaaaaaaaaaaaaaaaaaaaaaaaaaaa
            sdfasdkjhasdfkljghadskjhgakjhdsfak
            jhdsgdsfhhsfkjlasdfkljhlkdfaksfajd
            shkjhsdfkjlahsdfkashfhfkhsdfssdfaa
            aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
            aaaaaaaaaadafasdfasdfasdfasdfasdfa''',  # Name that's too long
            'json_schema': '{}'
        }
        payload_2 = {
            'name': 'example name',
            'json_schema': {}  # json_schema is a dictionary
        }
        payload_3 = {
            'name': '',  # No name
            'json_schema': '{}'
        }
        payload_4 = {
            'name': ['example name'],  # Incorrect name type
            'json_schema': '{}'
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
        client.login(username='developer1', password='developerpassword123')
        report = GeneratedReport(name='example name', created_by=User.objects.get(username='developer1'),
                                 json_schema='{}')
        report.save()
        payload = {  # Change name of report
            'name': 'a different name',
            'json_schema': '{}'
        }

        response = client.put(
            reverse('generated-reports-detail', kwargs={'pk': report.pk}),
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(str(GeneratedReport.objects.get(pk=report.pk)),
                         'Report created by developer1, named: a different name')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_invalid_generated_report(self):
        client = Client()
        client.login(username='developer1', password='developerpassword123')
        report = GeneratedReport.objects.create(name='example name', created_by=User.objects.get(username='developer1'),
                                                json_schema='{}')

        payload_1 = {
            'name': 'example name',
            'json_schema': {}  # json_schema thats actual json
        }
        payload_2 = {
            'name': '',  # No name
            'json_schema': '{}'
        }
        payload_3 = {
            'name': ['example name'],  # Incorrect name type
            'json_schema': '{}'
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

        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_3.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_existing_generated_report(self):
        client = Client()
        client.login(username='developer1', password='developerpassword123')
        report_to_delete = GeneratedReport.objects.create(name='example name',
                                                          created_by=User.objects.get(username='developer1'),
                                                          json_schema='{}')

        response = client.delete(
            reverse('generated-reports-detail', kwargs={'pk': report_to_delete.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_not_exist_company(self):
        client = Client()
        client.login(username='developer1', password='developerpassword123')
        GeneratedReport.objects.create(name='example name',
                                       created_by=User.objects.get(username='developer1'), json_schema='{}')

        response = client.delete(
            reverse('generated-reports-detail', kwargs={'pk': 10})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_superuser_get_all_reports(self):
        client = Client()
        client.login(username='admin', password='admin')
        GeneratedReport.objects.create(name='example name 1',
                                       created_by=User.objects.get(username='developer1'), json_schema='{}')
        GeneratedReport.objects.create(name='example name 2',
                                       created_by=User.objects.get(username='developer2'), json_schema='{}')
        
        response = client.get(
            reverse('generated-reports-list')
        )
        
        self.assertTrue(len(response.data) == 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_use_without_authenticating(self):
        client = Client()
        payload = {
            'name': 'example name',
            'json_schema': '{}'
        }
    
        response = client.post(
            reverse('generated-reports-list'),
            data=json.dumps(payload),
            content_type='application/json'
        )
    
        expected_response_message = {
            'detail': 'Authentication credentials were not provided.'
        }

        self.assertEqual(response.json(), expected_response_message)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cant_see_other_reports(self):
        client = Client()
        client.login(username='developer1', password='developerpassword123')
        GeneratedReport.objects.create(name='example name 1',
                                       created_by=User.objects.get(username='developer2'), json_schema='{}')
        GeneratedReport.objects.create(name='example name 2',
                                       created_by=User.objects.get(username='developer2'), json_schema='{}')
        
        response = client.get(
            reverse('generated-reports-list')
        )
        
        self.assertEqual(response.data, [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_update_report_not_owned(self):
        client = Client()
        client.login(username='developer1', password='developerpassword123')
        report = GeneratedReport(name='example name', created_by=User.objects.get(username='developer2'),
                                 json_schema='{}')
        report.save()
        payload = {  # Change name of report
            'name': 'a different name',
            'json_schema': '{}'
        }

        response = client.put(
            reverse('generated-reports-detail', kwargs={'pk': report.pk}),
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        expected_response_message = {
            'detail': 'You do not have permission to perform this action.'
        }

        self.assertEqual(response.json(), expected_response_message)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
