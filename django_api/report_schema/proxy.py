from report_schema.raw_report.utils import (
    retrieve_raw_reports_response
)
import json
import os
import re

"""
This file contains the Proxy class and the functions that it calls. This class
will be used to validate a request sent by the User from the front-end, and
will return a response with object from the backend with the help of the
functions in the utils.py file.
"""


def strip_request(request: dict) -> dict:
    """
    Removes whitespaces at the ends of each string value within a dictionary,
    as well as splits a list of comma-separated strings into a list of those
    strings without the whitespaces and commmas.

    Args:
        request: A request dictionary sent from the front-end.

    Returns:
        The same request passed in but with its values cleaned up in order to
        be used for further processing.
    """
    cleaned = {}
    for key, val in request.items():
        if isinstance(val, str):
            if key == 'years':
                split_years = val.split(',')
                cleaned[key] = [year.strip() for year in split_years]
            else:
                cleaned[key] = val.strip()
        else:
            cleaned[key] = val
    return cleaned


def is_valid_cik(cik: str) -> bool:
    """
    Checks to see whether the parameter is numeric.

    Args:
        cik: A CIK of a company.

    Returns:
        True if cik parameter is numeric; False otherwise
    """
    return cik.isnumeric()


def is_valid_years(years: list) -> bool:
    """
    Checks to see if a list of strings are numeric and length of 4.

    Args:
        years: A list of strings representing years.

    Returns:
        True if years contains well-formatted years; False otherwise.
    """
    for year in years:
        year = year.strip()
        if not year.isnumeric() or len(year) != 4:
            return False

    return True


def is_valid_report_type(report_type: str) -> bool:
    """
    Checks to see whether inputted string is equivalent to '10-K'.
    Args:
        report_type: A string corresponding to the report type requested.

    Returns:
        True if report_type is in a valid list of report types; False otherwise
    """
    report_types = ['10-K']

    return report_type in report_types


def is_valid_instructions(instructions: dict) -> bool:
    """
    Checks to see whether the items inside a dictionary are all numeric.

    Args:
        instructions: A dictionary where key is the Excel sheet name and the
            value is a list of integer strings corresponding to the rows wanted
            by the User for said Excel sheet.

    Returns:
        True if all the integers in the list are proper integers.
    """
    for sheet_name, row_items in instructions.items():
        for num in row_items:
            if not num.isnumeric():
                return False

    return True


def is_valid_file_path(file_path: str) -> bool:
    """
    Checks to see whether the file path inputted exists.

    Args:
        file_path: A path/directory to where the file should be saved to.

    Returns:
        True if such path exists; otherwise False
    """
    return os.path.exists(file_path)


def is_valid_sheet_names(sheet_names: list) -> bool:
    """
    Checks to see whether a list of strings pass an regex pattern for Excel
    sheet names.

    Args:
        sheet_names: Names of sheets to pull data from.

    Returns:
        True if all sheet names match the regex; False otherwise.
    """
    for sheet_name in sheet_names:
        match_obj = re.match(r'^\S([\-\(\)_a-zA-Z0-9 ]+)\S$', sheet_name)
        # Accepts a-z, A-Z, 0-9, hypens, paratheses, underscores, and spaces.
        # So with this regex, anything that starts with non-whitespace
        # characters, has any of the characters I specified above, and ends in
        # a non-whitespace character will pass this test. Testing can be done
        # on https://regexr.com.
        if match_obj is None:
            return False

    return True


def is_valid_file_name(file_name: str) -> bool:
    """
    Checks to see whether an inputted file name is valid.

    Args:
        file_name: Names file to save data to.

    Returns:
        True if file name matches regex; False otherwise.
    """
    match_obj = re.match(r'^([\.\-_a-zA-Z0-9]+){1}$', file_name)
    return match_obj is not None


def validate_new_report_request(request: dict) -> tuple:
    """
    Validates a request to generate a new report by validating each item in the
    request.

    Args:
        request: A dictionary containing the user inputted values with its
            corresponding keys.

    Returns:
        True, "success" if all values of request are valid; False, "reason"
        otherwise.
    """

    if not is_valid_cik(request['cik']):
        return False, "Invalid CIK"

    if not is_valid_years(request['years']):
        return False, "Invalid Years"

    if not is_valid_report_type(request['report_type']):
        return False, "Invalid Report Type"

    if not is_valid_instructions(request['report_filter']):
        return False, "Invalid Report Filter"

    return True, "success"


def validate_raw_report_request(request: dict) -> tuple:
    """
    Validates a request to generate a raw report by validating each item in the
    request.

    Args:
        request: A dictionary containing the user inputted values with its
            corresponding keys.

    Returns:
        True, "success" if all values of request are valid; False, "reason"
        otherwise.
    """
    if not is_valid_cik(request['cik']):
        return False, "Invalid CIK"

    if not is_valid_years(request['years']):
        return False, "Invalid Years"

    if not is_valid_report_type(request['report_type']):
        return False, "Invalid Report Type"

    return True, "success"


def validate_old_request(request: dict) -> tuple:
    """
    Validates a request to retrieve an old report by validating each item in
    the request.

    Args:
        request: A dictionary containing the user inputted values with its
            corresponding keys.

    Returns:
        True, "success" if all values of request are valid; False, "reason"
        otherwise.
    """

    if not is_valid_file_name(request['file_name']):
        return False, "Invalid File Name"

    return True, "success"


class Proxy:
    def __init__(self):
        pass

    def retrieve_raw_reports(self, request: dict) -> dict:
        """
        Calls validation methods on request and if the request validates,
        retrieve a response with raw reports in it.

        Args:
            request:
                {"cik": str, "years": list(str)}
        Returns:
            A tuple of a dictionary (response) that is either an error message
            or a valid reponse, along with a status code, 400 or 200
            repectively.
        """
        request = strip_request(request)
        is_valid, msg = validate_raw_report_request(request)

        if is_valid:
            return json.dumps(retrieve_raw_reports_response(request)), 200

        return json.dumps({"error": msg}), 400

    def generate_new_report(self, request: dict) -> dict:
        """
        Calls validation methods on request and if the request validates,
        retrieve a response with a generated report in it.

        Args:
            request: {
                        "cik": str,
                        "years": list(str),
                        "report_filter": str
                    }
        Returns:
            ToDo
        """
        is_valid, msg = validate_new_report_request(request)

        if is_valid:
            return json.dumps({'msg': msg}), 200
            # return self.query_engine.generate_new_report(request)

        return json.dumps({"error": msg}), 400
