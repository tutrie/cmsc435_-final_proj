# EDGAR-Lite
A small library for 10-Q and 10-K form url retrevial from SEC's edgar.

## Environment Setup
Be sure to run the following commands in terminal to install the required dependencies:
```bash
pip install requests
pip install lxml
pip install edgar
```

## Example
To get all urls to a company's 10-K excel reports, run

``` python
from edgar.company import Company
company = Company("Oracle Corp", "0001341439")
urls = company.get_company_excel_reports_from("10-K")
```

To get the url of a company's 2019 10-K excel report, run

``` python
from edgar.company import Company
company = Company("Oracle Corp", "0001341439")
company.get_company_excel_reports_from("10-K")
url = company.get_10k_year('2019')
```

To get all urls of a company's 10-Q excel report, run

``` python
from edgar.company import Company
company = Company("Oracle Corp", "0001341439")
urls = company.get_company_excel_reports_from("10-Q")
```

To get the url of a company's 2019's first quarter 10-Q excel report, run

``` python
from edgar.company import Company
company = Company("Oracle Corp", "0001341439")
company.get_company_excel_reports_from("10-Q")
url = company.get_10k_year('2019', '1')
```

## API

### Company
```python
Company(name, cik, timeout=10)
```
* name (company name)
* cik (company CIK number)
* timeout (optional) (default: 10)

#### Methods

`get_filings_url(self, filing_type="", prior_to="", ownership="include", no_of_entries=100) -> str`

Returns a url to fetch filings data
* filing_type: The type of document you want. i.e. 10-K, 10-Q. If not specified, it'll return all documents
* prior_to: Time prior which documents are to be retrieved. If not specified, it'll return all documents
* ownership: defaults to include. Options are include, exclude, only.
* no_of_entries: defaults to 100. Returns the number of entries to be returned. Maximum is 100.


`get_company_excel_reports_from(self, report_type)`

Returns the urls of all the documents in the specified report_type. i.e. 10-K, 10-Q
* report_type: the type of report to retrieve


`download_file(self, url, cik)`

Download the document from the url if the cid correspond to the current company.
* url: The url of the forms that need to download
* cik: The cik number of current company.


`get_10k_year(self, year)`

Returns the url of the 10-K excel report of a given company at a specified year. 
* year: year of the report

`get_10q_year_quarter(self, year, quarter)`
Returns the url of the 10-Q excel report of a given company at a specified year and quarter. 
* year: year of the report
* year: quarter of the year

## Note
For the 4th quarter of any given year is entailed the 10-K form for that year.  Additionally, some auto generated reports may not be present thus the URL has no downloadable content.  