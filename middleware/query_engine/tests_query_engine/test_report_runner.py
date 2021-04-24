from middleware.query_engine import report_runner as qry

from unittest import TestCase, mock
import os


class TestGetUserInput(TestCase):
    @mock.patch(qry.__name__ + '.input', create=True)
    def test_get_user_input(self, mocked_input):
        mocked_input.side_effect = ['input']

        value = qry.get_user_input('enter: ')

        self.assertEqual('input', value)


class TestGetUserInputAsList(TestCase):
    @mock.patch(qry.__name__ + '.input', create=True)
    def test_get_user_input_list_single_value(self, mocked_input):
        mocked_input.side_effect = ['1']

        value = qry.get_user_input_as_list('seperate by commas: ')

        self.assertEqual(['1'], value)

    @mock.patch(qry.__name__ + '.input', create=True)
    def test_get_user_input_list_multiple_values(self, mocked_input):
        mocked_input.side_effect = ['1, 2, 3']

        value = qry.get_user_input_as_list('seperate by commas: ')

        self.assertEqual(['1', '2', '3'], value)

    @mock.patch(qry.__name__ + '.input', create=True)
    def test_get_user_input_list_trailing_comma(self, mocked_input):
        mocked_input.side_effect = ['1, 2, ']

        value = qry.get_user_input_as_list('seperate by commas: ')

        self.assertEqual(['1', '2'], value)


class TestGetUserIntList(TestCase):
    @mock.patch(qry.__name__ + '.input', create=True)
    def test_get_user_int_list_single_value(self, mocked_input):
        mocked_input.side_effect = ['1']

        target = [1, 2, 3]
        value = qry.get_user_int_list(target)

        self.assertEqual([1], value)

    @mock.patch(qry.__name__ + '.input', create=True)
    def test_get_user_int_list_multiple_values(self, mocked_input):
        mocked_input.side_effect = ['1, 2, 3']

        target = [1, 2, 3]
        value = qry.get_user_int_list(target)

        self.assertEqual([1, 2, 3], value)

    @mock.patch(qry.__name__ + '.input', create=True)
    def test_get_user_int_list_invalid_then_valid(self, mocked_input):
        mocked_input.side_effect = ['1, 2, 3, 4', '1, 2']

        target = [1, 2, 3]
        value = qry.get_user_int_list(target)

        self.assertEqual([1, 2], value)


class TestSaveJson(TestCase):
    def test_save_json_success(self):
        report = {
            'line1': 'I am a data value!'
        }
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        output_file_path = os.path.join(curr_dir, 'test-save-json.json')

        qry.save_json(report, output_file_path)

        self.assertTrue(os.path.isfile(output_file_path))
        os.remove(output_file_path)


class TestSaveExcel(TestCase):
    def test_save_excel_success(self):
        report = {
            'sheet1': {
                'index': {
                    'row1': 'I am a data value!'
                }
            }
        }
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        output_file_path = os.path.join(curr_dir, 'test-save-excel.xlsx')

        qry.save_xlsx(report, output_file_path)

        self.assertTrue(os.path.isfile(output_file_path))
        os.remove(output_file_path)


class TestCanSaveToLocation(TestCase):
    def test_can_save_to_location_new_file_path(self):
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        output_file_path = os.path.join(curr_dir, 'test.json')
        answer = qry.can_save_to_location(output_file_path)
        self.assertTrue(answer)

    @mock.patch(qry.__name__ + '.input', create=True)
    def test_can_save_to_location_yes_overwrite(self, mocked_input):
        mocked_input.side_effect = ['y']

        report = {
            'line1': {
                'row1': 'data1'
            }
        }
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        output_file_path = os.path.join(curr_dir, 'test.json')

        qry.save_json(report, output_file_path)

        answer = qry.can_save_to_location(output_file_path)

        self.assertTrue(answer)
        os.remove(output_file_path)

    @mock.patch(qry.__name__ + '.input', create=True)
    def test_can_save_to_location_no_overwrite(self, mocked_input):
        mocked_input.side_effect = ['n']

        report = {
            'line1': 'I am a data value!'
        }
        curr_dir = os.path.dirname(os.path.realpath(__file__))
        output_file_path = os.path.join(curr_dir, 'test-save-to-loc.json')

        qry.save_json(report, output_file_path)

        answer = qry.can_save_to_location(output_file_path)

        self.assertFalse(answer)
        os.remove(output_file_path)


class TestChooseJsonOrXlsx(TestCase):
    @mock.patch(qry.__name__ + '.input', create=True)
    def test_choose_json_or_xlsx_as_xlsx(self, mocked_input):
        mocked_input.side_effect = ['xlsx']

        result = qry.choose_json_or_xlsx()
        self.assertEqual('.xlsx', result)

    @mock.patch(qry.__name__ + '.input', create=True)
    def test_choose_json_or_xlsx_invalid_then_xlsx(self, mocked_input):
        mocked_input.side_effect = ['invalid', 'xlsx']

        result = qry.choose_json_or_xlsx()
        self.assertEqual('.xlsx', result)

    @mock.patch(qry.__name__ + '.input', create=True)
    def test_choose_json_or_xlsx_as_json(self, mocked_input):
        mocked_input.side_effect = ['json']

        result = qry.choose_json_or_xlsx()
        self.assertEqual('.json', result)

    @mock.patch(qry.__name__ + '.input', create=True)
    def test_choose_json_or_xlsx_invalid_then_json(self, mocked_input):
        mocked_input.side_effect = ['invalid', 'json']

        result = qry.choose_json_or_xlsx()
        self.assertEqual('.json', result)


class TestGetValidFileName(TestCase):
    @mock.patch(qry.__name__ + '.input', create=True)
    def test_get_valid_file_name_valid_input(self, mocked_input):
        mocked_input.side_effect = ['im-a_File09']

        result = qry.get_valid_file_name()
        self.assertEqual(result, 'im-a_File09')

    @mock.patch(qry.__name__ + '.input', create=True)
    def test_get_valid_file_name_invalid_then_valid_input(self, mocked_input):
        mocked_input.side_effect = ['$', 'im-a_File09']

        result = qry.get_valid_file_name()
        self.assertEqual(result, 'im-a_File09')


class TestGetUserFolderPath(TestCase):
    @mock.patch(qry.__name__ + '.input', create=True)
    def test_get_user_folder_path_valid_path(self, mocked_input):
        mocked_input.side_effect = [os.getcwd()]

        output = qry.get_user_folder_path()
        self.assertEqual(output, os.getcwd() + '/')

    @mock.patch(qry.__name__ + '.input', create=True)
    def test_get_user_folder_path_invalid_then_valid_path(self, mocked_input):
        mocked_input.side_effect = ['393wjsdfsd', os.getcwd()]

        output = qry.get_user_folder_path()
        self.assertEqual(output, os.getcwd() + '/')


class TestSaveSingleReport(TestCase):
    @mock.patch(qry.__name__ + '.input', create=True)
    def test_save_single_report_success(self, mocked_input):
        mocked_input.side_effect = [
            os.path.dirname(os.path.realpath(__file__)),
            'test-save-single-report',
            'json'
        ]

        report_dict = {
            'test': 'test-save-single-report-success'
        }
        qry.save_single_report(report_dict)

        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                 'test-save-single-report.json')

        self.assertTrue(os.path.isfile(file_path))
        os.remove(file_path)


class TestMultipleReports(TestCase):
    @mock.patch(qry.__name__ + '.input', create=True)
    def test_save_multi_report_success(self, mocked_input):
        mocked_input.side_effect = [
            os.path.dirname(os.path.realpath(__file__)),
            'test-save-multi-report-1',
            'json',
            os.path.dirname(os.path.realpath(__file__)),
            'test-save-multi-report-2',
            'json'
        ]

        reports = {
            '2015': {
                'report_dict1': 'val1'
            },
            '2016': {
                'report_dict2': 'val2'
            }
        }
        qry.save_multiple_reports_locally(reports)

        file_path_1 = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test-save-multi-report-1.json')
        self.assertTrue(os.path.isfile(file_path_1))
        os.remove(file_path_1)

        file_path_2 = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test-save-multi-report-2.json')
        self.assertTrue(os.path.isfile(file_path_2))
        os.remove(file_path_2)


class TestIsErrorResponse(TestCase):
    class Response():
        def __init__(self, status_code: int):
            self.status_code = status_code

    def test_is_error_response_false(self):
        self.assertFalse(qry.is_error_response(self.Response(200)))

    def test_is_error_response_true(self):
        self.assertTrue(qry.is_error_response(self.Response(400)))


class TestBasicRequest(TestCase):
    @mock.patch(qry.__name__ + '.input', create=True)
    def test_basic_returns_dict_of_user_input(self, mocked_input):
        mocked_input.side_effect = ['myCompany', '123456789', '2016, 2017']

        valid_request = {
            'company': 'myCompany',
            'cik': '123456789',
            'years': ['2016', '2017']
        }

        value = qry.basic_request()

        self.assertEqual(valid_request, value)


class TestQueryRawReportApi(TestCase):
    @mock.patch(qry.__name__ + '.input', create=True)
    def test_query_raw_report_api_returns_reports(self, mocked_input):
        mocked_input.side_effect = ['Basset', '0000010329', '2016, 2017']

        result = qry.query_raw_report_api()

        self.assertEqual(result['company'], 'Basset')
        self.assertEqual(result['cik'], '0000010329')
        self.assertEqual(
            sorted(list(result['reports'].keys())), ['2016', '2017']
        )


class TestChooseRowsInSheet(TestCase):
    @mock.patch(qry.__name__ + '.input', create=True)
    def test_choose_rows_in_sheet_success(self, mocked_input):
        mocked_input.side_effect = ['1, 2, 3']

        to_keep = qry.choose_rows_in_sheet(
            'test-sheet', {'index': {1: 1, 2: 2, 3: 3, 4: 4}})
        self.assertEqual(to_keep, [1, 2, 3])


class TestChooseSheetNames(TestCase):
    @mock.patch(qry.__name__ + '.input', create=True)
    def test_choose_sheet_names_success(self, mocked_input):
        mocked_input.side_effect = ['1, 2, 3']
