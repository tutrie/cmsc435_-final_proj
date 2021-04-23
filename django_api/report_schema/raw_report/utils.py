
from report_schema.raw_report.report_cleaner.excelToPandasToJson import (
    ConvertCleanSave
)
from report_schema.raw_report.EdgarScraper import EdgarScraper
from report_schema.raw_report.models import RawReport, Company
import datetime
import os


def create_raw_report_models(company_model, jsons, urls) -> None:
    """
    A function to create RawReport models and save them to the database.

    Args:
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


def create_raw_report_jsons_from_workbooks(report_file_paths: dict) -> dict:
    """
    Assuming the raw report Excel workbooks are already downloaded, given a
    list of years, convert the excel workbooks into their dictionary
    representation.

    Args:
        report_file_paths: A dictionary where key is a year string and the
            value is a file path to a raw report corresponding to that year.

    Returns:
        A dictionary where keys are years and values are dictionary
        representations of Excel workbooks corresponding to that year.
    """
    json_dict_by_year = {}
    for year, file_path in report_file_paths.items():
        conversion_obj = ConvertCleanSave(file_path)

        json_dict_by_year[year] = conversion_obj.convert_to_json()

        os.remove(file_path)

    return json_dict_by_year


def raw_reports_from_db(request: dict) -> object:
    """
    Gets RawReport models with specfic CIK and year attributes from the
    database.

    Args:
        request: A request from the front-end with user inputted company, CIK,
        years of reports wanted, and the report type.

    Returns:
        Django Queryset of all reports in database that match user input
        values.
    """
    company_reports_in_db = RawReport.objects.filter(
        company__cik=request['cik'],
        report_date__year__in=request['years']
    )
    return company_reports_in_db


def retrieve_raw_reports_response(request: dict) -> dict:
    """
    Create a response object containing the company name and CIK in the
    request, as well as the urls of the Excel files for the requested years.
    Args:
        request: A request from the front-end with user inputted company, CIK,
            and years of reports wanted.

    Returns:
        A response dictionary containing the urls for the raw reports.
    """
    response = {
        'company_name': request['company'],
        'company_cik': request['cik'],
        'reports': {}
    }

    raw_reports_in_db = raw_reports_from_db(request)

    if not raw_reports_in_db:
        company_model = Company.objects.create(
            name=request['company'], cik=request['cik']
        )

        edgar_scraper = EdgarScraper(request['company'], request['cik'])

        report_file_paths = edgar_scraper.download_10k_reports()

        report_file_paths_filtered = {}

        for year, file_path in report_file_paths.items():
            if year in request['years']:
                report_file_paths_filtered[year] = file_path

        # Must be called after downloading 10-K's (i.e. the previous statement)
        jsons_by_year = create_raw_report_jsons_from_workbooks(
            report_file_paths_filtered
        )

        create_raw_report_models(company_model, jsons_by_year,
                                 edgar_scraper._excel_urls['10-K'])

        # Raw reports are now in database.
        raw_reports_in_db = raw_reports_from_db(request)

    for report_model in raw_reports_in_db:
        year_str = str(report_model.report_date.year)
        if year_str in request['years']:
            response['reports'][year_str] = report_model.parsed_json

    return response
