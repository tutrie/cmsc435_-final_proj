from report_schema import object_conversions
from report_schema.raw_report.report_cleaner.cleaner import (
    ten_k_workbook_to_dataframes_dict,
    ten_k_excel_cleaning
)
import openpyxl as pyxl


class ConvertCleanSave:
    """
    This class is responsible for cleaning and converting a spreadsheet when it is pulled into the database for the
    first time. Most of it's functions are in cleaner.py
    """
    def __init__(self, file: str):
        """
        :param file: takes the file path of the xlsx downloaded from edgar
        """
        # the original workbook in case needed in future
        self.excel_report = pyxl.load_workbook(file)
        self.cleaned_excel_report, self.notes = ten_k_excel_cleaning(
            pyxl.load_workbook(file))  # pyxl Workbook object
        self.pandas_dict = ten_k_workbook_to_dataframes_dict(
            self.cleaned_excel_report, self.notes)

    def convert_to_json(self) -> dict:
        """
        :return: calls the object_conversion utility to make a json for storing in the database
        """
        return object_conversions.dataframes_dict_to_json_dict(self.pandas_dict)
