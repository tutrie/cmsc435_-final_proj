import re
from typing import List
import requests
from lxml import html
import lxml

BASE_URL = "https://www.sec.gov"


def get_10k_year(url):
    url = url.split('/')
    return '20' + url[7][10:12]


def get_10Q_year_seq_number(url):
    url = url.split('/')
    return ['20' + url[7][10:12], url[7][12:]]


class Company:

    def __init__(self, name, cik, timeout=10):
        self.name = name
        self.cik = cik
        self.url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}"
        self.timeout = timeout
        self._document_urls = []
        # [url, year]
        # [url, year, quarterNumber]
        self._excel_urls = {'10-K': [], '10-Q': {}}

    @property
    def document_urls(self):
        return list(set(self._document_urls))

    def _get(self, url):
        return requests.get(url, timeout=self.timeout)

    def get_filings_url(self, filing_type="", prior_to="", ownership="include", no_of_entries=100) -> str:
        url = self.url + "&type=" + filing_type + "&dateb=" + prior_to + "&owner=" + ownership + "&count=" + str(
            no_of_entries)
        return url

    def get_all_filings(self, filing_type="", prior_to="", ownership="include",
                        no_of_entries=100) -> lxml.html.HtmlElement:
        url = self.get_filings_url(filing_type, prior_to, ownership, no_of_entries)
        page = self._get(url)
        return html.fromstring(page.content)

    # How often should we update the report, or should we just redo the scraping each time we call the function?
    def _get_company_10_K_excel_report(self):
        """
        Parse the company's 10-K excel report urls.
        """
        for elem in self._document_urls:
            # split the original document url by '/', replace the last element with 'Financial_Report.xlsx'
            new_url = '/'.join(elem.split('/')[:-1] + ["Financial_Report.xlsx"])
            entry = [new_url, get_10k_year(new_url)]
            self._excel_urls["10-K"].append(entry)

    def _get_company_10_Q_excel_report(self):
        """
        Parse the company's 10-Q excel report urls.
        """
        for elem in self._document_urls:
            # split the original document url by '/', replace the last element with 'Financial_Report.xlsx'
            new_url = '/'.join(elem.split('/')[:-1] + ["Financial_Report.xlsx"])
            year, quarter_seq = get_10Q_year_seq_number(new_url)
            url_lst = self._excel_urls["10-Q"].get(year, [])
            # The 10Q entry is formatted as (url, quarter_seq)
            url_lst.append(new_url, quarter_seq)

            self._excel_urls["10-Q"][year] = url_lst

        

    def get_company_excel_reports_from(self, report_type) -> List[str]:
        """
        Retrieve the company's excel format 10-K or 10-Q report
        """
        # determine type of request
        regex = re.search('10-K|10-Q', report_type)
        if not regex:
            return None

        page = self.get_all_filings(filing_type=report_type)

        self._document_urls = [BASE_URL + elem.attrib["href"]
                               for elem in page.xpath("//*[@id='documentsbutton']") if elem.attrib.get("href")]

        if report_type == "10-K":
            self._get_company_10_K_excel_report()
        else:
            self._get_company_10_Q_excel_report()

        return self._excel_urls[report_type]

    def download_file(self, url, cid) -> bool:
        if not cid == self.cik:
            return False

        req = requests.get(url, allow_redirects=True)
        file = open('report_' + self.name + '.xlsx', 'wb')
        file.write(req.content)
        file.close()
        return True

    # return all existing 10-K and 10-Q's
    def get_form_types(self):
        return self._excel_urls

    # return 10-K
    def get_10k_year(self, year):
        tenK_lst = self._excel_urls['10-K']
        for idx in tenK_lst:
            if idx[1] == year:
                return idx[0]
        return None

    # return 10-Q
    # def get_10Q_year(self, year, quarter):
    #     tenQ_lst = self._excel_urls['10-Q']
    #     print(tenQ_lst)
    #     for idx in tenQ_lst:
    #         if idx.get(year) is None:
    #             continue
    #         else:
    #             print(idx[year][1])
    #             if idx[year][1] == quarter:
    #                 return idx[year][0]
    #     return None
        # return 10-Q
    def get_10Q_year(self, year, quarter):
        tenQ_lst = self._excel_urls['10-Q']
        for idx in tenQ_lst:
            if idx[1] == year:
                if idx[2] == quarter:
                    return idx[0]
        return None


company = Company("Oracle Corp", "0001341439")
company.get_company_excel_reports_from("10-Q")
print(company.get_form_types())
result = company.get_10Q_year('2020', '2')
print(result)
