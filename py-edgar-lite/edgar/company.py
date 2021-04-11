import re
import time
from typing import List
import requests
from lxml import html
import lxml
import urllib.parse as urlparse
from urllib.parse import parse_qs

BASE_URL = "https://www.sec.gov"


def get_10k_year_from_url(url):
    url = url.split('/')
    return '20' + url[7][10:12]


def get_10q_year_seq_number(url):
    url = url.split('/')
    return ['20' + url[7][10:12], url[7][12:]]


def get_accession_number(interactive_url):
    parsed = urlparse.urlparse(interactive_url)
    accession_num = parse_qs(parsed.query)['accession_number']

    return accession_num[0]


class Company:

    def __init__(self, name, cik, timeout=10):
        self.name = name
        self.cik = cik
        self.url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}"
        self.timeout = timeout
        self._document_urls = []
        self._interactive_urls = []
        # '10-K': [url: str, year: ]
        # '10-Q': {year: [url]}
        self._excel_urls = {'10-K': [], '10-Q': {}}

    @property
    def document_urls(self):
        return list(set(self._document_urls))

    def _get(self, url):
        """
        A private method for GET request.
        """
        return requests.get(url, timeout=self.timeout)

    def get_filings_url(self, filing_type="", prior_to="", ownership="include", no_of_entries=100) -> str:
        """
        Return the url of filing page which contains information for 10-K or 10-Q reports.
        """
        url = self.url + "&type=" + filing_type + "&dateb=" + prior_to + "&owner=" + ownership + "&count=" + str(
            no_of_entries)
        return url

    def get_all_filings(self, filing_type="", prior_to="", ownership="include",
                        no_of_entries=100) -> lxml.html.HtmlElement:
        """
        Return the HTML of the filing page. If the GET request to the filing url was not successful return None.
        """
        # url of the filing page
        url = self.get_filings_url(filing_type, prior_to, ownership, no_of_entries)
        # GET request to the filing page
        page = self._get(url)

        # Request up to five more times if the GET request was not successful.
        counter = 0
        while counter < 5 and not page.ok:
            page = self._get(url)
            counter = counter + 1

        if not page.ok:
            return None

        return html.fromstring(page.content)

    def _get_company_10_k_excel_report(self):
        """
        A private method that parse the company's 10-K excel report urls.
        """
        processed = 0

        for document_url in self._document_urls:
            accession_num = get_accession_number(self._interactive_urls[processed])
            # Check if the document_url corresponds to the interactive_url, means the document has excel report
            if re.search(accession_num, document_url) is None:
                continue

            # split the original document url by '/', replace the last element with 'Financial_Report.xlsx'
            new_url = '/'.join(document_url.split('/')[:-1] + ["Financial_Report.xlsx"])
            entry = [new_url, get_10k_year_from_url(new_url)]
            self._excel_urls["10-K"].append(entry)

            processed += 1
            # Check if all the excel reports has been processed
            if processed == len(self._interactive_urls):
                break

    def _get_company_10_q_excel_report(self):
        """
        Parse the company's 10-Q excel report urls.
        """
        processed = 0

        for document_url in self._document_urls:
            accession_num = get_accession_number(self._interactive_urls[processed])
            # Check if the document_url corresponds to the interactive_url, means the document has excel report
            if re.search(accession_num, document_url) is None:
                continue

            # split the original document url by '/', replace the last element with 'Financial_Report.xlsx'
            new_url = '/'.join(document_url.split('/')[:-1] + ["Financial_Report.xlsx"])
            year, quarter_seq = get_10q_year_seq_number(new_url)
            url_lst = self._excel_urls["10-Q"].get(year, [])
            # The 10Q entry is formatted as (url, quarter_seq)
            url_lst.append((new_url, quarter_seq))

            self._excel_urls["10-Q"][year] = url_lst

            processed += 1
            # Check if all the excel reports has been processed
            if processed == len(self._interactive_urls):
                break

        for _, url_lst in self._excel_urls["10-Q"].items():
            # Sort the url_lst base on the quarter sequence number so that the entries are ordered based on quarter.
            # [first_quarter, second_quarter, third_quarter]
            url_lst.sort(key=lambda x: x[1])
            url_lst[:] = list(map(lambda x: x[0], url_lst))

    def get_company_excel_reports_from(self, report_type, prior_to="", no_of_entries=100) -> dict[str, List[str]]:
        """
        Retrieve the company's excel format 10-K or 10-Q report
        """
        # determine type of request
        regex = re.search('10-K|10-Q', report_type)
        if not regex:
            return None

        if self._excel_urls[report_type]:
            return self._excel_urls[report_type]

        page = self.get_all_filings(filing_type=report_type, prior_to=prior_to, no_of_entries=no_of_entries)
        if page is None:
            return None

        self._document_urls = [BASE_URL + elem.attrib["href"]
                               for elem in page.xpath("//*[@id='documentsbutton']") if elem.attrib.get("href")]

        self._interactive_urls = [BASE_URL + elem.attrib["href"]
                                  for elem in page.xpath("//*[@id='interactiveDataBtn']") if elem.attrib.get("href")]

        if report_type == "10-K":
            self._get_company_10_k_excel_report()
        else:
            self._get_company_10_q_excel_report()

        return self._excel_urls[report_type]

    def download_file(self, url) -> bool:
        """
        Download the file from the given url.
        """
        req = requests.get(url, allow_redirects=True)
        file = open('report_' + '_'.join(self.name.split(' ')) + '.xlsx', 'wb')
        file.write(req.content)
        file.close()
        return True

    def get_existing_forms(self) -> dict[str, dict]:
        """
        Return all existing 10-K and 10-Q's
        """
        return self._excel_urls

    def get_10k_year(self, year):
        """
        Return the url of specified year's 10-K excel report.
        """
        ten_k_lst = self._excel_urls['10-K']
        if not ten_k_lst:
            self._get_company_10_k_excel_report()
        for idx in ten_k_lst:
            if idx[1] == year:
                return idx[0]
        return None

    def get_10q_year_quarter(self, year, quarter):
        """
        Return the url of specified year and quarter's 10-Q excel report.
        """
        try:
            quarter = int(quarter)
        except ValueError:
            return None

        ten_q_dict = self._excel_urls['10-Q']
        if not ten_q_dict:
            self._get_company_10_q_excel_report()
        entry = ten_q_dict.get(year)

        if entry:
            if quarter <= len(entry):
                return entry[quarter - 1]

        return None
