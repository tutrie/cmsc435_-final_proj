from report_generator.utils.convert_objects.object_conversions import *
from .cleaner import *
import openpyxl as pyxl


class ConvertCleanSave:
    def __init__(self, file: str):
        self.excel_report = pyxl.load_workbook(file)  # the original workbook in case needed in future
        self.cleaned_excel_report, self.notes = ten_k_excel_cleaning(pyxl.load_workbook(file))  # pyxl Workbook object
        self.pandas_dict = ten_k_workbook_to_dataframes_dict(self.cleaned_excel_report, self.notes)