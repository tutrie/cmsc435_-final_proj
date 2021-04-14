import unittest
from report_generator.utils.report_cleaner import cleaner

file_path = "ReportGenerator/excel_reports/10-K-20.xlsx"


class MyTestCase(unittest.TestCase):
    def test_CleanedExcelReport_notes(self):
        test_object = cleaner.CleanedExcelReport(file_path)
        self.assertEqual(8, len(test_object.notes.keys()))

    def test_CleanedExcelReport_original(self):
        # 97 sheets in OG 10-k-20 report
        test_object = cleaner.CleanedExcelReport(file_path)
        self.assertEqual(97, len(test_object.excel_report.sheetnames))

    def test_CleanedExcelReport_cleaned(self):
        # 97 sheets in OG 10-k-20 report
        test_object = cleaner.CleanedExcelReport(file_path)
        self.assertEqual(8, len(test_object.cleaned_excel_report.sheetnames))
