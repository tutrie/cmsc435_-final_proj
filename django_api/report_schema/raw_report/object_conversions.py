import pandas as pd
import json
import openpyxl as pyxl


def workbook_to_dataframes_dict(excel_report: pyxl.Workbook) -> dict:
    """
    Args:
        excel_report: openpyxl Workbook object

    Returns:
        Dictionary of dataframes for each sheet in excel workbook.
    """
    dataframes_dict = {}
    for sheet in excel_report.worksheets:
        data = sheet.values
        cols = next(data)  # Headers (First Row)
        data = list(data)  # Second until Last rows
        dataframes_dict[sheet.title] = (pd.DataFrame(data, columns=cols))
    return dataframes_dict


def dataframes_dict_to_json_dict(dataframes_dict: dict) -> dict:
    """
    Args:
        dataframes_dict: Dictionary of Pandas dataframes where key is the sheet
            name of the dataframe while the value is the inner dictionary
            corresponding to the dataframe itself.

    Returns:
        Dictionary of dictionaries where key is the sheet name of the dataframe
        while the value is the dictionary representation of the dataframe.
    """
    json_dict = {}
    for sheet_name, df in dataframes_dict.items():
        json_dict[sheet_name] = dataframe_to_dict(df)

    return json_dict


def dataframe_to_dict(dataframe: object) -> dict:
    """
    Args:
        dataframe: A pandas dataframe

    Returns:
        Dictionary representation of pandas dataframe
    """
    return json.loads(dataframe.to_json(force_ascii=False))
