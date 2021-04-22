from report_schema.raw_report.report_cleaner.excelToPandasToJson import (
    ConvertCleanSave
)
from os.path import dirname, realpath
import unittest

# # For production:
# file_path = '~' + '/downloaded_reports/'

# For development:
file_path = dirname(realpath(__file__)).replace(
    'report_schema/raw_report', 'downloaded_reports/') + '10-K-20.xlsx'


class TestReportCleaner(unittest.TestCase):
    def test_CleanedExcelReport_notes(self):
        test_object = ConvertCleanSave(file_path)
        self.assertEqual(8, len(test_object.notes.keys()))

    def test_CleanedExcelReport_original(self):
        # 97 sheets in OG 10-k-20 report
        test_object = ConvertCleanSave(file_path)
        self.assertEqual(97, len(test_object.excel_report.sheetnames))

    def test_CleanedExcelReport_cleaned(self):
        # 97 sheets in OG 10-k-20 report
        test_object = ConvertCleanSave(file_path)
        self.assertEqual(8, len(test_object.cleaned_excel_report.sheetnames))
