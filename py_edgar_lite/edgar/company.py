import re
import requests
from lxml import html
import lxml
import urllib.parse as urlparse
from urllib.parse import parse_qs

BASE_URL = "https://www.sec.gov"


class Company:
    """
    A class representing a Company in the EDGAR Filling System.

    This class can get the urls of a specified company's 10-K and 10-Q excel reports by providing
    this company's name and CIK number. And also it contains functionalities to download the reports.

    Fields:
        name: Company's name.
        cik: Company's CIK number.
        url: Default url to the company's filing page.
        timeout: Timeout for get requests will be used in the class, default to 10.
        _document_urls: Urls for document buttons on the company's filing page.
        _interactive_urls: Urls for interactive buttons on the company's filing page.
        _excel_urls: Downloading urls for company's 10-K and 10-Q excel reports.
    """

    def __init__(self, name: str, cik: str, timeout: int = 10):
        self.name = name
        self.cik = cik
        self.url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}"
        self.timeout = timeout
        self._document_urls = []
        self._interactive_urls = []
        self._excel_urls = {'10-K': {}, '10-Q': {}}

    def _get(self, url: str) -> requests.models.Response:
        """
        Args:
            url: A url that want to be sending GET request to.

        Returns:
            The response of the GET request if the request was successful within five tries,
            and None if the request was not successful.
        """
        page = requests.get(url, timeout=self.timeout, allow_redirects=True)
        counter = 0

        while counter < 5 and not page.ok:
            page = requests.get(url, timeout=self.timeout, allow_redirects=True)
            counter = counter + 1

        if not page.ok:
            return None

        return page

    def get_filings_url(self, filing_type: str = "", prior_to: str = "",
                        ownership: str = "include", no_of_entries: int = 100) -> str:
        """
        Args:
            filing_type: The type of document you want. i.e. 10-K, 10-Q. If not specified will return all documents.
            prior_to: Time prior which documents are to be retrieved. If not specified will return all documents.
            ownership: Defaults to include. Options are include, exclude, only.
            no_of_entries: Number of reports can be returned. Defaults to 100 and the maximum is 100 as well.

        Returns:
            Returns the url of filing page which contains information for 10-K or 10-Q reports.
        """
        url = self.url + "&type=" + filing_type + "&dateb=" + prior_to + "&owner=" + ownership + "&count=" + str(
            no_of_entries)
        return url

    def get_all_filings(self, filing_type: str = "", prior_to: str = "",
                        ownership: str = "include", no_of_entries: int = 100) -> lxml.html.HtmlElement:
        """
        Args:
            filing_type: The type of document you want. i.e. 10-K, 10-Q. If not specified will return all documents.
            prior_to: Time prior which documents are to be retrieved. If not specified will return all documents.
            ownership: Defaults to include. Options are include, exclude, only.
            no_of_entries: Number of reports can be returned. Defaults to 100 and the maximum is 100 as well.

        Returns:
            Returns the HTML of the filing page. If the GET request to the filing url was not successful return None.
        """
        url = self.get_filings_url(filing_type, prior_to, ownership, no_of_entries)
        page = self._get(url)

        if page:
            return html.fromstring(page.content)
        else:
            return None

    def get_company_excel_reports_from(self, filing_type: str = "", prior_to: str = "",
                                       ownership: str = "include", no_of_entries: int = 100) -> dict:
        """
        Args:
            filing_type: The type of document you want. i.e. 10-K, 10-Q. If not specified will return all documents.
            prior_to: Time prior which documents are to be retrieved. If not specified will return all documents.
            ownership: Defaults to include. Options are include, exclude, only.
            no_of_entries: Number of reports can be returned. Defaults to 100 and the maximum is 100 as well.

        Returns:
            A dictionary of urls for the company's 10-K or 10-Q excel reports.
        """
        regex = re.search('10-K|10-Q', filing_type)
        if not regex:
            return None

        page = self.get_all_filings(filing_type, prior_to, ownership, no_of_entries)
        if page is None:
            return None

        self._document_urls = [BASE_URL + elem.attrib["href"]
                               for elem in page.xpath("//*[@id='documentsbutton']") if elem.attrib.get("href")]

        self._interactive_urls = [BASE_URL + elem.attrib["href"]
                                  for elem in page.xpath("//*[@id='interactiveDataBtn']") if elem.attrib.get("href")]

        if filing_type == "10-K":
            self._get_company_10_k_excel_report()
        else:
            self._get_company_10_q_excel_report()

        return self._excel_urls[filing_type]

    def _get_company_10_k_excel_report(self) -> None:
        """
        A private method that parse the company's 10-K excel report urls and store them into the _excel_urls dictionary.
        The urls are put into a dictionary with corresponding year as its key. For each year, the 10-K report is being
        stored as a list containing one single url.

        So the _excel_urls after calling this function could look like:
            {"10-K": {"2020": [url], "2019": [url], "2018": [url]} }
        """
        processed = 0

        for document_url in self._document_urls:
            accession_num = get_accession_number(self._interactive_urls[processed])
            if re.search(accession_num, document_url) is None:
                continue

            new_url = '/'.join(document_url.split('/')[:-1] + ["Financial_Report.xlsx"])
            year = get_10k_year_from_url(new_url)
            self._excel_urls["10-K"][year] = [new_url]

            processed += 1
            if processed == len(self._interactive_urls):
                break

    def _get_company_10_q_excel_report(self):
        """
        A private method that parse the company's 10-q excel report urls and store them into the _excel_urls dictionary.
        The urls are put into a dictionary with corresponding year as its key. For each year, there is a list of 10-Q
        urls that are sorted based on its quarter number.

        So the _excel_urls after calling this function could look like:
            {"10-Q": {"2020": [q1_url, q2_url, q3_url], "2019": [q1_url, q2_url, q3_url]} }
        """
        processed = 0

        for document_url in self._document_urls:
            accession_num = get_accession_number(self._interactive_urls[processed])
            if re.search(accession_num, document_url) is None:
                continue

            new_url = '/'.join(document_url.split('/')[:-1] + ["Financial_Report.xlsx"])
            year, quarter_seq = get_10q_year_seq_number(new_url)
            url_lst = self._excel_urls["10-Q"].get(year, [])
            url_lst.append((new_url, quarter_seq))

            self._excel_urls["10-Q"][year] = url_lst

            processed += 1
            if processed == len(self._interactive_urls):
                break

        for _, url_lst in self._excel_urls["10-Q"].items():
            url_lst.sort(key=lambda x: x[1])
            url_lst[:] = list(map(lambda x: x[0], url_lst))

    def download_file(self, url: str) -> bool:
        """
        Downloads the file from the given url.

        Args:
            url: The downloading url of the file wants to be downloaded.

        Returns:
            True is downloading is successful, False other wise.
        """
        req = self._get(url)
        if req is None:
            req = self._get(url[:-1])

        if req:
            file = open('report_' + '_'.join(self.name.split(' ')) + '.xlsx', 'wb')
            file.write(req.content)
            file.close()
            return True
        return False

    def download_10k_reports(self, prior_to: str = "", ownership: str = "include",
                             no_of_entries: int = 100) -> None:
        """
        Downloads the 10-K excel reports of the current company.

        Args:
            prior_to: Time prior which documents are to be retrieved. If not specified will return all documents.
            ownership: Defaults to include. Options are include, exclude, only.
            no_of_entries: Number of reports can be returned. Defaults to 100 and the maximum is 100 as well.
        """
        self.get_company_excel_reports_from("10-K", prior_to, ownership, no_of_entries)
        dict_10k = self._excel_urls['10-K']

        for year in dict_10k.keys():
            url = dict_10k[year][0]
            req = self._get(url)

            if req is None:
                req = self._get(url[:-1])

            if req is not None:
                company_name = '_'.join(self.name.split(' '))
                file = open(f'10K_{year}_report_{company_name}.xlsx', 'wb')
                file.write(req.content)
                file.close()

    def download_10q_reports(self, prior_to: str = "", ownership: str = "include",
                             no_of_entries: int = 100) -> None:
        """
        Downloads the 10-Q excel reports of the current company.

        Args:
            prior_to: Time prior which documents are to be retrieved. If not specified will return all documents.
            ownership: Defaults to include. Options are include, exclude, only.
            no_of_entries: Number of reports can be returned. Defaults to 100 and the maximum is 100 as well.
        """
        self.get_company_excel_reports_from("10-Q", prior_to, ownership, no_of_entries)
        dict_10q = self._excel_urls['10-Q']

        if not dict_10q:
            self.get_company_excel_reports_from("10-Q")

        for year in dict_10q.keys():
            for quarter in range(0, len(dict_10q[year])):
                url = dict_10q[year][quarter]
                req = self._get(url)

                if req is None:
                    req = self._get(url[:-1])

                if req is not None:
                    company_name = '_'.join(self.name.split(' '))
                    file = open(f'10Q_{year}_{quarter + 1}_report_{company_name}.xlsx', 'wb')
                    file.write(req.content)
                    file.close()

    def get_10k_year(self, year: str) -> str:
        """
        Args:
            year: The year of the report url that wants to be retrieved.

        Returns:
            The url of specified year's 10-K excel report.
        """
        dict_10k = self._excel_urls['10-K']
        if not dict_10k:
            self.get_company_excel_reports_from("10-K")
            dict_10k = self._excel_urls['10-K']

        url_list = dict_10k.get(year)
        if url_list:
            return url_list[0]
        return None

    def get_10q_year_quarter(self, year: str, quarter: str) -> str:
        """
        Args:
            year: The year of the report url that wants to be retrieved.
            quarter: The quarter of the report url that wants to be retrieved.

        Returns:
            The url of specified year and quarter's 10-K excel report.
        """
        try:
            quarter = int(quarter)
        except ValueError:
            return None

        dict_10q = self._excel_urls['10-Q']
        if not dict_10q:
            self.get_company_excel_reports_from("10-Q")
            dict_10q = self._excel_urls['10-Q']

        url_list = dict_10q.get(year)
        if url_list:
            if quarter <= len(url_list):
                return url_list[quarter - 1]

        return None


def get_10k_year_from_url(url: str) -> str:
    """
        Args:
            url: The url to a 10-K excel document.

        Returns:
            A string represent the year corresponds to the 10-K excel document.
    """
    url = url.split('/')
    return '20' + url[7][10:12]


def get_10q_year_seq_number(url: str) -> tuple:
    """
    Args:
        url: The url to a 10-Q excel document.

    Returns:
       A tuple of string with two elements, the first being the year corresponds to the 10-Q excel document,
       the second being the sequence number of this document.
    """
    url = url.split('/')
    return ['20' + url[7][10:12], url[7][12:]]


def get_accession_number(interactive_url: str) -> str:
    """
    Args:
        interactive_url: The url to a 10-Q excel document.

    Returns:
       A string of the accession number of the particular 10-Q document.
    """
    parsed = urlparse.urlparse(interactive_url)
    accession_num = parse_qs(parsed.query)['accession_number']

    return accession_num[0]
