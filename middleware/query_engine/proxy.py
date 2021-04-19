from middleware.query_engine.query_engine import QueryEngine
import os
import re


def is_valid_cik(cik: str) -> bool:
    """
    Args:
        cik: A CIK of a company.

    Returns:
        True if cik paremeter is numeric; False otherwise
    """
    return cik.isnumeric()


def is_valid_years(years: list) -> bool:
    """
    Args:
        years: A list of interger strings reprenting years.

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
    Args:
        report_type: A string corresponding to the report type requested.

    Returns:
        True if report_type is in a valid list of report types; False otherwise
    """
    report_types = ['10-K']

    return report_type in report_types


def is_valid_instructions(instructions: dict) -> bool:
    """
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
    Args:
        file_path: A path/directory to where the file should be saved to.

    Returns:
        True if such path exists; otherwise False
    """
    return os.path.exists(file_path)


def is_valid_sheet_names(sheet_names: list) -> bool:
    """
    Args:
        sheet_names: Names of sheets to pull data from.

    Returns:
        True if all sheet names match the regex; False otherwise.
    """
    for sheet_name in sheet_names:
        match_obj = re.match(r'^\S([\-\(\)_a-zA-Z0-9 ]+)\S$', sheet_name)  # could you explain what would pass/fail?
        if match_obj is None:
            return False

    return True


def is_valid_file_name(file_name: str) -> bool:
    """
    Args:
        file_name: Names file to save data to.

    Returns:
        True if file name matches regex; False otherwise.
    """
    match_obj = re.match(r'^([\.\-_a-zA-Z0-9]+){1}$', file_name)
    return match_obj is not None


def validate_new_report_request(request: dict) -> tuple:
    """
    Args:
        request: A dictionary containing the user inputted values with its
            corresponding keys.

    Returns:
        True, "success" if all values of request are valid; False, "reason" otherwise.
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
    Args:
        request: A dictionary containing the user inputted values with its
            corresponding keys.

    Returns:
        True, "success" if all values of request are valid; False, "reason" otherwise.
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
    Args:
        request: A dictionary containing the user inputted values with its
            corresponding keys.

    Returns:
        True, "success" if all values of request are valid; False, "reason" otherwise.
    """

    if not is_valid_file_name(request['file_name']):
        return False, "Invalid File Name"

    return True, "success"


class Proxy:
    def __init__(self):
        self.query_engine = QueryEngine()

    def retrieve_raw_reports(self, request: dict) -> dict:
        """

        Args:
            request:
                {"cik": str, "years": list(str), "report_type": str}
        Returns:

        """
        is_valid, msg = validate_raw_report_request(request)

        if is_valid:
            return self.query_engine.retrieve_raw_reports(request)

        return {"error": msg}

    def generate_new_report(self, request: dict) -> dict:
        """

        Args:
            request:
                {"cik": str, "years": list(str), "report_type": str, "report_filter": str}
        Returns:

        """
        is_valid, msg = validate_new_report_request(request)

        if is_valid:
            return self.query_engine.generate_new_report(request)

        return {"error": msg}
