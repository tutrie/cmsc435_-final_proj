import excelcleaner
from report_generator.utils.object_conversions import workbook_to_dataframes_dict


class ConvertCleanSave:
    def __init__(self, file: str):
        self.excel_report = excelcleaner(file)
        self.pandas_dict = workbook_to_dataframes_dict(self.excel_report.cleaned_excel_report)
