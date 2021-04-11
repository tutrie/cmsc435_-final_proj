# EDGAR-Lite
Edgar-Lite is a small library you can use to retrieve financial data from the SEC Edgar Website.  With Edgar-Lite API you can download excel documents for any company's 10-Q and 10-K data through a python program.

## Environment Setup
Run the following commands in your terminal to install the required dependencies for Edgar-Lite:
```bash
pip install requests
pip install lxml
```
## API

### Methods

`Company(name="", cik="", timeout="")`

Returns a company object that you use to retrieve filings
* name (company name)
* cik (company CIK number)
* timeout (optional) (default: 10)


`get_filings_url(self, filing_type="", prior_to="", ownership="include", no_of_entries=100) -> str`

Returns a url to fetch filings data and saves that url in the database to access reports from later
* filing_type: The type of document you want. i.e. 10-K, 10-Q. If not specified, it'll return all documents
* prior_to: Time prior which documents are to be retrieved. If not specified, it'll return all documents
* ownership: defaults to include. Options are include, exclude, only.
* no_of_entries: defaults to 100. Returns the number of entries to be returned. Maximum is 100.


`get_company_excel_reports_from(self, report_type)`

Returns the urls of all the documents in the specified report_type. i.e. 10-K, 10-Q
* report_type: the type of report to retrieve


`download_file(self, url)`

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

### Usage

#### Import Edgar

Import the Edgar-Lite library into your python program:

``` python
from edgar.company import Company
```

#### Create Companies

Create a company object for any company that you are interested in retrieving data for by using the Company class with the company's name and CIK number as parameters:

``` python
company = Company("Oracle Corp", "0001341439")
```

#### Retrieve Urls
To retrieve a dictionary of urls to access company excel reports use the get_company_excel_reports_from() method with the type of the report you want. ('10-K' or '10-Q')

``` python
urls = company.get_company_excel_reports_from("10-K")
```

To get the url of a company's report from a specific quarter use get_10q_year_quarter('year_number','quarter_number') or get_10q_year_quarter('year_number','quarter_number')

``` python
url = company.get_10q_year_quarter('2019', '3')
```

#### Note
For the 4th quarter of any given year is entailed the 10-K form for that year. Additionally, some auto generated reports may not be present thus the URL has no downloadable content.

## Examples 

Use Edgar-Lite to get 10-K report for Oracle over the past 10 years as excel documents:

``` python
#import Company class from edgar library
from edgar.company import Company
#create Company object for Oracle
company = Company("Oracle Corp", "0001341439")
#get urls of past 10 years of 10-K filings in the database from company
urls = company.get_company_excel_reports_from(report_type='10-K', no_of_entries=10)
# download excel documents from the urls
for url in urls:
    company.download_file(url[0])
```

Use Edgar-Lite to get a specific quarter of a year's 10-Q report for Oracle as excel documents:

``` python
#import Company class from edgar library
from edgar.company import Company
#create Company object for Oracle
company = Company("Oracle Corp", "0001341439")
#save url for page of 10-Q filings in the database
company.get_filings_url('10-Q')
# get urls from page
urls = company.get_company_excel_reports_from('10-Q')
# download first quarter of 2019's excel documents from the url
company.download_file(urls['2019']['1'])
```


## Testing
Running every test cases at once will cause some tests fail randomly, which is due to the fact that the tests were run 
concurrently. It will be more consistent to run each one by one. 








  
