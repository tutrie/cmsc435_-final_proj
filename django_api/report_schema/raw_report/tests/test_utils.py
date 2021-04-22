from report_schema.raw_report.EdgarScraper import EdgarScraper
from report_schema.raw_report.models import RawReport, Company
from report_schema.raw_report import utils
from unittest import TestCase
from datetime import datetime


class TestUtils(TestCase):

    def test_create_raw_report_models(self):
        company_model = Company.objects.create(name='Google', cik='123456')
        jsons = {
            '2015': {
                'item1': 'line1',
            },
            '2016': {
                'item1': 'line1',
                'item2': 'line2'
            }
        }
        urls = {
            '2015': 'Google.com/2015',
            '2016': 'Google.com/2016'
        }

        utils.create_raw_report_models(company_model, jsons, urls)

        raw_reports = RawReport.objects.all().order_by('report_date__year')

        report1 = raw_reports.first()
        self.assertTrue(company_model == report1.company)
        self.assertTrue(2015 == report1.report_date.year)
        self.assertTrue(jsons['2015'] == report1.parsed_json)
        self.assertTrue('Google.com/2015' == report1.excel_url)

        report2 = raw_reports.last()
        self.assertTrue(company_model == report2.company)
        self.assertTrue(2016 == report2.report_date.year)
        self.assertTrue(jsons['2016'] == report2.parsed_json)
        self.assertTrue('Google.com/2016' == report2.excel_url)

    def test_create_raw_report_jsons_from_workbooks(self):
        edgar_scraper = EdgarScraper('Basset', '0000010329')
        file_paths = edgar_scraper.download_10k_reports()

        intended_years = ['2015', '2016', '2017', '2018', '2019', '2020']

        json_dict = utils.create_raw_report_jsons_from_workbooks(file_paths)

        for year, report_dict in json_dict.items():
            self.assertTrue(year in intended_years)
            self.assertIsInstance(report_dict, dict)

    def test_raw_reports_from_db(self):
        company_model = Company.objects.create(name='Google', cik='123456')

        raw_report_model1 = RawReport.objects.create(
            company=company_model,
            report_date=datetime.date(2015, 1, 1),
            excel_url='Google.com'
        )

        raw_report_model2 = RawReport.objects.create(
            company=company_model,
            report_date=datetime.date(2016, 1, 1),
            excel_url='Google.com'
        )

        reports_in_db = utils.raw_reports_from_db({
            'company': company_model.name,
            'cik': company_model.cik,
            'years': ["2015"]
        }).order_by('report_date__year')

        report1 = reports_in_db.first()
        self.assertTrue(raw_report_model1.company == report1.company)
        self.assertTrue(raw_report_model1.report_date == report1.report_date)
        self.assertTrue(raw_report_model1.excel_url == report1.excel_url)

        report2 = reports_in_db.last()
        self.assertTrue(raw_report_model2.company == report2.company)
        self.assertTrue(raw_report_model2.report_date == report2.report_date)
        self.assertTrue(raw_report_model2.excel_url == report2.excel_url)

    def test_retrieve_raw_reports_response_company_does_not_exist(self):
        intended_response = {
            'company': 'Basset',
            'cik': '0000010329',
            'reports': {
                '2015': 'json_2015',
                '2016': 'json_2016',
                '2017': 'json_2017',
                '2018': 'json_2018',
                '2019': 'json_2019',
                '2020': 'json_2020',
            }
        }

        inputted_request = {
            'company': 'Basset',
            'cik': '0000010329',
            'years': ['2015', '2016', '2017', '2018', '2019', '2020']
        }

        returned_response = utils.retrieve_raw_reports_response(
            inputted_request)

        for year, json_dict in returned_response['reports'].items():
            self.assertTrue(year in intended_response['reports'].keys())
            self.assertIsInstance(json_dict, dict)

    def test_retrieve_raw_reports_response_company_already_exist(self):
        company_model = Company.objects.create(name='Google', cik='123456')

        for year in range(2015, 2021):
            RawReport.objects.create(
                company=company_model,
                report_date=datetime.date(year, 1, 1),
                excel_url='Google.com'
            )

        intended_response = {
            'company': 'Google',
            'cik': '123456',
            'reports': {
                '2015': 'json_2015',
                '2016': 'json_2016',
                '2017': 'json_2017',
                '2018': 'json_2018',
                '2019': 'json_2019',
                '2020': 'json_2020',
            }
        }

        inputted_request = {
            'company': 'Google',
            'cik': '123456',
            'years': ['2015', '2016', '2017', '2018', '2019', '2020']
        }

        returned_response = utils.retrieve_raw_reports_response(
            inputted_request)

        for year, json_dict in returned_response['reports'].items():
            self.assertTrue(year in intended_response['reports'].keys())
            self.assertIsInstance(json_dict, dict)
