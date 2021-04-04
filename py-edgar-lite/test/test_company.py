import unittest
from edgar.company import Company

ORACLE_10K_EXCEL = ['https://www.sec.gov/Archives/edgar/data/1341439/000156459020030125/Financial_Report.xlsx',
                    'https://www.sec.gov/Archives/edgar/data/1341439/000156459019023119/Financial_Report.xlsx',
                    'https://www.sec.gov/Archives/edgar/data/1341439/000119312518201034/Financial_Report.xlsx',
                    'https://www.sec.gov/Archives/edgar/data/1341439/000119312517214833/Financial_Report.xlsx',
                    'https://www.sec.gov/Archives/edgar/data/1341439/000119312516628942/Financial_Report.xlsx',
                    'https://www.sec.gov/Archives/edgar/data/1341439/000119312515235239/Financial_Report.xlsx',
                    'https://www.sec.gov/Archives/edgar/data/1341439/000119312514251351/Financial_Report.xlsx',
                    'https://www.sec.gov/Archives/edgar/data/1341439/000119312513272832/Financial_Report.xlsx',
                    'https://www.sec.gov/Archives/edgar/data/1341439/000119312512284007/Financial_Report.xlsx',
                    'https://www.sec.gov/Archives/edgar/data/1341439/000119312511174819/Financial_Report.xlsx',
                    'https://www.sec.gov/Archives/edgar/data/1341439/000119312510151896/Financial_Report.xlsx',
                    'https://www.sec.gov/Archives/edgar/data/1341439/000095012309018689/Financial_Report.xlsx',
                    'https://www.sec.gov/Archives/edgar/data/1341439/000095013408012257/Financial_Report.xlsx',
                    'https://www.sec.gov/Archives/edgar/data/1341439/000095013407014478/Financial_Report.xlsx',
                    'https://www.sec.gov/Archives/edgar/data/1341439/000119312506151154/Financial_Report.xlsx']


class CompanyTestCase(unittest.TestCase):

    def test_get_company_excel_reports_from_10K(self):
        company = Company("Oracle Corp", "0001341439")
        # company.get_all_filings()
        result = company.get_company_excel_reports_from_10K()
        self.assertEqual(result, ORACLE_10K_EXCEL)
        print("got here")

    def test_download_url(self):
        company = Company("Oracle Corp", "0001341439")
        # download file
        url = "https://www.sec.gov/Archives/edgar/data/1341439/000119312506151154/Financial_Report.xlsx"
        self.assertEqual(True, company.download_file(url, '0001341439'))
        self.assertEqual(False, company.download_file(url, '0123456789'))
        # delete downloaded files
