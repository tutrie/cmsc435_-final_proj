from report_schema.generated_report.models import GeneratedReport
from report_schema.generated_report.active_report import ActiveReport
from report_schema import object_conversions
from report_schema.raw_report import utils as raw_rep_utils

from datetime import datetime
import json

# for c in dataframe.columns
#   dataframe[c].index.to_list

def get_sheets_and_rows(report_name: str, company_name: str, cik: str, years: str) -> bool:
    # Get raw reports for the company based on cik and years (call raw report endpoint)
    year_list = years.split(',')

    args = {
        'company': company_name,
        'cik': cik,
        'years': year_list
    }
    response = raw_rep_utils.retrieve_raw_reports_response(args)

    print(response.json())

    return True


def create_generated_report(self, user: str, report_name: str, sheets: list, rows: list, output_type: str) -> int:
   # Arguments are gauranteed to be validated already
   
    # Get the raw report jsons (we know theyre in the database)
    report_json = {}
    
    # Generate the report
    merged_report = ActiveReport(report_json) # Active report good
    saved_report = merged_report.return_json_report()
    new_merged_report = ActiveReport(saved_report)


    instructions = generate_instructions(merged_report, sheets, rows)
    
    
    merged_report.filter_report(instructions) # Active report good
    generated_report_json = merged_report.return_json_report()  # Active report good
    save_single_report(generated_report_json, output_type)



    # Create generated report in the database
    GeneratedReport.objects.create(
        name=report_name,
        json_schema=generated_report_json
    )

def generate_instructions(merged_report: ActiveReport, sheets, rows) -> dict:
    """
    Generate instructions to filter report.

    Returns:
        Instructions dictionary with key being a sheet name and the values
        being rows for that sheet to keep.
    """
    instructions = {}

    sheets_to_keep = choose_sheet_names(merged_report)

    for sheet in sheets_to_keep:
        instructions[sheet] = choose_rows_in_sheet(sheet, merged_report.dataframes_dict[sheet])

    return instructions

def save_single_report(report_dict: dict, output_type) -> None:
    """
    Call functions to save a single report.

    Args:
        report_dict: A dictionary represntation of a report.
    """

    current_date_and_time = str(datetime.now())

    filename = 'generated-report' + current_date_and_time + f'.{output}'

    save_function = {'json': save_json, 'xlsx': save_xlsx}
    save_function[output](report_dict, filename)

def save_json(report_dict: dict, output_file: str) -> None:
    """
    Saves a dictionary as a JSON file to the given output file path.

    Args:
        report_dict: A dictionary represntation of a report.

        output_file: A full file path to where the report should be saved to.
    """
    object_conversions.json_dict_to_json_file(report_dict, output_file)



def save_xlsx(report_dict: dict, output_file: str):
    """
    Saves a dictionary as an Excel file to the given output file path.

    Args:
        report_dict: A dictionary represntation of a report.

        output_file: A full file path to where the report should be saved to.
    """
    dataframes_dict = object_conversions.json_dict_to_dataframes_dict(report_dict)
    object_conversions.dataframes_dict_to_workbook(dataframes_dict, output_file)
