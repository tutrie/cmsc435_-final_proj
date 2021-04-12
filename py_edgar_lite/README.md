# EDGAR-Lite
Edgar-Lite is a small library you can use to retrieve financial data from the SEC Edgar Website.  With Edgar-Lite API you can download excel documents for any company's 10-Q and 10-K data through a python program.

## Environment Setup
Run the following commands in your terminal to install the required dependencies for Edgar-Lite:
```bash
pip install requests
pip install lxml
pip install urllib3
```

## Usage

### Import Edgar

* Import the Edgar-Lite library into your python program:

``` python
from edgar.company import Company
```

### Create Companies

* Create a company object for any company that you are interested in retrieving data for by using the Company class with the company's name and CIK number as parameters:

``` python
company = Company("Oracle Corp", "0001341439")
```

### Retrieve Urls
* To retrieve a dictionary of urls to access company excel reports use the get_company_excel_reports_from('report_type') method with the type of the report you want. ('10-K' or '10-Q')

``` python
urls = company.get_company_excel_reports_from("10-K")
```

* To get the url of a company's report from a specific year use get_10k_year('year_number')

``` python
url = company.get_10k_year('2019')
```

* To get the url of a company's report from a specific quarter use get_10q_year_quarter('year_number','quarter_number')

``` python
url = company.get_10q_year_quarter('2019', '3')
```

### Download Excel Report
* To download a specific document url you retrieved from the methods above, use download_file(url)

``` python
url = company.get_10q_year_quarter('2019', '3')
company.download_file(url)
```

* To download all excel reports from 10-K document from the current company, use download_all_10k_reports(self)

``` python
company.download_10k_reports()
```

* To download all excel reports from 10-Q document from the current company, use download_all_10q_reports(self)

``` python
company.download_10q_reports()
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


`get_company_excel_reports_from(self, report_type, prior_to="", no_of_entries=100)`

Returns the urls of all the documents in the specified report_type. i.e. 10-K, 10-Q
* report_type: the type of report to retrieve.
* prior_to: Time prior which documents are to be retrieved. If not specified, it'll return all documents
* no_of_entries: defaults to 100. Returns the number of entries to be returned. Maximum is 100.

`get_10k_year(self, year)`

Returns the url of the 10-K excel report of a given company at a specified year. 
* year: year of the report

`get_10q_year_quarter(self, year, quarter)`

Returns the url of the 10-Q excel report of a given company at a specified year and quarter. 
* year: year of the report
* quarter: quarter of the year

`download_file(self, url)`

Download the document from the url.
* url: The url of the forms that need to download

`download_10k_reports(self, prior_to="", no_of_entries=100)`

Download all the 10k excel reports for the current company.
* prior_to: Time prior which documents are to be retrieved. If not specified, it'll return all documents
* no_of_entries: defaults to 100. Returns the number of entries to be returned. Maximum is 100.


`download_10q_reports(self, prior_to="", no_of_entries=100)`

Download all the 10q excel reports for the current company.
* prior_to: Time prior which documents are to be retrieved. If not specified, it'll return all documents
* no_of_entries: defaults to 100. Returns the number of entries to be returned. Maximum is 100.



### Note
For the 4th quarter of any given year is entailed the 10-K form for that year. Additionally, some auto generated reports may not be present thus the URL has no downloadable content.

## Examples 

* Use Edgar-Lite to get all the urls to Oracle's 10-K Excel reports:

``` python
# import Company class from edgar library
from edgar.company import Company
# create Company object for Oracle
company = Company("Oracle Corp", "0001341439")
# get all the urls of the 10K excel reports of this compnay
url_dict = company.get_company_excel_reports_from("10-K")
```

* Use Edgar-Lite to download the latest ten 10-Q report for Oracle as excel documents:

``` python
# import Company class from edgar library
from edgar.company import Company
# create Company object for Oracle
company = Company("Oracle Corp", "0001341439")
# download the 10-Q report over the past 10 years.
company.download_10q_reports(self, no_of_entries=10)
```

* Use Edgar-Lite to download a specific quarter of a year's 10-Q report for Oracle as excel documents:

``` python
#import Company class from edgar library
from edgar.company import Company
#create Company object for Oracle
company = Company("Oracle Corp", "0001341439")
# get the url for the first quarter of 2019's excel documents.
url = company.get_10q_year_quarter('2019', '1')
# download  from the url
company.download_file(url)
```


## Testing
* To be able to run the tests for the EDGAR-Lite, first cd into the folder of `py_edgar_lite` in the terminal.

* To simply run the tests, run the following command in the terminal.
```commandline
python -m unittest discover
```

* To run the tests with the option to see the coverage of the tests, run the following 
command in the terminal
```commandline
coverage run --source=edgar -m unittest discover
coverage report 
```

* After running the test, to delete all the downloaded excel reports generated by the tests from the current folder. 
(WARN: make sure you are in the correct folder)

    * First, run the following commands to see which files will be deleted and double check that they are the 
files you want to delete.
    ```commandline
    find . -name "*.xlsx" -type f
    find . -name "*.xls" -type f
    ```

    * Then, run the following commands to delete the excel reports from the current directory.
    ```commandline
    find . -name "*.xlsx" -type f -delete
    find . -name "*.xls" -type f -delete
    ```









  
