from django.core.exceptions import ObjectDoesNotExist
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
            {'Document And Entity Information': {'Nov. 28, 2015 - 12 Months Ended': {'Entity Registrant Name': 'BASSETT FURNITURE INDUSTRIES INC', 'Entity Central Index Key': 10329}, 'Jan. 08, 2016': {'Entity Registrant Name': None, 'Entity Central Index Key': None}, 'May. 30, 2015': {'Entity Registrant Name': None, 'Entity Central Index Key': None}}},
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
            {'CONSOLIDATED STATEMENTS OF INCOME': {'Dec. 31, 2016 - 12 Months Ended': {'Revenue': 27638000000.0, 'Costs and expenses: - CATEGORY': 0.0, 'Cost of revenue': 3789000000.0}, 'Dec. 31, 2015 - 12 Months Ended': {'Revenue': 17928000000.0, 'Costs and expenses: - CATEGORY': 0.0, 'Cost of revenue': 2867000000.0}, 'Dec. 31, 2014 - 12 Months Ended': {'Revenue': 12466000000.0, 'Costs and expenses: - CATEGORY': 0.0, 'Cost of revenue': 2153000000.0}, 'Dec. 31, 2013 - 12 Months Ended': {'Revenue': 7872000000.0, 'Costs and expenses: - CATEGORY': 0.0, 'Cost of revenue': 1875000000.0}}},
            json.loads(GeneratedReport.objects.get(name='test report').json_schema)
        )


class TestValidateAnalysisRequest(TestCase):
    def setUp(self):
        User.objects.create_user('developer1', 'developer1@example.com',
                                 'developerpassword123')
        User.objects.create_user('developer2', 'developer2@example.com',
                                 'developerpassword456')
        User.objects.create_user('admin', 'admin@example.com', 'admin')

        admin = User.objects.get(username='admin')
        admin.is_superuser = True
        admin.save()

        utils.get_sheets_and_rows(
            User.objects.get(username='developer2'),
            'test report',
            'Facebook',
            '1326801',
            '2016,2017'
        )

        utils.create_generated_report(
            User.objects.get(username='developer2'),
            'test report',
            json.dumps({'CONSOLIDATED STATEMENTS OF INCOME': [0, 1, 2]}),
            'json'
        )

    def test_validate_request_valid_input(self):
        request_simple = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_id': 1,
                'json_schema': json.dumps({
                    'sheet1': ['row1', 'row2']
                })
            }
        )

        request_id_is_int_string = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_id': '1',
                'json_schema': json.dumps({
                    'sheet1': ['row1', 'row2']
                })
            }
        )

        self.assertTrue(utils.validate_analysis_request(request_simple))
        self.assertTrue(utils.validate_analysis_request(request_id_is_int_string))

    def test_validate_request_invalid_user(self):
        user_is_none = MockedRequest(
            None,
            {
                'report_id': 1,
                'json_schema': json.dumps({
                    'sheet1': ['row1', 'row2']
                })
            }
        )

        self.assertFalse(utils.validate_analysis_request(user_is_none)[0])

    def test_validate_request_invalid_report_id(self):

        id_is_dict = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_id': {},
                'json_schema': json.dumps({
                    'sheet1': ['row1', 'row2']
                })
            }
        )

        id_is_list = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_id': [],
                'json_schema': json.dumps({
                    'sheet1': ['row1', 'row2']
                })
            }
        )

        id_is_none = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_id': None,
                'json_schema': json.dumps({
                    'sheet1': ['row1', 'row2']
                })
            }
        )

        id_is_string_not_int = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_id': "string",
                'json_schema': json.dumps({
                    'sheet1': ['row1', 'row2']
                })
            }
        )

        id_is_float_string = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_id': "1.5",
                'json_schema': json.dumps({
                    'sheet1': ['row1', 'row2']
                })
            }
        )

        id_is_tuple = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_id': (1, 1),
                'json_schema': json.dumps({
                    'sheet1': ['row1', 'row2']
                })
            }
        )

        self.assertFalse(utils.validate_analysis_request(id_is_none)[0])
        self.assertFalse(utils.validate_analysis_request(id_is_dict)[0])
        self.assertFalse(utils.validate_analysis_request(id_is_list)[0])
        self.assertFalse(utils.validate_analysis_request(id_is_string_not_int)[0])
        self.assertFalse(utils.validate_analysis_request(id_is_float_string)[0])
        self.assertFalse(utils.validate_analysis_request(id_is_tuple)[0])

    def test_validate_request_invalid_json_schema(self):
        schema_is_missing = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_id': 1
            }
        )

        schema_is_empty = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_id': 1,
                'json_schema': {}
            }
        )

        self.assertFalse(utils.validate_analysis_request(schema_is_empty)[0])
        self.assertFalse(utils.validate_analysis_request(schema_is_missing)[0])

    def test_validate_request_invalid_request_data(self):
        data_is_empty = MockedRequest(
            User.objects.get(username='developer1'),
            {}
        )

        data_is_missing_report_id = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'json_schema': json.dumps({
                    'sheet1': ['row1', 'row2']
                })
            }
        )

        data_is_missing_report_json_schema = MockedRequest(
            User.objects.get(username='developer1'),
            {
                'report_id': '1'
            }
        )

        self.assertFalse(utils.validate_analysis_request(data_is_empty)[0])
        self.assertFalse(utils.validate_analysis_request(data_is_missing_report_id)[0])
        self.assertFalse(utils.validate_analysis_request(data_is_missing_report_json_schema)[0])


class TestRunAnalysisTests(TestCase):
    def setUp(self):
        User.objects.create_user('developer1', 'developer1@example.com',
                                 'developerpassword123')
        User.objects.create_user('developer2', 'developer2@example.com',
                                 'developerpassword456')
        User.objects.create_user('admin', 'admin@example.com', 'admin')

        admin = User.objects.get(username='admin')
        admin.is_superuser = True
        admin.save()

        utils.get_sheets_and_rows(
            User.objects.get(username='developer1'),
            'test report',
            'Facebook',
            '1326801',
            '2016,2017'
        )

        utils.create_generated_report(
            User.objects.get(username='developer1'),
            'test report',
            json.dumps({'CONSOLIDATED STATEMENTS OF INCOME': [0, 1, 2]}),
            'json'
        )

    def test_run_analysis_valid(self):
        report_id = utils.run_analysis(
            user=User.objects.get(username='developer1'),
            report_id=1
        )

        self.assertEqual(1, report_id)

    def test_run_analysis_incorrect_user(self):
        self.assertRaises(ObjectDoesNotExist,
                          utils.run_analysis,
                          user=User.objects.get(username='developer2'),
                          report_id=1)

    def test_run_analysis_incorrect_report_id(self):
        self.assertRaises(ObjectDoesNotExist,
                          utils.run_analysis,
                          user=User.objects.get(username='developer1'),
                          report_id=3)

    def test_run_analysis_already_ran_false(self):
        user = User.objects.get(username='developer1')
        report_id = 1

        report = GeneratedReport.objects.get(pk=report_id, created_by=user)
        report_data = json.loads(report.json_schema)

        self.assertFalse(utils.analysis_already_ran(report_data))

    def test_run_analysis_already_ran_true(self):
        user = User.objects.get(username='developer1')
        report_id = 1

        utils.run_analysis(user, report_id)

        report = GeneratedReport.objects.get(pk=report_id, created_by=user)
        report_data = json.loads(report.json_schema)

        self.assertTrue(utils.analysis_already_ran(report_data))
