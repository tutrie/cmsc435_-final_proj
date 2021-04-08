from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
import json

from .models import Company
from .serializers import CompanySerializer


class CompanyAPITest(TestCase):
    def test_can_create_company(self):
        Company.objects.create(
            name='Google',
            cik='123456'
        )

        self.assertTrue(Company.objects.all())

    def test_can_retrieve_company(self):
        company = Company(name='Google', cik='123456')
        company.save()

        retrieved_company = Company.objects.get(name='Google')

        self.assertEqual(str(company), str(retrieved_company))

    def test_can_delete_company(self):
        company = Company(name='Google', cik='123456')
        company.save()

        Company.objects.get(name='Google').delete()

        self.assertFalse(Company.objects.all())

    def test_get_valid_company(self):
        client = Client()
        company_to_get = Company.objects.create(
            name='Google',
            cik='123456'
        )

        response = client.get(
            reverse('companies-detail', kwargs={'pk': company_to_get.pk})
        )

        company_expected = Company.objects.get(pk=company_to_get.pk)
        serializer = CompanySerializer(company_expected)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_non_exist_company(self):
        client = Client()
        Company.objects.create(
            name='Google',
            cik='123456'
        )

        response = client.get(
            reverse('companies-detail', kwargs={'pk': 'Facebook'})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_valid_company(self):
        client = Client()
        payload = {
            'name': 'Google',
            'cik': '123456'
        }

        response = client.post(
            reverse('companies-list'),
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_invalid_company(self):
        client = Client()
        payload_1 = {
            'name': '',
            'cik': '123456'
        }
        payload_2 = {
            'name': 'Google',
            'cik': None
        }
        payload_3 = {
            'name': ['Google'],
            'cik': ['123456']
        }

        response_1 = client.post(
            reverse('companies-list'),
            data=json.dumps(payload_1),
            content_type='application/json'
        )
        response_2 = client.post(
            reverse('companies-list'),
            data=json.dumps(payload_2),
            content_type='application/json'
        )
        response_3 = client.post(
            reverse('companies-list'),
            data=json.dumps(payload_3),
            content_type='application/json'
        )

        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_3.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_valid_company(self):
        client = Client()
        initial_company = Company.objects.create(
            name='Google',
            cik='123456'
        )
        payload = {
            'name': 'Microsoft',
            'cik': '123456'
        }

        response = client.put(
            reverse('companies-detail', kwargs={'pk': initial_company.pk}),
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(str(Company.objects.get(pk='Microsoft')), 'Microsoft')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_invalid_company(self):
        client = Client()
        initial_company = Company.objects.create(
            name='Google',
            cik='123456'
        )
        payload_1 = {
            'name': '',
            'cik': '123456'
        }
        payload_2 = {
            'name': 'Google',
            'cik': None
        }
        payload_3 = {
            'name': ['Google'],
            'cik': ['123456']
        }

        response_1 = client.put(
            reverse('companies-detail', kwargs={'pk': initial_company.pk}),
            data=json.dumps(payload_1),
            content_type='application/json'
        )
        response_2 = client.put(
            reverse('companies-detail', kwargs={'pk': initial_company.pk}),
            data=json.dumps(payload_2),
            content_type='application/json'
        )
        response_3 = client.put(
            reverse('companies-detail', kwargs={'pk': initial_company.pk}),
            data=json.dumps(payload_3),
            content_type='application/json'
        )

        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_3.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_existing_company(self):
        client = Client()
        initial_company = Company.objects.create(
            name='Google',
            cik='123456'
        )

        response = client.delete(
            reverse('companies-detail', kwargs={'pk': initial_company.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_not_exist_company(self):
        client = Client()
        Company.objects.create(
            name='Google',
            cik='123456'
        )

        response = client.delete(
            reverse('companies-detail', kwargs={'pk': 10})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
