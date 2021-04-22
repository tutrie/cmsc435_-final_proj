from os.path import dirname, realpath
from urllib.parse import parse_qs
import urllib.parse as urlparse
from lxml import html
import requests
import lxml
import re

BASE_URL = "https://www.sec.gov"


class EdgarScraper:
    """
    A class representing a Company in the EDGAR Filling System.

    This class can get the urls of a specified company's 10-K and 10-Q excel
    reports by providing this company's name and CIK number. And also it
    contains functionalities to download the reports.

    Fields:
        name: Company's name.
        cik: Company's CIK number.
        url: Default url to the company's filing page.
        timeout: Timeout for get requests will be used in the class, default to
            10.
        _document_urls: Urls for document buttons on the company's filing page.
        _interactive_urls: Urls for interactive buttons on the company's
            filing page.
        _excel_urls: Downloading urls for company's 10-K and 10-Q excel
            reports.
    """

    def __init__(self, name, cik, timeout=10):
        self.name = name
        self.cik = cik
        self.url = 'https://www.sec.gov/cgi-bin/browse-edgar?' + \
            f'action=getcompany&CIK={cik}'
        self.timeout = timeout
        self._document_urls = []
        self._interactive_urls = []
        self._excel_urls = {'10-K': {}}

    def _get(self, url: str) -> requests.models.Response:
        """
        A private function that send a GET request to a url.

        Args:
            url: A url that want to be sending GET request to.

        Returns:
            The response of the GET request if the request was successful
            within five tries, and None if the request was not successful.
        """
        page = requests.get(url, timeout=self.timeout, allow_redirects=True)
        counter = 0

        while counter < 5 and not page.ok:
            page = requests.get(
                url, timeout=self.timeout, allow_redirects=True
            )
            counter = counter + 1

        if not page.ok:
            return None

        return page

    def get_filings_url(self,
                        filing_type: str = "10-K",
                        prior_to: str = "2015",
                        ownership: str = "include",
                        no_of_entries: int = 100) -> str:
        """
        A function that gets the url link to a company's overall filing page.

        Args:
            filing_type: The type of document you want. i.e. 10-K, 10-Q. If not
            specified will return all documents.
            prior_to: Time prior which documents are to be retrieved. If not
            specified will return all documents.
            ownership: Defaults to include. Options are include, exclude, only.
            no_of_entries: Number of reports can be returned. Defaults to 100
            and the maximum is 100 as well.

        Returns:
            Returns the url of filing page which contains information for 10-K
            or 10-Q reports.
        """
        url = self.url + "&type=" + filing_type + "&dateb=" + prior_to + \
            "&owner=" + ownership + "&count=" + str(
                no_of_entries)
        return url

    def get_all_filings(self,
                        filing_type: str = "",
                        prior_to: str = "2015",
                        ownership: str = "include",
                        no_of_entries: int = 100) -> lxml.html.HtmlElement:
        """
        A function that get the htmlElement from the GET result of the filing
        page of a company.

        Args:
            filing_type: The type of document you want. i.e. 10-K, 10-Q. If not
            specified will return all documents.
            prior_to: Time prior which documents are to be retrieved. If not
            specified will return all documents.
            ownership: Defaults to include. Options are include, exclude, only.
            no_of_entries: Number of reports can be returned. Defaults to 100
            and the maximum is 100 as well.

        Returns:
            Returns the HTML of the filing page. If the GET request to the
            filing url was not successful return None.
        """
        url = self.get_filings_url(filing_type, prior_to, ownership,
                                   no_of_entries)
        page = self._get(url)

        if page:
            return html.fromstring(page.content)
        else:
            return None

    def _get_company_10_k_excel_report(self) -> None:
        """
        A private method that parse the company's 10-K excel report urls and
        store them into the _excel_urls dictionary. The urls are put into a
        dictionary with corresponding year as its key. For each year, the 10-K
        report is being stored as a list containing one single url.

        So the _excel_urls after calling this function could look like:
            {"10-K": {"2020": [url], "2019": [url], "2018": [url]} }
        """
        processed = 0

        for document_url in self._document_urls:
            accession_num = get_accession_number(
                self._interactive_urls[processed])
            if re.search(accession_num, document_url) is None:
                continue

            new_url = '/'.join(document_url.split('/')
                               [:-1] + ["Financial_Report.xlsx"])
            year = get_10k_year_from_url(new_url)
            self._excel_urls["10-K"][year] = [new_url]

            processed += 1
            if processed == len(self._interactive_urls):
                break

    def get_company_excel_reports_from(self,
                                       filing_type: str = "10-K",
                                       prior_to: str = "2015",
                                       ownership: str = "include",
                                       no_of_entries: int = 100) -> dict:
        """
        A function that retrieve the either 10-Q or 10-K excel reports from
        the company's filing page.

        Args:
            filing_type: The type of document you want. i.e. 10-K, 10-Q. If not
                specified will return all documents.

            prior_to: Time prior which documents are to be retrieved. If not
                specified will return all documents.

            ownership: Defaults to include. Options are include, exclude, only.

            no_of_entries: Number of reports can be returned. Defaults to 100
                and the maximum is 100 as well.

        Returns:
            A dictionary of urls for the company's 10-K or 10-Q excel reports.
        """
        # determine type of request
        regex = re.search('10-K', filing_type)
        if not regex:
            return None

        page = self.get_all_filings(
            filing_type, prior_to, ownership, no_of_entries)

        if page is None:
            return None

        self._document_urls = []
        for elem in page.xpath("//*[@id='documentsbutton']"):
            if elem.attrib.get("href"):
                self._document_urls.append(BASE_URL + elem.attrib["href"])

        self._interactive_urls = []
        for elem in page.xpath("//*[@id='interactiveDataBtn']"):
            if elem.attrib.get("href"):
                self._interactive_urls.append(BASE_URL + elem.attrib["href"])

        if filing_type != "10-K":
            return None

        self._get_company_10_k_excel_report()
        return self._excel_urls[filing_type]

    def download_file(self, url: str) -> str:
        """
        Downloads the file from the given url.

        Args:
            url: The downloading url of the file wants to be downloaded.

        Returns:
            File path of downloaded file is downloading is successful; None
            otherwise.
        """
        req = self._get(url)
        if req is None:
            req = self._get(url[:-1])

        if req is not None:
            # For production:
            # dir_name = '~' + '/downloaded_reports/'

            # For development:
            dir_name = dirname(realpath(__file__)).replace(
                'report_schema/raw_report', 'downloaded_reports/'
            )
            file_name = 'report_' + '_'.join(self.name.split(' ')) + '.xlsx'
            file_path = f'{dir_name}{file_name}'
            file = open(file_path, 'wb')
            file.write(req.content)
            file.close()
            return file_path
        return None

    def download_10k_reports(self,
                             prior_to: str = "",
                             ownership: str = "include",
                             no_of_entries: int = 100) -> dict:
        """
        Downloads the 10-K excel reports of the current company.

        Args:
            prior_to: Time prior which documents are to be retrieved. If not
                specified will return all documents.

            ownership: Defaults to include. Options are include, exclude, only.

            no_of_entries: Number of reports can be returned. Defaults to 100
                and the maximum is 100 as well.

        Returns:
            A dictionary where key is a year and the value is the file path for
            the file corresponding to that year.
        """
        self.get_company_excel_reports_from(
            "10-K", prior_to, ownership, no_of_entries)
        dict_10k = self._excel_urls['10-K']

        file_paths = {}

        for year in dict_10k.keys():
            url = dict_10k[year][0]
            req = self._get(url)

            if req is None:
                req = self._get(url[:-1])

            if req is not None:
                company_name = '_'.join(self.name.split(' '))

                # For production:
                # dir_name = '~' + '/downloaded_reports/'

                # For development:
                dir_name = dirname(realpath(__file__)).replace(
                    'report_schema/raw_report', 'downloaded_reports/'
                )

                filename = f'10K_{year}_report_{company_name}.xlsx'
                full_file = f'{dir_name}{filename}'
                file = open(full_file, 'wb')
                file.write(req.content)
                file.close()

                file_paths[year] = full_file
        return file_paths

    def get_existing_forms(self) -> dict:
        """
        Return all existing 10-K url.
        """
        return self._excel_urls

    def get_10k_year(self, year: str) -> str:
        """
        Get the url of a specific year's 10-K excel report of a company.

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


def get_10k_year_from_url(url: str) -> str:
    """
    Get the year and quarter of the given 10-K excel report url.

    Args:
        url: The url to a 10-K excel document.

    Returns:
        A string represent the year corresponds to the 10-K excel document.
    """
    url = url.split('/')
    return '20' + url[7][10:12]


def get_accession_number(interactive_url: str) -> str:
    """
    Get the accession number of the given 10-Q interactive button's url.

    Args:
        interactive_url: The url to a 10-Q excel document.

    Returns:
    A string of the accession number of the particular 10-Q document.
    """
    parsed = urlparse.urlparse(interactive_url)
    accession_num = parse_qs(parsed.query)['accession_number']

    return accession_num[0]
