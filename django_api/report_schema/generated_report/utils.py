from report_schema.generated_report.models import GeneratedReport
from report_schema.generated_report.active_report import ActiveReport
from report_schema.raw_report import utils as raw_rep_utils
from report_schema import object_conversions

import json
import pandas as pd
import numpy as np


def get_sheets_and_rows(user: str, report_name: str, company_name: str, cik: str, years: str) -> dict:
    """Called by the frontend to get data to populate the filtering form.
    Retrieves the needed raw reports to create a merged report if they don't exist.

    Args:
        user (str): User that used the endpoint
        report_name (str): What the user wants to name the report
        company_name (str): The company to create the report for.
        cik (str): The cik of the company to create the report for.
        years (str): The years to merge together.

    Returns:
        dict: A dictionary that contains the sheet names as keys
        and an array of row names as the values for each sheet name.
    """
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


def create_form_data(report: dict) -> dict:
    """Helper function that goes into the data frame object and retrieves the form data.

    Args:
        report (dict): Dictionary representation of the merged report.

    Returns:
        dict: returns a dictionary of sheet names and row values.
    """
    form_data = {}
    sheet_names = report.json_dict.keys()
    for sheet_name in sheet_names:
        form_data[sheet_name] = report.dataframes_dict[sheet_name].index.to_list()

    return form_data


def create_generated_report(user: str, report_name: str, form_data: str, output_type: str) -> int:
    """[summary]

    Args:
        user (str): [description]
        report_name (str): [description]
        form_data (str): [description]
        output_type (str): [description]

    Returns:
        int: [description]
    """
    form_data = object_conversions.json_dict_to_dataframes_dict(json.loads(form_data))

    report_to_filter = GeneratedReport.objects.get(name=report_name, created_by=user)

    active_report_obj = ActiveReport()
    active_report_obj.load_generated_report(json.loads(report_to_filter.json_schema))
    active_report_obj.filter_report(form_data)

    report_to_filter.json_schema = json.dumps(active_report_obj.return_json_report())
    report_to_filter.save()

    return report_to_filter.pk


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

        acceptable_years = {'2015', '2016', '2017', '2018', '2019', '2020', '2021'}
        for year in data['years'].split(','):
            if not (year in acceptable_years):
                return False, 'Year selected is not a valid year.'

        matching_report = GeneratedReport.objects.filter(created_by=request.user, name=data['report_name'])
        if matching_report:
            return False, 'That user has already created a report with that name.'

        return True, 'Valid.'

def min_max_avg(generated_report: dict) -> dict:
    """
    :return: does min/max/avg analysis on self.generate_report object. Adds the columns to each sheet
    """
    skip_first = 0

    generated_report = object_conversions.json_dict_to_dataframes_dict(
        generated_report)

    for frame in generated_report:
        if skip_first == 1:
            generated_report[frame] = generated_report[
                frame].applymap(
                lambda x: x.strip() if isinstance(x, str) else x).replace(
                to_replace='', value=0.0)
            analysis = generated_report[frame].astype(
                np.float64).select_dtypes(np.number) \
                .stack().groupby(level=0).agg(['min', 'max', 'mean'])
        else:
            skip_first = 1
            analysis = generated_report[frame].select_dtypes(np.number) \
                .stack().groupby(level=0).agg(['min', 'max', 'mean'])

        generated_report[frame] = pd.concat(
            [generated_report[frame], analysis], axis=1)

    return generated_report
