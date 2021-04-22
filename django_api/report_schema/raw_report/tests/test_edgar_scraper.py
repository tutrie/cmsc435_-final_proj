from report_schema.raw_report.EdgarScraper import EdgarScraper
from lxml import html
import unittest
import requests
import os


ORACLE_10K_EXCEL = {
    '2010': ['https://www.sec.gov/Archives/edgar/data/1341439/000119312510151896/Financial_Report.xlsx'],
    '2011': ['https://www.sec.gov/Archives/edgar/data/1341439/000119312511174819/Financial_Report.xlsx'],
    '2012': ['https://www.sec.gov/Archives/edgar/data/1341439/000119312512284007/Financial_Report.xlsx'],
    '2013': ['https://www.sec.gov/Archives/edgar/data/1341439/000119312513272832/Financial_Report.xlsx'],
    '2014': ['https://www.sec.gov/Archives/edgar/data/1341439/000119312514251351/Financial_Report.xlsx'],
    '2015': ['https://www.sec.gov/Archives/edgar/data/1341439/000119312515235239/Financial_Report.xlsx'],
    '2016': ['https://www.sec.gov/Archives/edgar/data/1341439/000119312516628942/Financial_Report.xlsx'],
    '2017': ['https://www.sec.gov/Archives/edgar/data/1341439/000119312517214833/Financial_Report.xlsx'],
    '2018': ['https://www.sec.gov/Archives/edgar/data/1341439/000119312518201034/Financial_Report.xlsx'],
    '2019': ['https://www.sec.gov/Archives/edgar/data/1341439/000156459019023119/Financial_Report.xlsx'],
    '2020': ['https://www.sec.gov/Archives/edgar/data/1341439/000156459020030125/Financial_Report.xlsx']}

GET_FORMS_ONLY_10K = {'10-K': {
    '2010': ['https://www.sec.gov/Archives/edgar/data/1341439/000119312510151896/Financial_Report.xlsx'],
    '2011': ['https://www.sec.gov/Archives/edgar/data/1341439/000119312511174819/Financial_Report.xlsx'],
    '2012': ['https://www.sec.gov/Archives/edgar/data/1341439/000119312512284007/Financial_Report.xlsx'],
    '2013': ['https://www.sec.gov/Archives/edgar/data/1341439/000119312513272832/Financial_Report.xlsx'],
    '2014': ['https://www.sec.gov/Archives/edgar/data/1341439/000119312514251351/Financial_Report.xlsx'],
    '2015': ['https://www.sec.gov/Archives/edgar/data/1341439/000119312515235239/Financial_Report.xlsx'],
    '2016': ['https://www.sec.gov/Archives/edgar/data/1341439/000119312516628942/Financial_Report.xlsx'],
    '2017': ['https://www.sec.gov/Archives/edgar/data/1341439/000119312517214833/Financial_Report.xlsx'],
    '2018': ['https://www.sec.gov/Archives/edgar/data/1341439/000119312518201034/Financial_Report.xlsx'],
    '2019': ['https://www.sec.gov/Archives/edgar/data/1341439/000156459019023119/Financial_Report.xlsx'],
    '2020': ['https://www.sec.gov/Archives/edgar/data/1341439/000156459020030125/Financial_Report.xlsx']}}


class EdgarScraperTestCase(unittest.TestCase):

    def test_get_filings_url(self):
        company = None
        company = EdgarScraper("Oracle Corp", "0001341439")
        result = company.get_filings_url(filing_type="10-K")
        expected = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001341439&type=10-K&dateb=&owner" \
                   "=include&count=100"
        self.assertEqual(result, expected)

    def test_get_all_filings(self):
        company = None
        company = EdgarScraper("Oracle Corp", "0001341439")
        result = company.get_all_filings(filing_type="10-K")

        url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001341439&type=10-K&dateb=&owner" \
              "=include&count=100"
        page = requests.get(url, timeout=10)

        while not page.ok:
            page = requests.get(url, timeout=10)

        expected = html.fromstring(page.content)
        self.assertEqual(html.tostring(result), html.tostring(expected))

    def test_get_company_excel_reports_from_10K(self):
        self.maxDiff = None
        company = None
        company = EdgarScraper("Oracle Corp", "0001341439")
        result = company.get_company_excel_reports_from("10-K")
        self.assertEqual(result, ORACLE_10K_EXCEL)

    def test_download_url(self):
        company = None
        company = EdgarScraper("Oracle Corp", "0001341439")
        # download file
        url = "https://www.sec.gov/Archives/edgar/data/1341439/000119312514251351/Financial_Report.xlsx"
        file_path = company.download_file(url)
        self.assertTrue(file_path is not None)
        os.remove(file_path)

    def test_download_all_10k_reports(self):
        company = None
        company = EdgarScraper("Oracle Corp", "0001341439")
        # download file
        file_paths = company.download_10k_reports()
        self.assertTrue(file_paths is not None)

        for file_path in file_paths.values():
            os.remove(file_path)

    def test_correct_return_10k(self):
        self.maxDiff = None
        company = None
        company = EdgarScraper("Oracle Corp", "0001341439")
        company.get_company_excel_reports_from("10-K")
        result = company.get_existing_forms()
        self.assertEqual(result, GET_FORMS_ONLY_10K)
        result = company.get_10k_year('2020')
        self.assertEqual(result, GET_FORMS_ONLY_10K['10-K']['2020'][0])
        result = company.get_10k_year('2019')
        self.assertEqual(result, GET_FORMS_ONLY_10K['10-K']['2019'][0])
        result = company.get_10k_year('2018')
        self.assertEqual(result, GET_FORMS_ONLY_10K['10-K']['2018'][0])

    def test_incorrect_return_10k(self):
        company = None
        company = EdgarScraper("Oracle Corp", "0001341439")
        result = company.get_10k_year('1988')
        self.assertEqual(result, None)
        result = company.get_10k_year('2025')
        self.assertEqual(result, None)
        result = company.get_10k_year('2001')
        self.assertEqual(result, None)
        result = company.get_10k_year('hello')
        self.assertEqual(result, None)
        result = company.get_10k_year(True)
        self.assertEqual(result, None)
        result = company.get_10k_year(None)
        self.assertEqual(result, None)
        result = company.get_10k_year(2.4)
        self.assertEqual(result, None)
        result = company.get_10k_year(2018)
        self.assertEqual(result, None)
