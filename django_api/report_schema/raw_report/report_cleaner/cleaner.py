import pandas as pd
import openpyxl as pyxl
import numpy as np


def ten_k_workbook_to_dataframes_dict(excel_report: pyxl.Workbook,
                                      notes: dict) -> dict:
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
        df = pd.DataFrame(data, columns=cols)
        for loc in range(len(df['index'])):
            df.loc[loc, 'index'] = str(df['index'][loc].replace(' (loss)', ''))
            df.loc[loc, 'index'] = str(df['index'][loc].replace(' (gain)', ''))
            df.loc[loc, 'index'] = str(
                df['index'][loc].replace(' (benefit)', ''))
            df.loc[loc, 'index'] = str(
                df['index'][loc].replace(' (losses)', ''))
            df.loc[loc, 'index'] = str(
                df['index'][loc].replace(' (gains)', ''))
            df.loc[loc, 'index'] = str(
                df['index'][loc].replace(' (expense)', ''))
        df = df.set_index('index').fillna(value=np.nan)
        dup_count = 1
        while True in df.index.duplicated():
            df.index = df.index.where(
                ~df.index.duplicated(), df.index + ' dp_' + str(dup_count))
            dup_count += 1


#        dataframes_dict[sheet.title] = pd.DataFrame(data, columns=cols).set_index(keys='index').fillna(value=np.nan)
        dataframes_dict[sheet.title] = df

    # return dataframes_dict
    return normalize_data(dataframes_dict, notes)


def normalize_data(dataframes_dict: dict, notes: dict) -> dict:
    for index, (sheet_name, frame) in enumerate(dataframes_dict.items()):
        if get_multiplier(notes[sheet_name]) > 1:
            multiplier = get_multiplier(notes[sheet_name])
            df = frame.T
            if index == 0:
                df['Entity Public Float'] = df['Entity Public Float'] * multiplier
                dataframes_dict[sheet_name] = df.T
            else:
                for row_name in df.columns:
                    row_to_skip = (
                        '(in shares)' in row_name or '(in dollars per share)' in row_name)
                    if not row_to_skip:
                        df[row_name] = df[row_name] * multiplier
                dataframes_dict[sheet_name] = df.T
    return dataframes_dict


def get_multiplier(note: str) -> int:
    if 'Thousands' in note:
        return 1000
    if 'Millions' in note:
        return 1000000
    if 'Billions' in note:
        return 1000000000
    return 1


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
                    # haven't seen a spreadsheet yet where this isnt the
                    # case for merged cells at the top.
                    next_coord = col_cell.coordinate[0] + '2'
                    sheets[next_coord].value = sheets[next_coord].value + \
                        ' - ' + sheets[my_range][0][0].value
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

        # Units in US Dollars (most likely)
        notes[sheets.title] = sheets['A1'].value

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

    return excel_report, notes
