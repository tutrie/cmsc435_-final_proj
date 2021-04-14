from .excelcleaner import CleanedExcelReport
from report_generator.utils.convert_objects.object_conversions import *


class ConvertCleanSave:
    def __init__(self, file: str):
        self.excel_report = CleanedExcelReport(file)
        self.pandas_dict = workbook_to_dataframes_dict(self.excel_report.cleaned_excel_report)
