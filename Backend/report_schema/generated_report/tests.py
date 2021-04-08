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
