from py_edgar_lite.edgar.company import Company
from datetime import datetime
import requests
import json

base_url = "http://127.0.0.1:8000/api/"
companies_url = base_url + "companies"
raw_report_url = base_url + "raw-reports"


def is_company_in_db(company_cik: str) -> bool:
    """
    Args:
        company: A string of a company CIK.

    Returns:
        True if the company exists in the database; False otherwise.
    """
    r = requests.get(companies_url)

    for company in r.json():
        if company['cik'] == company_cik:
            return True

    return False


def get_raw_reports_in_db(request: dict) -> dict:
    """
    Args:
        request: A request sent from the front-end containing a company name,
            cik, and years for reports wanted.

    Returns:
        A dictionary response containing the urls for the reports wanted based
        on their year.
    """
    output = {
        'company': request['company'],
        'report_type': request['report_type'],
        'report_date': {},
        'notes': []
    }

    year_list_copy = request['years'].copy()

    r = requests.get(raw_report_url)
    for report in r.json():
        # Assuming the report-date in the database to be in the format of YYYY.
        check1 = report['report_date'] in year_list_copy
        check2 = report['company']['cik'] == request['cik']
        check3 = report['report_type'] == request['report_type']

        if check1 and check2 and check3:
            output['report_date'][report['report_date']] = report["excel_url"]
            year_list_copy.pop(year_list_copy.index(report['report_date']))

    # Generating raw report urls from Edgar.
    company = Company(request['name'], request['cik'], timeout=20)

    # Check to see if there is a year that the User sent that is not included
    # in the database. May be unnecessary at this point in the project.
    for year in year_list_copy:
        excel_url = company.get_10k_year(year)
        if excel_url:
            payload = {
                'company': {
                    'name': request['name'],
                    'cik': request['cik']
                },
                'report_date': str(year),
                'excel_url': excel_url
            }
            request.post(raw_report_url, payload=payload)
            output['report_date'][str(year)] = excel_url
        else:
            output['notes'].append(f'Report could not be generated for
                                   year {year}!')

    return output


def get_raw_reports_from_edgar(request: dict) -> dict:
    """
    Args:
        request: A request sent from the front-end containing a company name,
            cik, and years for reports wanted.

    Returns:
        A dictionary response containing the urls for the reports wanted based
        on their year.
    """
    output = {
        'company_name': request['name'],
        'company_cik': request['cik'],
        'report_type': request['report_type'],
        'report_date': {},
        'notes': []
    }

    earliest_report_year = 2015
    latest_report_year = datetime.now().date.year

    # Generating raw report urls from Edgar.
    company = Company(request['name'], request['cik'], timeout=20)
    report_urls = company.get_company_excel_reports_from(
        request['report_type'], prior_to=str(earliest_report_year),
    )

    if not report_urls:
        output['notes'].append(f"Couldn't get excel reports from company!")
        return output

    # Add report urls to output if requested by user and to database.
    for year in range(earliest_report_year, latest_report_year):
        year_str = str(year)
        if year_str in request['years']:
            output['report_date'][year_str] = report_urls[year_str]

        payload = {
            "name": request['name'],
            "cik": request['cik'],
            "report_date": year_str,
            "report_type": request['report_type'],
            "excel_url": report_urls[year_str]
        }
        response = request.post(raw_report_url, payload=payload)
        if response.status_code != 201:
            output['notes'].append(f'POST request error for year {year}!')

    return output


def retrieve_raw_reports(request: dict) -> dict:
    """
    Args:
        request: A request sent from the front-end containing a company name,
            cik, and years for reports wanted. Assuming the request should look
            like:
            {
                'name': COMPANY_NAME,
                'cik': COMPANY_CIK
                'years': A list of year Strings in the format of YYYY.
                'report_type': '10-K' or '10-Q'
            }

    Returns:
        A dictionary response containing the urls for the reports wanted,
        assuming to be returned to the front-end. End result looks like:
        {
            'company_name': request['name'],
            'company_cik': request['cik'],
            'report_type': request['report_type'],
            'report_date': {
                '<report_year>': '<report_url>',
                ...
            },
            'notes': [
                'Additional notes go here!'
            ]
        }
    """
    if company_in_db(request['company']['cik']):
        response = get_raw_reports_in_db(request)
    else:
        response = get_raw_reports_from_edgar(request)

    return response
