from report_schema.raw_report.report_cleaner.cleaner import (
    ten_k_excel_cleaning,
    ten_k_workbook_to_dataframes_dict
)
from report_schema.raw_report.object_conversions import (
    dataframes_dict_to_json_dict
)
import openpyxl as pyxl


class ConvertCleanSave:
    def __init__(self, file: str):
        # the original workbook in case needed in future
        self.excel_report = pyxl.load_workbook(file)
        self.cleaned_excel_report, self.notes = ten_k_excel_cleaning(
            pyxl.load_workbook(file))  # pyxl Workbook object
        self.pandas_dict = ten_k_workbook_to_dataframes_dict(
            self.cleaned_excel_report, self.notes)

    def convert_to_json(self):
        return dataframes_dict_to_json_dict(self.pandas_dict)
