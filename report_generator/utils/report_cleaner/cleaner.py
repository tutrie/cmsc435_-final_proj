import pandas as pd
import openpyxl as pyxl
import numpy as np


def ten_k_workbook_to_dataframes_dict(excel_report: pyxl.Workbook, notes: dict) -> dict:
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
        df = pd.DataFrame(data, columns=cols).set_index('index', inplace=True)
        dataframes_dict[sheet.title] = pd.DataFrame(data, columns=cols).set_index(keys='index').fillna(value=np.nan)

    return dataframes_dict

def normalize_data(dataframes_dict: dict, notes: dict) -> dict:
    pass



def ten_k_excel_cleaning(excel_report: pyxl.Workbook) -> pyxl.Workbook:
    sheets_name_series = pd.Series(excel_report.sheetnames)
    notes = {}
    pattern = '^Condensed|^Consolidated|^CONSOLIDATED|^CONDENSED|^condensed|^consolidated'
    to_keep = sheets_name_series.str.contains(pattern)
    to_drop = (sheets_name_series[~to_keep])[1:]
    for sheet_name in to_drop:
        excel_report.remove(excel_report[sheet_name])

    for sheets in excel_report.worksheets:
        while sheets.merged_cells.ranges:
            my_range = str(sheets.merged_cells.ranges[0])
            sheets.unmerge_cells(my_range)
            # Fixing merged cells tha say '# Months Ended'
            if len(sheets[my_range]) == 1:  # Len = 1 if Merged Horizontally
                for col_cell in sheets[my_range][0]:
                    # haven't seen a spreadsheet yet where this isnt the case for merged cells at the top.
                    next_coord = col_cell.coordinate[0] + '2'
                    sheets[next_coord].value = sheets[next_coord].value + ' - ' + sheets[my_range][0][0].value
                sheets[my_range][0][0].value = None

    # Fixing Sheet names to value in cell A1 and making cell A1 to be units
    for sheets in excel_report.worksheets:
        to_cut = sheets['A1'].value.index('-')
        sheets.title = sheets['A1'].value[:to_cut - 1]
        sheets['A1'].value = sheets['A1'].value[to_cut + 2:]

    for sheets in excel_report.worksheets:
        # Making blank cells have no bold format and
        # adding string to visualize already-bolded
        # categories distinctive in JSON format later on.
        index_col = list(next(sheets.columns))
        for cell in index_col:
            if cell.value is None and cell.font.b:
                cell.font.b = False
            elif cell.value is not None and cell.font.b:
                cell.value += ' - CATEGORY'

        notes[sheets.title] = sheets['A1'].value  # Units in US Dollars (most likely)

        # If only merged cells existed in first row
        # and were dealt with in previous for-loop
        if sheets['B1'].value is None:
            sheets.delete_rows(1)

        # Otherwise, check to see if there still exists
        # cells that has '# Months Ended' that should
        # be merged with the cell below it. Afterwards,
        # remove first row as it is unnecessary.
        else:
            first_row = next(sheets.rows)
            extra_header = False
            for cell in first_row:
                if cell.value and 'Months Ended' in cell.value:
                    cell_below = f'{cell.column_letter}{cell.row + 1}'
                    sheets[cell_below].value += f' - {cell.value}'
                    extra_header = True
            if extra_header:
                sheets.delete_rows(1)

        # this is needed for the json to work properly
        sheets['A1'].value = 'index'

        # Can't modify styles. Must create copy and set cell font equal to copy.
        #copy_style = copy(sheets['A1'].font)
        #copy_style.b = True  # Bold
        #copy_style.i = True  # Italicize
        #sheets['A1'].font = copy_style

    return excel_report, notes
