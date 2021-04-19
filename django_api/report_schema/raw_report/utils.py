from report_generator.utils.object_conversions import (
    dataframes_dict_to_json_dict,
    workbook_to_dataframes_dict
)
from py_edgar_lite.edgar.company import Company as EdgarScraper
from models import RawReport, Company
from openpyxl import load_workbook
import os


def create_company_model(request: dict) -> None:
    company_model = CompanyModel.objects.create(
        name=request['company'], cik=request['cik'],
    )
    company_model.save()


def raw_reports_from_db(request: dict) -> Queryset:
    company_reports_in_db = RawReport.objects.filter(
        company=stripped_request['company'],
        report_date__in=stripped_request['years'],
        report_type=stripped_request['report_type']
    )
    return company_reports_in_db


def create_raw_report_jsons_from_workbooks(request: dict) -> dict:
    json_dict_by_year = {}
    for year in request['years']:
        wb = load_workbook(f'10K_{year}_report_{request['company']}.xlsx')
        df_dict = workbook_to_dataframes_dict(wb)
        json_dict_by_year[year] = dataframes_dict_to_json_dict(df_dict)
        os.remove(f'10K_{year}_report_{request['company']}.xlsx')
    return json_dict_by_year


def create_raw_report_models(company_model, request, jsons, urls):
    for year, json in jsons.items():
        RawReport.objects.create(
            company=company_model,
            # NEED TO CHANGE THIS OR GET FULL DATE FROM SIYAO!
            report_date=models.DateField(),
            report_type=request['report_type'],
            parsed_json=json,
            excel_url=urls[year]
        )


def download_and_create_reports(request: dict) -> None:
    edgar_scraper = EdgarScraper(request['company'], request['cik'])

    edgar_scraper.download_10k_reports(prior_to='2015')

    # Must be called after downloading 10-K's (i.e. the previous statement)
    jsons_by_year = create_raw_report_jsons_from_workbooks(request)

    create_raw_report_models(company_model, request, jsons_by_year,
                             edgar_scraper._excel_urls[request['report_type']]
                             )

    return edgar_scraper._excel_urls[request['report_type']]
