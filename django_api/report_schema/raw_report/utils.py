from report_schema.raw_report.EdgarScraper import EdgarScraper
from report_schema.raw_report.models import RawReport, Company
from report_schema.raw_report.object_conversions import (
    dataframes_dict_to_json_dict,
    workbook_to_dataframes_dict
)
from os.path import dirname, realpath
from openpyxl import load_workbook
import datetime
import os


def raw_reports_from_db(request: dict) -> object:
    """
    Args:
        request: A request from the front-end with user inputted company, CIK,
        years of reports wanted, and the report type.

    Returns:
        Django Queryset of all reports in database that match user input
        values.
    """
    company_reports_in_db = RawReport.objects.filter(
        company__cik=request['cik'],
        report_date__in=request['years']
    )
    return company_reports_in_db


def create_raw_report_jsons_from_workbooks(request: dict) -> dict:
    """
     Args:
        request: A request from the front-end with user inputted company, CIK,
        years of reports wanted, and the report type.

    Returns:
        A dictionary where keys are years and values are dictionary
        representations of Excel workbooks corresponding to that year.
    """
    json_dict_by_year = {}
    for year in request['years']:
        dir_name = dirname(realpath(__file__)) + '/downloaded_reports/'
        filename = f'10K_{year}_report_{request["company"]}.xlsx'
        wb = load_workbook(f'{dir_name}{filename}')

        df_dict = workbook_to_dataframes_dict(wb)
        json_dict_by_year[year] = dataframes_dict_to_json_dict(df_dict)

        os.remove(f'10K_{year}_report_{request["company"]}.xlsx')
    return json_dict_by_year


def create_raw_report_models(request, company_model, jsons, urls) -> None:
    """
    A function to create RawReport models and save them to the database.

    Args:
        request: A request from the front-end with user inputted company, CIK,
            years of reports wanted, and the report type.

        company_model: A Company model object from company_schema/models.py
            correspoding to the user inputted company name and CIK.

        jsons: A dictionary where keys are years and values are dictionary
            representations of Excel workbooks corresponding to that year; what
            is outputted by create_raw_report_jsons_from_workbooks.

        urls: A dictionary where keys are years and values are urls
            corresponding to the urls where the actual Excel files of the json
            representation with the same year inside jsons can be downloaded
            from.

    Returns:
        None
    """
    for year, json in jsons.items():
        RawReport.objects.create(
            company=company_model,
            # Edgar Scaper only able to get year of report, not full date.
            report_date=datetime.date(int(year), 1, 1),
            parsed_json=json,
            excel_url=urls[year]
        )


def download_and_create_reports(request: dict, company_model: Company) -> dict:
    """
    Args:
        request: A request from the front-end with user inputted company, CIK,
            years of reports wanted, and the report type.

        company_model: A Company model object from company_schema/models.py
            correspoding to the user inputted company name and CIK.

    Returns:
        A dictionary where keys are years and values are urls
        corresponding to the urls where the actual Excel files of the raw
        reports can be donwloaded from.
    """
    edgar_scraper = EdgarScraper(request['company'], request['cik'])

    edgar_scraper.download_10k_reports(prior_to='2015')

    # Must be called after downloading 10-K's (i.e. the previous statement)
    jsons_by_year = create_raw_report_jsons_from_workbooks(request)

    create_raw_report_models(request, company_model, jsons_by_year,
                             edgar_scraper._excel_urls[request['10-K']]
                             )

    return edgar_scraper._excel_urls[request['10-K']]


def retrieve_raw_reports_response(request: dict) -> dict:
    """
    Args:
        request: A request from the front-end with user inputted company, CIK,
            years of reports wanted, and the report type.

    Returns:
        A response dictionary containing the urls for the raw reports.
    """
    response = {
        'company_name': request['name'],
        'company_cik': request['cik'],
        'reports': {}
    }

    raw_reports_in_db = raw_reports_from_db(request)

    if not raw_reports_in_db:
        company_model = Company.objects.create(
            name=request['company'], cik=request['cik']
        )

        response['reports'] = download_and_create_reports(
            request, company_model
        )
    else:
        for report_model in raw_reports_from_db:
            year_str = str(report_model.report_date.year)
            response['reports'][year_str] = report_model.excel_url

    return response
