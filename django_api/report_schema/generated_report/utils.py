from report_schema.generated_report.models import GeneratedReport
from report_schema.generated_report.active_report import ActiveReport
from report_schema import object_conversions
from report_schema.raw_report import utils as raw_rep_utils
from report_schema import object_conversions

import json


def get_sheets_and_rows(user: str, report_name: str, company_name: str, cik: str, years: str) -> dict:
    year_list = years.split(',')

    args = {
        'company': company_name,
        'cik': cik,
        'years': year_list
    }
    response = raw_rep_utils.retrieve_raw_reports_response(args)
    
    merged_report = ActiveReport(response['reports'])

    GeneratedReport.objects.create(
        name=report_name,
        created_by=user,
        json_schema=json.dumps(merged_report.return_json_report())
    )

    form_data = create_form_data(merged_report)

    return form_data


def create_form_data(report: dict):
    form_data = {}
    sheet_names = report.json_dict.keys()
    for sheet_name in sheet_names:
        form_data[sheet_name] = report.dataframes_dict[sheet_name]
    
    return object_conversions.dataframes_dict_to_json_dict(form_data)


def create_generated_report(user: str, report_name: str, form_data: str, output_type: str) -> int:
    form_data = object_conversions.json_dict_to_dataframes_dict(json.loads(form_data))

    report_to_filter = GeneratedReport.objects.get(name=report_name, created_by=user)
    
    active_report_obj = ActiveReport()
    active_report_obj.load_generated_report(json.loads(report_to_filter.json_schema))
    active_report_obj.filter_report(form_data)

    # Don't think we need this
    # save_single_report(generated_report_json, report_name, user, output_type)

    report_to_filter.json_schema = json.dumps(active_report_obj.return_json_report())
    report_to_filter.save()

    return report_to_filter.pk

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

def validate_create_report_request(request):
        data = request.data
        keys_in_request = 'report_name' in data \
                        and 'form_data' in data \
                        and 'type' in data

        if not keys_in_request:
            return False, 'Correct keys not in request body.'

        correct_types = isinstance(data['report_name'], str) and \
                        isinstance(data['form_data'], str) and \
                        isinstance(data['type'], str)

        if not correct_types:
            return False, 'Key values not the right type in the request body.'

        acceptable_types = {'json', 'xlsx'}
        if data['type'] not in acceptable_types:
            return False, 'File type is invalid.'
        
        matching_report = GeneratedReport.objects.filter(created_by=request.user, name=data['report_name'])
        if not matching_report:
            return False, 'That report does not exist yet.'

        return (True, 'Valid.')

def validate_get_form_data_request(request):
        data = request.data
        keys_in_request = 'report_name' in data \
                        and 'company' in data \
                        and 'cik' in data \
                        and 'years' in data
        
        if not keys_in_request:
            return False, 'Correct keys not in request body.'

        correct_types = isinstance(data['report_name'], str) and \
                        isinstance(data['company'], str) and \
                        isinstance(data['cik'], str) and \
                        isinstance(data['years'], str)
        
        if not correct_types:
            return False, 'Key values not the right type in the request body.'

        acceptable_years = {'2016', '2017', '2018', '2019', '2020', '2021'}
        for year in data['years'].split(','):
            if not (year in acceptable_years):
                return False, 'Year selected is not a valid year.'

        matching_report = GeneratedReport.objects.filter(created_by=request.user, name=data['report_name'])
        if matching_report:
            return False, 'That user has already created a report with that name.'

        return True, 'Valid.'
