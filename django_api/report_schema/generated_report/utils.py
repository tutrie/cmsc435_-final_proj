from report_schema.generated_report.models import GeneratedReport
from report_schema.generated_report.active_report import ActiveReport
from report_schema import object_conversions
from report_schema.raw_report import utils as raw_rep_utils
from report_schema import object_conversions

import json

# for c in dataframe.columns
#   dataframe[c].index.to_list

def get_sheets_and_rows(user: str, report_name: str, company_name: str, cik: str, years: str) -> dict:
    year_list = years.split(',')

    args = {
        'company': company_name,
        'cik': cik,
        'years': year_list
    }
    response = raw_rep_utils.retrieve_raw_reports_response(args)
    
    merged_report = ActiveReport(response['reports'])

    # Save the merged report to the database
    json_report = merged_report.return_json_report()
    GeneratedReport.objects.create(
        name=report_name,
        created_by=user,
        json_schema=json.dumps(json_report)
    )

    # Create instructions
    form_data = {}

    sheets = merged_report.json_dict.keys()
    for sheet in sheets:
        form_data[sheet] = merged_report.dataframes_dict[sheet]


    # Send the intructions back
    return object_conversions.dataframes_dict_to_json_dict(form_data)


def create_generated_report(user: str, report_name: str, form_data: str, output_type: str) -> int:
    form_data = object_conversions.json_dict_to_dataframes_dict(json.loads(form_data))

    # Get the report json using the report_name
    report_obj = GeneratedReport.objects.get(name=report_name, created_by=user)
    
    active_report_obj = ActiveReport()
    active_report_obj.load_generated_report(json.loads(report_obj.json_schema))

    active_report_obj.filter_report(form_data) # Active report good

    generated_report_json = active_report_obj.return_json_report()  # Active report good

    save_single_report(generated_report_json, report_name, user, output_type)

    report_obj.json_schema = json.dumps(generated_report_json)
    report_obj.save()

    return report_obj.pk

def save_single_report(report_dict: dict, report_name: str, user: str, output_type: str) -> None:
    """
    Call functions to save a single report.

    Args:
        report_dict: A dictionary represntation of a report.
    """
    filename = f'C:\\Users\\bs404\\Downloads\\{report_name}-{user}.{output_type}'

    save_function = {'json': save_json, 'xlsx': save_xlsx}
    save_function[output_type](report_dict, filename)

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
