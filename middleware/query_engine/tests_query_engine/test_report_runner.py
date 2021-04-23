# from middleware.report_generator.src.active_report import ActiveReport
# from middleware.query_engine import report_runner as qry

# from os.path import exists
# from unittest import TestCase, mock
# import os


# class TestGetUserInput(TestCase):
#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_get_user_input(self, mocked_input):
#         mocked_input.side_effect = ["input"]

#         value = qry.get_user_input("enter: ")

#         self.assertEqual("input", value)


# class TestGetUserInputAsList(TestCase):
#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_get_user_input_list_single_value(self, mocked_input):
#         mocked_input.side_effect = ["1"]

#         value = qry.get_user_input_as_list("seperate by commas: ")

#         self.assertEqual(["1"], value)

#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_get_user_input_list_multiple_values(self, mocked_input):
#         mocked_input.side_effect = ["1, 2, 3"]

#         value = qry.get_user_input_as_list("seperate by commas: ")

#         self.assertEqual(["1", "2", "3"], value)

#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_get_user_input_list_trailing_comma(self, mocked_input):
#         mocked_input.side_effect = ["1, 2, "]

#         value = qry.get_user_input_as_list("seperate by commas: ")

#         self.assertEqual(["1", "2"], value)


# class TestBasicRequest(TestCase):
#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_basic_returns_dict_of_user_input(self, mocked_input):
#         mocked_input.side_effect = ["cik", "2010", "type"]

#         valid_request = {"cik": "cik", "years": [
#             "2010"], "report_type": "type"}

#         value = qry.basic_request()

#         self.assertEqual(valid_request, value)


# class TestIsError(TestCase):
#     def test_is_error_true_when_error(self):
#         error = {"error": "msg"}

#         value = qry.is_error_response(error)

#         self.assertTrue(value)

#     def test_is_error_false_when_no_error(self):
#         response = {"report": "msg"}

#         value = qry.is_error_response(response)

#         self.assertFalse(value)


# class TestGetRowsForSheets(TestCase):
#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_get_rows_for_sheets_maps_single_sheet_to_single_row(self, mocked_input):
#         mocked_input.side_effect = ["1"]
#         sheets = ["test"]
#         valid = {"test": ["1"]}

#         value = qry.get_rows_for_sheets(sheets)

#         self.assertEqual(valid, value)

#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_get_rows_for_sheets_maps_single_sheet_to_multiple_rows(self, mocked_input):
#         mocked_input.side_effect = ["1, 2, 3"]
#         sheets = ["test"]
#         valid = {"test": ["1", "2", "3"]}

#         value = qry.get_rows_for_sheets(sheets)

#         self.assertEqual(valid, value)

#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_get_rows_for_sheets_maps_multiple_sheets_to_single_rows(self, mocked_input):
#         mocked_input.side_effect = ["1", "2", "3"]
#         sheets = ["test1", "test2", "test3"]
#         valid = {"test1": ["1"], "test2": ["2"], "test3": ["3"]}

#         value = qry.get_rows_for_sheets(sheets)

#         self.assertEqual(valid, value)

#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_get_rows_for_sheets_maps_multiple_sheets_to_multiple_rows(self, mocked_input):
#         mocked_input.side_effect = ["1, 2, 3", "4, 5, 6", "7, 8, 9"]
#         sheets = ["test1", "test2", "test3"]
#         valid = {"test1": ["1", "2", "3"], "test2": [
#             "4", "5", "6"], "test3": ["7", "8", "9"]}

#         value = qry.get_rows_for_sheets(sheets)

#         self.assertEqual(valid, value)


# class TestGetUserFolderPath(TestCase):
#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_get_user_folder_path_valid_with_slash(self, mocked_input):
#         directory = './../'
#         mocked_input.side_effect = [directory]

#         result = qry.get_user_folder_path()
#         self.assertEqual(directory, result)

#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_get_user_folder_path_valid_without_slash(self, mocked_input):
#         directory = './..'
#         mocked_input.side_effect = [directory]

#         result = qry.get_user_folder_path()
#         self.assertEqual(directory + '/', result)

#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_get_user_folder_path_invalid_then_valid(self, mocked_input):
#         directory_one = ' '
#         directory_two = './..'
#         mocked_input.side_effect = [directory_one, directory_two]

#         result = qry.get_user_folder_path()
#         self.assertEqual(directory_two + '/', result)


# class TestChooseJsonOrXlsx(TestCase):
#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_choose_json_or_xlsx_as_xlsx(self, mocked_input):
#         mocked_input.side_effect = ["xlsx"]

#         result = qry.choose_json_or_xlsx()
#         self.assertEqual(".xlsx", result)

#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_choose_json_or_xlsx_invalid_then_xlsx(self, mocked_input):
#         mocked_input.side_effect = ["invalid", "xlsx"]

#         result = qry.choose_json_or_xlsx()
#         self.assertEqual(".xlsx", result)

#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_choose_json_or_xlsx_as_json(self, mocked_input):
#         mocked_input.side_effect = ["json"]

#         result = qry.choose_json_or_xlsx()
#         self.assertEqual(".json", result)

#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_choose_json_or_xlsx_invalid_then_json(self, mocked_input):
#         mocked_input.side_effect = ["invalid", "json"]

#         result = qry.choose_json_or_xlsx()
#         self.assertEqual(".json", result)


# class TestGetValidFileName(TestCase):
#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_get_valid_file_name_valid_input(self, mocked_input):
#         mocked_input.side_effect = ["im-a_File09"]

#         result = qry.get_valid_file_name()
#         self.assertEqual(result, "im-a_File09")

#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_get_valid_file_name_invalid_then_valid_input(self, mocked_input):
#         mocked_input.side_effect = ["$", "im-a_File09"]

#         result = qry.get_valid_file_name()
#         self.assertEqual(result, "im-a_File09")


# class TestCanSaveToLocation(TestCase):
#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_can_save_to_location_when_doesnt_exist(self, mocked_input):
#         mocked_input.side_effect = ["im-a_File09"]

#         result = qry.can_save_to_location("im-aFile089")
#         self.assertTrue(result)

#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_can_save_to_location_when_does_exist(self, mocked_input):
#         mocked_input.side_effect = ["y"]

#         result = qry.can_save_to_location(
#             "Backend/ReportGenerator/Toplevel/UserReports/test/test.json")
#         self.assertTrue(result)


# class TestSaveUserReport(TestCase):
#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_save_json_report(self, mocked_input):
#         mocked_input.side_effect = ['Username/', "test", "json"]

#         report = ActiveReport.from_year("0000010329", "2020", "10-K")

#         file_loc = qry.save_report_locally(report.json)

#         self.assertTrue(exists(file_loc))
#         os.remove(file_loc)

#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_save_xlsx_report(self, mocked_input):
#         mocked_input.side_effect = ['Username/', "test", "xlsx"]

#         report = ActiveReport.from_year("0000010329", "2020", "10-K")

#         file_loc = qry.save_report_locally(report.json)

#         self.assertTrue(exists(file_loc))
#         os.remove(file_loc)


# class TestStartReportRetrieval(TestCase):
#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_input_done(self, mocked_input):
#         mocked_input.side_effect = ["done"]
#         qry.start_report_retrieval()

#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_input_invalid_then_done(self, mocked_input):
#         mocked_input.side_effect = ["invalid", "done"]
#         qry.start_report_retrieval()

#     @mock.patch(qry.__name__ + '.input', create=True)
#     def test_input_valid(self, mocked_input):
#         mocked_input.side_effect = ["1"]

#         try:
#             qry.start_report_retrieval()
#         except Exception:
#             print("")
