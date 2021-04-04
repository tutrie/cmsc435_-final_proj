from typing import List
import requests
from lxml import html
import lxml

BASE_URL = "https://www.sec.gov"


class Company:

    def __init__(self, name, cik, timeout=10):
        self.name = name
        self.cik = cik
        self.url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}"
        self.timeout = timeout
        self._document_urls = []
        self._excel_urls = []

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

    def get_company_excel_reports_from_10K(self) -> List[str]:
        """
        Retrieve the company's excel format 10-K report
        """
        page = self.get_all_filings(filing_type="10-K")

        self._document_urls = [BASE_URL + elem.attrib["href"]
                               for elem in page.xpath("//*[@id='documentsbutton']") if elem.attrib.get("href")]
        self._excel_urls = ['/'.join(elem.split('/')[:-1] + ["Financial_Report.xlsx"])
                            for elem in self._document_urls]
        return self._excel_urls

    def download_file(self, url, cid) -> bool:
        if not cid == self.cik:
            return False

        req = requests.get(url, allow_redirects=True)
        # may need to append .xlsx to end of file name
        file = open('report_' + self.name + '.xlsx', 'wb')
        file.write(req.content)
        file.close()
        return True
