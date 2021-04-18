from datetime import datetime
import requests
import json

base_url = "http://127.0.0.1:8000/api/"
companies_url = base_url + "companies"
raw_report_url = base_url + "raw-reports"


def is_company_in_db(company_name: str) -> bool:
    """
    Args:
        company: A string of a company name.

    Returns:
        True if the company exists in the database; False otherwise.
    """
    r = requests.get(companies_url)

    for company in r.json():
        if company['name'] == company_name:
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
        'report_date': {}
    }

    year_list_copy = request['years'].copy()

    r = requests.get(raw_report_url)
    for report in r.json():
        # Assuming the report-date to be in the formation of YYYY-MM-DD.
        date_obj = datetime.strptime(report['report_date'], '%Y-%m-%d')

        check1 = date_obj.date.year in year_list_copy
        check2 = report['company']['name'] == request['company']['name']
        check3 = report['report_type'] == request['report_type']

        if check1 and check2 and check3:
            output['report_date'][report['report_date']] = report["excel_url"]
            year_list_copy.pop(year_list_copy.index(date_obj.date.year))

    # Check to see if there is a year that the User sent that is not included
    # in the database. May be unnecessary at this point in the project.
    for year in year_list_copy:
        # Call Siyao's code to generate link from company name, CIK, and year.
        # Hopefully, somehow, this returns the report date as well.
        report_date, excel_url = siyao_dummy_function()
        payload = {
            'company': {
                'name': request['name'],
                'cik': request['cik']
            },
            'report_date': report_date,
            'excel_url': excel_url
        }
        request.post(raw_report_url, payload=payload)
        output['report_date'][report_date] = excel_url

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
        'company': request['company'],
        'report_type': request['report_type'],
        'report_date': {}
    }
    earliest_report_year = 2015
    latest_report_year = datetime.now().date.year
    for year in range(earliest_report_year, latest_report_year):
        # Call Siyao's code to generate report_date / report excel url
        report_date, excel_url = siyao_dummy_function()
        payload = {
            "company": {
                "name": request['company'],
                "cik": request['cik']
            },
            "report_date": report_date,
            "report_type": request['report_type'],
            "excel_url": excel_url
        }
        request.post(raw_report_url, payload=payload)

        # Assuming the report-date to be in the formation of YYYY-MM-DD.
        date_obj = datetime.strptime(report['report_date'], '%Y-%m-%d')
        should_include = date_obj.date.year in request['years']
        if should_include:
            output['report_date'][report_date] = excel_url

    return output


def retrieve_raw_reports(request: dict) -> dict:
    """
    Args:
        request: A request sent from the front-end containing a company name,
            cik, and years for reports wanted. Assuming the request should look
            like:
            {
                'company': {
                    'name': COMPANY_NAME,
                    'cik': COMPANY_CIK
                },
                'years': A list of years in the format of YYYY.
            }

    Returns:
        A dictionary response containing the urls for the reports wanted,
        assuming to be returned to the front-end via a JSONResponse or
        HTTPResponse object.
    """
    if company_in_db(request['company']['name']):
        response = get_raw_reports_in_db(request)
    else:
        response = get_raw_reports_from_edgar(request)

    return response
