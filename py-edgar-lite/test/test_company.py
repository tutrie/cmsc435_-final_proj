import unittest
import requests
from lxml import html

from edgar.company import Company

ORACLE_10K_EXCEL = [['https://www.sec.gov/Archives/edgar/data/1341439/000156459020030125/Financial_Report.xlsx', '2020'],
                    ['https://www.sec.gov/Archives/edgar/data/1341439/000156459019023119/Financial_Report.xlsx', '2019'],
                    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312518201034/Financial_Report.xlsx', '2018'],
                    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312517214833/Financial_Report.xlsx', '2017'],
                    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312516628942/Financial_Report.xlsx', '2016'],
                    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312515235239/Financial_Report.xlsx', '2015'],
                    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312514251351/Financial_Report.xlsx', '2014'],
                    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312513272832/Financial_Report.xlsx', '2013'],
                    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312512284007/Financial_Report.xlsx', '2012'],
                    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312511174819/Financial_Report.xlsx', '2011'],
                    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312510151896/Financial_Report.xlsx', '2010'],
                    ['https://www.sec.gov/Archives/edgar/data/1341439/000095012309018689/Financial_Report.xlsx', '2009'],
                    ['https://www.sec.gov/Archives/edgar/data/1341439/000095013408012257/Financial_Report.xlsx', '2008'],
                    ['https://www.sec.gov/Archives/edgar/data/1341439/000095013407014478/Financial_Report.xlsx', '2007'],
                    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312506151154/Financial_Report.xlsx', '2006']]


class CompanyTestCase(unittest.TestCase):

    def test_get_filings_url(self):
        company = Company("Oracle Corp", "0001341439")
        result = company.get_filings_url(filing_type="10-K")
        expected = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001341439&type=10-K&dateb=&owner=include&count=100"
        self.assertEqual(result, expected)

        result = company.get_filings_url(filing_type="10-Q")
        expected = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001341439&type=10-Q&dateb=&owner=include&count=100"
        self.assertEqual(result, expected)

    def test_get_all_filings(self):
        company = Company("Oracle Corp", "0001341439")
        result = company.get_all_filings(filing_type="10-K")

        url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001341439&type=10-K&dateb=&owner=include&count=100"
        page = requests.get(url, timeout=10)
        expected = html.fromstring(page.content)
        self.assertEqual(html.tostring(result), html.tostring(expected))

    def test_get_company_excel_reports_from_10K(self):
        company = Company("Oracle Corp", "0001341439")
        result = company.get_company_excel_reports_from("10-K")
        self.assertEqual(result, ORACLE_10K_EXCEL)

    def test_download_url(self):
        company = Company("Oracle Corp", "0001341439")
        # download file
        url = "https://www.sec.gov/Archives/edgar/data/1341439/000119312506151154/Financial_Report.xlsx"
        self.assertEqual(True, company.download_file(url, '0001341439'))
        self.assertEqual(False, company.download_file(url, '0123456789'))
        # delete downloaded files


