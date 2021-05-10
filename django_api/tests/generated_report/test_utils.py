from django.test import TestCase
from django.contrib.auth.models import User
import json

from report_schema.generated_report.models import GeneratedReport
from report_schema.generated_report import utils
from tests.mocks import MockedRequest

class GenReportUtilTests(TestCase):
    def setUp(self):
        User.objects.create_user('developer1', 'developer1@example.com', 'developerpassword123')
        User.objects.create_user('developer2', 'developer2@example.com', 'developerpassword456')
        User.objects.create_user('admin', 'admin@example.com', 'admin')
        
        admin = User.objects.get(username='admin')
        admin.is_superuser = True
        admin.save()

    def test_validate_get_form_data_request_with_valid_requests(self):
        request_1 = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_name': 'test report',
                'company': 'Bassett',
                'cik': '0000010329',
                'years': '2016,2017,2018'
            }
        )
        request_2 = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_name': 'test report 2',
                'company': 'Bassett',
                'cik': '0000010329',
                'years': '2016,2018'
            }
        )
        request_3 = MockedRequest(
            User.objects.get(username='developer2'),
            {
                'report_name': 'test report 3',
                'company': 'Bassett',
                'cik': '0000010329',
                'years': '2020'
            }
        )
        request_4 = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_name': 'test report 4',
                'company': 'Google',
                'cik': '00000103432',
                'years': '2018,2019,2020'
            }
        )

        res_1, _ = utils.validate_get_form_data_request(request_1)
        res_2, _ = utils.validate_get_form_data_request(request_2)
        res_3, _ = utils.validate_get_form_data_request(request_3)
        res_4, _ = utils.validate_get_form_data_request(request_4)

        self.assertTrue(res_1)
        self.assertTrue(res_2)
        self.assertTrue(res_3)
        self.assertTrue(res_4)
    
    def test_validate_get_form_data_request_with_invalid_requests(self):
        request_1 = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_name': 'test report',
                'company': 'Bassett',
                'cik': '0000010329',
                'years': ['2016', '2017', '2018'] # invalid years format
            }
        )
        request_2 = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_name': 'test report 2',
                'company': 'Bassett',
                'years': '2016,2018' # Missing CIK
            }
        )
        request_3 = MockedRequest(
            User.objects.get(username='developer2'),
            {
                'report_name': 'test report 3',
                'company': 'Bassett',
                'cik': 10329, # CIK not string
                'years': '2020'
            }
        )
        request_4 = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_name': 'test report 4',
                'company': 'Google',
                'cik': '00000103432',
                'years': '2012' # Inaccesible year
            }
        )

        res_1, _ = utils.validate_get_form_data_request(request_1)
        res_2, _ = utils.validate_get_form_data_request(request_2)
        res_3, _ = utils.validate_get_form_data_request(request_3)
        res_4, _ = utils.validate_get_form_data_request(request_4)

        self.assertFalse(res_1)
        self.assertFalse(res_2)
        self.assertFalse(res_3)
        self.assertFalse(res_4)

    def test_validate_get_form_data_fails_with_existing_report(self):
        GeneratedReport.objects.create(
            name='test report',
            created_by=User.objects.get(username='developer1'),
            json_schema='{}'
        )
        
        request = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_name': 'test report',
                'company': 'Bassett',
                'cik': '0000010329',
                'years': '2016,2017,2018'
            }
        )

        res, _ = utils.validate_get_form_data_request(request)
        
        self.assertFalse(res)

    def test_validate_create_report_request_with_valid_requests(self):
        GeneratedReport.objects.create(
            name='test report',
            created_by=User.objects.get(username='developer1'),
            json_schema='{}'
        )

        request_1 = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_name': 'test report',
                'form_data': json.dumps({}),
                'type': 'json',
            }
        )
        request_2 = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_name': 'test report',
                'form_data': json.dumps({}),
                'type': 'xlsx',
            }
        )
        request_3 = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_name': 'test report',
                'form_data': json.dumps({
                    'sheet1': ['row1', 'row2']
                }),
                'type': 'json',
            }
        )

        res_1, _ = utils.validate_create_report_request(request_1)
        res_2, _ = utils.validate_create_report_request(request_2)
        res_3, _ = utils.validate_create_report_request(request_3)

        self.assertTrue(res_1)
        self.assertTrue(res_2)
        self.assertTrue(res_3)
    
    def test_validate_create_report_request_with_invalid_requests(self):
        GeneratedReport.objects.create(
            name='test report',
            created_by=User.objects.get(username='developer1'),
            json_schema='{}'
        )

        request_1 = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_name': 'test report',
                'form_data': json.dumps({}),
                'type': 'xml' # type doesn't exist
            }
        )
        request_2 = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_name': 'test report',
                'type': 'xlsx' # Missing form data
            }
        )
        request_3 = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_name': ['test report'], # Wrong value type
                'form_data': json.dumps({
                    'sheet1': ['row1', 'row2']
                }),
                'type': 'json'
            }
        )

        res_1, _ = utils.validate_create_report_request(request_1)
        res_2, _ = utils.validate_create_report_request(request_2)
        res_3, _ = utils.validate_create_report_request(request_3)

        self.assertFalse(res_1)
        self.assertFalse(res_2)
        self.assertFalse(res_3)

    def test_validate_create_report_request_fails_if_report_doesnt_exist(self):
        request = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_name': 'test report', # Report doesn't exist
                'form_data': json.dumps({}),
                'type': 'json'
            }
        )

        res, _ = utils.validate_create_report_request(request)

        self.assertFalse(res)

    def test_get_sheets_and_rows_returns_form_data(self):
        form_data = utils.get_sheets_and_rows(
            User.objects.get(username='developer1'),
            'test report',
            'Bassett', # Bassett not in the database yet
            '0000010329',
            '2016' # Call with just a single year
        )

        self.assertTrue(len(form_data))
        self.assertTrue(GeneratedReport.objects.filter(name='test report'))

        form_data = utils.get_sheets_and_rows(
            User.objects.get(username='developer2'),
            'test report 2',
            'Bassett',
            '0000010329',
            '2016,2017,2018' # Call with multiple concurrent years
        )

        self.assertTrue(len(form_data))
        self.assertTrue(GeneratedReport.objects.filter(name='test report 2'))

        form_data = utils.get_sheets_and_rows(
            User.objects.get(username='developer2'),
            'test report 3',
            'Facebook',
            '1326801',
            '2018,2020' # Call with multiple non concurrent years
        )

        self.assertTrue(len(form_data))
        self.assertTrue(GeneratedReport.objects.filter(name='test report 3'))

    def test_create_generated_report_1(self):
        utils.get_sheets_and_rows(
            User.objects.get(username='developer1'),
            'test report',
            'Bassett',
            '0000010329',
            '2016'
        )

        report_id = utils.create_generated_report(
            User.objects.get(username='developer1'),
            'test report',
            json.dumps({'Document And Entity Information': [0, 1]}),
            'json'
        )

        self.assertTrue(report_id)
        self.assertEqual(
            {'Document And Entity Information': {'Nov. 28, 2015 - 12 Months Ended': {'Entity Registrant Name': 'BASSETT FURNITURE INDUSTRIES INC'}, 'Jan. 08, 2016': {'Entity Registrant Name': None}, 'May. 30, 2015': {'Entity Registrant Name': None}}},
            json.loads(GeneratedReport.objects.get(name='test report').json_schema)
        )

    def test_create_generated_report_2(self):
        utils.get_sheets_and_rows(
            User.objects.get(username='developer2'),
            'test report',
            'Facebook',
            '1326801',
            '2016,2017'
        )

        report_id = utils.create_generated_report(
            User.objects.get(username='developer2'),
            'test report',
            json.dumps({'CONSOLIDATED STATEMENTS OF INCOME': [0, 1, 2]}),
            'xlsx'
        )

        self.assertTrue(report_id)
        self.assertEqual(
            {'CONSOLIDATED STATEMENTS OF INCOME': {'Dec. 31, 2016 - 12 Months Ended': {'Revenue': 27638000000.0}, 'Dec. 31, 2015 - 12 Months Ended': {'Revenue': 17928000000.0}, 'Dec. 31, 2014 - 12 Months Ended': {'Revenue': 12466000000.0}, 'Dec. 31, 2013 - 12 Months Ended': {'Revenue': 7872000000.0}}},
            json.loads(GeneratedReport.objects.get(name='test report').json_schema)
        )
