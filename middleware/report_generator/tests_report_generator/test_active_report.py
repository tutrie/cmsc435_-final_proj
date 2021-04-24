# from middleware.report_generator.src.active_report import ActiveReport
# from unittest import TestCase


# class TestActiveReportFromYear(TestCase):
#     def test_from_year_single_year(self):
#         cik = '0000010329'
#         year = '2020'
#         report_type = '10-K'

#         active_report = ActiveReport.from_year(cik, year, report_type)

#         self.assertIsInstance(active_report.json, dict)
#         self.assertIsInstance(active_report.dataframes, dict)

#     def test_from_year_multiple_years(self):
#         cik = '0000010329'
#         years = ['2019', '2020']
#         report_type = '10-K'

#         active_report = ActiveReport.from_year_list(cik, years, report_type)

#         self.assertIsInstance(active_report.json, dict)
#         self.assertIsInstance(active_report.dataframes, dict)


# class TestActiveReportFilterReport(TestCase):
#     def test_filter_report_with_instructions(self):
#         instructions = {
#             "Document And Entity Information": [1, 2, 3, 4, 5],
#             "Consolidated Balance Sheets": [1, 2, 3, 4],
#             "Consolidated Statements of Stockholders' Equity (Parentheticals)":
#                 [0, 1, 2]
#         }

#         cik = '0000010329'
#         year = '2020'
#         report_type = '10-K'

#         active_report = ActiveReport.from_year(cik, year, report_type)

#         active_report.filter_report(instructions)

#         generated_report = active_report.generated_report

#         # Check to see if number of sheets requested
#         # is the number of sheets returned
#         self.assertEqual(3, len(generated_report.keys()))

#         for sheet_name, row_list in instructions.items():

#             # Check to see if sheets requested are in the generated report.
#             self.assertTrue(sheet_name in generated_report)

#             # Check to see if number of filtered value match
#             # up with length of row indices in instructions.
#             sheet = generated_report[sheet_name]
#             self.assertEqual(len(row_list), len(sheet.index))

#             # Check to see if filtered values match up with instructions
#             for idx, value in zip(row_list, sheet['index']):
#                 self.assertEqual(
#                     value, active_report.json[sheet_name]['index'][str(idx)]
#                 )
