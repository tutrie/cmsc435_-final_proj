from report_schema.raw_report.report_cleaner.excelToPandasToJson import (
    ConvertCleanSave
)
from os.path import dirname, realpath
import unittest
import sys

# # For production:
# file_path = '~' + '/downloaded_reports/'

# For development:

if sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
    file_path = dirname(realpath(__file__)).replace(
        'report_schema/raw_report/tests', 'downloaded_reports/')
elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
    file_path = dirname(realpath(__file__)).replace(
        r'report_schema\\raw_report\\tests', r'downloaded_reports\\')

file_path += '10-K-20.xlsx'


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
