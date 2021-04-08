import unittest
import requests
from lxml import html
import urllib.parse as urlparse
from urllib.parse import parse_qs

from edgar.company import Company


ORACLE_10K_EXCEL = [
    ['https://www.sec.gov/Archives/edgar/data/1341439/000156459020030125/Financial_Report.xlsx', '2020'],
    ['https://www.sec.gov/Archives/edgar/data/1341439/000156459019023119/Financial_Report.xlsx', '2019'],
    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312518201034/Financial_Report.xlsx', '2018'],
    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312517214833/Financial_Report.xlsx', '2017'],
    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312516628942/Financial_Report.xlsx', '2016'],
    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312515235239/Financial_Report.xlsx', '2015'],
    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312514251351/Financial_Report.xlsx', '2014'],
    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312513272832/Financial_Report.xlsx', '2013'],
    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312512284007/Financial_Report.xlsx', '2012'],
    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312511174819/Financial_Report.xlsx', '2011'],
    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312510151896/Financial_Report.xlsx', '2010']]

ORACLE_10Q_EXCEL = {
    '2021': [
        ('https://www.sec.gov/Archives/edgar/data/1341439/000156459021012539/Financial_Report.xlsx', '012539')],
    '2020': [
        ('https://www.sec.gov/Archives/edgar/data/1341439/000156459020010833/Financial_Report.xlsx', '010833'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000156459020043448/Financial_Report.xlsx', '043448'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000156459020056896/Financial_Report.xlsx', '056896')],
    '2019': [
        ('https://www.sec.gov/Archives/edgar/data/1341439/000156459019008273/Financial_Report.xlsx', '008273'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000156459019034717/Financial_Report.xlsx', '034717'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000156459019045966/Financial_Report.xlsx', '045966')],
    '2018': [
        ('https://www.sec.gov/Archives/edgar/data/1341439/000156459018023315/Financial_Report.xlsx', '023315'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000156459018031113/Financial_Report.xlsx', '031113'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312518090646/Financial_Report.xlsx', '090646')],
    '2017': [
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312517087309/Financial_Report.xlsx', '087309'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312517287455/Financial_Report.xlsx', '287455'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312517372232/Financial_Report.xlsx', '372232')],
    '2016': [
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312516510333/Financial_Report.xlsx', '510333'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312516713596/Financial_Report.xlsx', '713596'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312516797253/Financial_Report.xlsx', '797253')],
    '2015': [
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312515098586/Financial_Report.xlsx', '098586'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312515323532/Financial_Report.xlsx', '323532'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312515407703/Financial_Report.xlsx', '407703')],
    '2014': [
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312514108126/Financial_Report.xlsx', '108126'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312514350291/Financial_Report.xlsx', '350291'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312514448728/Financial_Report.xlsx', '448728')],
    '2013': [
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312513122271/Financial_Report.xlsx', '122271'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312513373455/Financial_Report.xlsx', '373455'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312513481081/Financial_Report.xlsx', '481081')],
    '2012': [
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312512129918/Financial_Report.xlsx', '129918'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312512401697/Financial_Report.xlsx', '401697'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312512513009/Financial_Report.xlsx', '513009')],
    '2011': [
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312511081178/Financial_Report.xlsx', '081178'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312511255436/Financial_Report.xlsx', '255436'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312511351954/Financial_Report.xlsx', '351954')],
     '2010': [
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312510070192/Financial_Report.xlsx', '070192'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312510219697/Financial_Report.xlsx', '219697'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312510285703/Financial_Report.xlsx', '285703')],
    '2009': [
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312509195193/Financial_Report.xlsx', '195193'),
        ('https://www.sec.gov/Archives/edgar/data/1341439/000119312509257212/Financial_Report.xlsx', '257212')]}

GET_FORMS_ONLY_10K = {'10-K':
    [['https://www.sec.gov/Archives/edgar/data/1341439/000156459020030125/Financial_Report.xlsx',
    '2020'],
    ['https://www.sec.gov/Archives/edgar/data/1341439/000156459019023119/Financial_Report.xlsx',
    '2019'],
    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312518201034/Financial_Report.xlsx',
    '2018'],
    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312517214833/Financial_Report.xlsx',
    '2017'],
    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312516628942/Financial_Report.xlsx',
    '2016'],
    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312515235239/Financial_Report.xlsx',
    '2015'],
    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312514251351/Financial_Report.xlsx',
    '2014'],
    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312513272832/Financial_Report.xlsx',
    '2013'],
    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312512284007/Financial_Report.xlsx',
    '2012'],
    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312511174819/Financial_Report.xlsx',
    '2011'],
    ['https://www.sec.gov/Archives/edgar/data/1341439/000119312510151896/Financial_Report.xlsx',
    '2010']],
    '10-Q': {}}


class CompanyTestCase(unittest.TestCase):

    def test_get_filings_url(self):
        company = Company("Oracle Corp", "0001341439")
        result = company.get_filings_url(filing_type="10-K")
        expected = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001341439&type=10-K&dateb=&owner" \
                   "=include&count=100"
        self.assertEqual(result, expected)

        result = company.get_filings_url(filing_type="10-Q")
        expected = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001341439&type=10-Q&dateb=&owner" \
                   "=include&count=100"
        self.assertEqual(result, expected)

    def test_get_all_filings(self):
        company = Company("Oracle Corp", "0001341439")
        result = company.get_all_filings(filing_type="10-K")

        url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001341439&type=10-K&dateb=&owner" \
              "=include&count=100"
        page = requests.get(url, timeout=10)
        expected = html.fromstring(page.content)
        self.assertEqual(html.tostring(result), html.tostring(expected))

    def test_get_company_excel_reports_from_10K(self):
        company = Company("Oracle Corp", "0001341439")
        result = company.get_company_excel_reports_from("10-K")
        self.assertEqual(result, ORACLE_10K_EXCEL)

    def test_get_company_excel_reports_from_10Q(self):
        company = Company("Oracle Corp", "0001341439")
        result = company.get_company_excel_reports_from("10-Q")
        self.assertEqual(result, ORACLE_10Q_EXCEL)

    def test_download_url(self):
        company = Company("Oracle Corp", "0001341439")
        # download file
        url = "https://www.sec.gov/Archives/edgar/data/1341439/000119312506151154/Financial_Report.xlsx"
        self.assertEqual(True, company.download_file(url, '0001341439'))
        self.assertEqual(False, company.download_file(url, '0123456789'))
        # delete downloaded files

    # There's some minor thing need to update in these two test
    def test_correct_return_10k(self):
        length_10k_values = len(GET_FORMS_ONLY_10K['10-K'])
        company = Company("Oracle Corp", "0001341439")
        company.get_company_excel_reports_from("10-K")
        result = company.get_form_types()
        self.assertEqual(result, GET_FORMS_ONLY_10K)
        result = company.get_10k_year('2020')
        self.assertEqual(result, GET_FORMS_ONLY_10K['10-K'][0])
        result = company.get_10k_year('2019')
        self.assertEqual(result, GET_FORMS_ONLY_10K['10-K'][1])
        result = company.get_10k_year('2018')
        self.assertEqual(result, GET_FORMS_ONLY_10K['10-K'][2])
        result = company.get_10k_year('2007')
        self.assertEqual(result, GET_FORMS_ONLY_10K['10-K'][length_10k_values - 2])
        result = company.get_10k_year('2006')
        self.assertEqual(result, GET_FORMS_ONLY_10K['10-K'][length_10k_values - 1])

    def test_incorrect_return_10k(self):
        company = Company("Oracle Corp", "0001341439")
        company.get_company_excel_reports_from("10-K")
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
