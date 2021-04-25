#from middleware.report_generator.src.active_report import ActiveReport
from middleware.query_engine import report_runner as qry
import pandas as pd
from os import remove
from os.path import exists
from unittest import TestCase
from unittest.mock import patch


@patch(qry.__name__ + '.input', create=True)
class TestGetUserInput(TestCase):
    def test_get_user_input(self, mocked_input):
        mocked_input.side_effect = ['input']

        value = qry.get_user_input('enter: ')

        self.assertEqual('input', value)


@patch(qry.__name__ + '.input', create=True)
class TestGetUserInputAsList(TestCase):
    def test_get_user_input_list_single_value(self, mocked_input):
        mocked_input.side_effect = ['1']

        value = qry.get_user_input_as_list('seperate by commas: ')

        self.assertEqual(['1'], value)

    def test_get_user_input_list_multiple_values(self, mocked_input):
        mocked_input.side_effect = ['1, 2, 3']

        value = qry.get_user_input_as_list('seperate by commas: ')

        self.assertEqual(['1', '2', '3'], value)

    def test_get_user_input_list_trailing_comma(self, mocked_input):
        mocked_input.side_effect = ["1, 2, "]

        value = qry.get_user_input_as_list("seperate by commas: ")

        self.assertEqual(["1", "2"], value)


class TestBasicRequest(TestCase):
    @patch(qry.__name__ + '.input', create=True)
    def test_basic_returns_dict_of_user_input(self, mocked_input):
        mocked_input.side_effect = ["Bassett", "00", "2010"]

        valid_request = {"company": "Bassett", "cik": '00', "years": ["2010"]}

        value = qry.basic_request()

        self.assertEqual(valid_request, value)


@patch(qry.__name__ + '.input', create=True)
class TestIsError(TestCase):
    def test_is_error_true_when_error(self, mocked_input: patch):
        # , mock_stdout: patch):

        mocked_input.side_effect = ["Bassett", "00", "2010"]
        value = qry.query_raw_report_api()

        #print('Captured', mock_stdout.getvalue())

        #print(value.keys())

        self.assertEqual(value, None)

    def test_is_error_false_when_no_error(self, mocked_input: patch):
        mocked_input.side_effect = ["Bassett", "0000010329", "2016"]
        value = qry.query_raw_report_api()
        good_response = {'company': None, 'cik': None, 'reports': None}

        self.assertEqual(good_response.keys(), value.keys())


@patch(qry.__name__ + '.input', create=True)
class TestGetRowsForSheets(TestCase):
    def test_get_rows_for_sheets_maps_single_sheet_to_single_row(self, mocked_input):
        mocked_input.side_effect = ["0"]
        sheets = pd.DataFrame(data={"test": ["1"]})
        valid = [0]

        value = qry.choose_rows_in_sheet("test", sheets)

        self.assertEqual(valid, value)

    def test_get_rows_for_sheets_maps_single_sheet_to_multiple_rows(self, mocked_input):
        mocked_input.side_effect = ["0, 1, 2"]
        sheets = pd.DataFrame(data={"test": ["1", "2", "2"]})
        valid = [0, 1, 2]

        value = qry.choose_rows_in_sheet("test", sheets)

        self.assertEqual(valid, value)

#    @patch(qry.__name__ + '.input', create=True)
#    def test_get_rows_for_sheets_maps_multiple_sheets_to_single_rows(self, mocked_input):
#        mocked_input.side_effect = ["1", "2", "3"]
#        sheets = ["test1", "test2", "test3"]
#       valid = {"test1": ["1"], "test2": ["2"], "test3": ["3"]}

#        value = qry.get_rows_for_sheets(sheets)

#        self.assertEqual(valid, value)

#    @patch(qry.__name__ + '.input', create=True)
#    def test_get_rows_for_sheets_maps_multiple_sheets_to_multiple_rows(self, mocked_input):
#        mocked_input.side_effect = ["1, 2, 3", "4, 5, 6", "7, 8, 9"]
#        sheets = ["test1", "test2", "test3"]
#        valid = {"test1": ["1", "2", "3"], "test2": [
#            "4", "5", "6"], "test3": ["7", "8", "9"]}

#        value = qry.get_rows_for_sheets(sheets)

 #       self.assertEqual(valid, value)


@patch(qry.__name__ + '.input', create=True)
class TestGetUserFolderPath(TestCase):
    def test_get_user_folder_path_valid_with_slash(self, mocked_input):
        directory = './../'
        mocked_input.side_effect = [directory]

        result = qry.get_user_folder_path()
        self.assertEqual(directory, result)

    def test_get_user_folder_path_valid_without_slash(self, mocked_input):
        directory = './..'
        mocked_input.side_effect = [directory]

        result = qry.get_user_folder_path()
        self.assertEqual(directory + '/', result)

    def test_get_user_folder_path_invalid_then_valid(self, mocked_input):
        directory_one = ' '
        directory_two = './..'
        mocked_input.side_effect = [directory_one, directory_two]

        result = qry.get_user_folder_path()
        self.assertEqual(directory_two + '/', result)


@patch(qry.__name__ + '.input', create=True)
class TestChooseJsonOrXlsx(TestCase):
    def test_choose_json_or_xlsx_as_xlsx(self, mocked_input):
        mocked_input.side_effect = ['xlsx']

        result = qry.choose_json_or_xlsx()
        self.assertEqual('.xlsx', result)

    def test_choose_json_or_xlsx_invalid_then_xlsx(self, mocked_input):
        mocked_input.side_effect = ['invalid', 'xlsx']

        result = qry.choose_json_or_xlsx()
        self.assertEqual('.xlsx', result)

    def test_choose_json_or_xlsx_as_json(self, mocked_input):
        mocked_input.side_effect = ['json']

        result = qry.choose_json_or_xlsx()
        self.assertEqual('.json', result)

    def test_choose_json_or_xlsx_invalid_then_json(self, mocked_input):
        mocked_input.side_effect = ['invalid', 'json']

        result = qry.choose_json_or_xlsx()
        self.assertEqual('.json', result)


@patch(qry.__name__ + '.input', create=True)
class TestGetValidFileName(TestCase):
    def test_get_valid_file_name_valid_input(self, mocked_input):
        mocked_input.side_effect = ['im-a_File09']

        result = qry.get_valid_file_name()
        self.assertEqual(result, 'im-a_File09')

    def test_get_valid_file_name_invalid_then_valid_input(self, mocked_input):
        mocked_input.side_effect = ['$', 'im-a_File09']

        result = qry.get_valid_file_name()
        self.assertEqual(result, 'im-a_File09')



@patch(qry.__name__ + '.input', create=True)
class TestCanSaveToLocation(TestCase):
    def test_can_save_to_location_when_doesnt_exist(self, mocked_input):
        mocked_input.side_effect = ["im-a_File09"]

        result = qry.can_save_to_location("im-aFile089")
        self.assertTrue(result)

    def test_can_save_to_location_when_does_exist(self, mocked_input):
        mocked_input.side_effect = ["y"]

        result = qry.can_save_to_location(
            "Backend/ReportGenerator/Toplevel/UserReports/test/test.json")
        self.assertTrue(result)


class TestCanQueryAndSaveRawReport(TestCase):
    @patch(qry.__name__ + '.input', create=True)
    def test_save_json_report(self, mocked_input):
        mocked_input.side_effect = ['Bassett', "0000010329", "2020", 'test', 'test', 'json']
        report = qry.retrieve_raw_reports()
        file_loc = 'test/test.json'
        self.assertTrue(exists(file_loc))
        remove(file_loc)

    @patch(qry.__name__ + '.input', create=True)
    def test_save_xlsx_report(self, mocked_input):
        mocked_input.side_effect = ['Bassett', "0000010329", "2020", 'test', 'test', 'xlsx']
        report = qry.retrieve_raw_reports()
        file_loc = 'test/test.xlsx'
        self.assertTrue(exists(file_loc))
        remove(file_loc)


@patch(qry.__name__ + '.input', create=True)
class TestStartReportRetrieval(TestCase):
    def test_input_done(self, mocked_input):
        mocked_input.side_effect = ["done"]
        qry.start_report_retrieval()

    def test_input_invalid_then_done(self, mocked_input):
        mocked_input.side_effect = ["invalid", "done"]
        qry.start_report_retrieval()

    def test_input_valid(self, mocked_input):
        mocked_input.side_effect = ["1"]

        try:
            qry.start_report_retrieval()
        except Exception:
            print("")

class TestChooseSheetNames(TestCase):
    @patch(qry.__name__ + '.input', create=True)
    def test_choose_sheet_names_success(self, mocked_input):
        mocked_input.side_effect = ['1, 2, 3']

