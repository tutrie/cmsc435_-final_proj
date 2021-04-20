from report_generator.utils.convert_objects.object_conversions import (
    json_dict_to_json_file,
    json_dict_to_dataframes_dict,
    dataframes_dict_to_workbook
)
from os.path import realpath, dirname, exists
from re import match
import requests
import sys


base_url = "http://127.0.0.1:5000/api/"
raw_report_url = base_url + "raw-report"
generate_report_url = base_url + "generate-report"
user_report_url = base_url + "user-report"


def get_user_input(prompt: str) -> str:
    """
    Args:
        prompt: A prompt to the user.

    Returns:
        A user inputted string stripped of whitespaces at each end.
    """
    value = input(prompt)
    return value.strip()


def get_user_input_as_list(prompt: str) -> list:
    """
    Args:
        prompt: A prompt to the user.

    Returns:
        The input into a list after seperating by commas.
    """
    as_list = []

    for val in get_user_input(prompt).split(","):
        val = val.strip()

        if len(val) > 0:
            as_list.append(val)

    return as_list


def basic_request() -> dict:
    return {
        "cik": get_user_input("Enter CIK: "),
        "years": get_user_input_as_list("Enter list of years seperated by commas: "),
        "report_type": get_user_input("Enter report type"),
    }


def is_error_response(response):
    if "error" in response:
        print(response["error"])
        return True

    return False


def get_rows_for_sheets(sheets: list) -> dict:
    sheet_map = {}

    for sheet in sheets:
        print(f'Sheet Name: {sheet}\n')

        rows_to_get = get_user_input_as_list("Enter the rows you would like: ")
        sheet_map[sheet] = rows_to_get

    return sheet_map


def get_database_path() -> str:
    """Returns the path to the database."""

    if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        dir_name = dirname(realpath(__file__)).replace(
            "middleware/query_engine", "report_generator/mocks/")
        return dir_name + "mock_database/Users/"

    # To be deleted when put into Linux container
    elif sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
        dir_name = dirname(realpath(__file__)).replace(
            "middleware\\query_engine", "report_generator\\mocks\\")
        return dir_name + "mock_database\\Users\\"


def retrieve_raw_report() -> dict:
    valid_input = False
    report = {}

    while not valid_input:
        request = basic_request()
        response = requests.get(raw_report_url, json=request).json()

        if not is_error_response(response):
            report = response["report"]
            valid_input = True

    return report


"""
def retrieve_user_report() -> dict:
    valid_input = False
    report = {}

    while not valid_input:
        request = basic_request()
        request["user"] = "USERNAME"  # ToDo get username of the person using the program

        response = requests.get(user_report_url, request).json()

        if not is_error_response(response):
            report = response["report"]
            valid_input = True

    return report
"""


def generate_new_report() -> dict:
    valid_input = False
    report = {}

    while not valid_input:
        request = basic_request()
        sheets = get_user_input_as_list(
            "Enter a list of sheets you want to pull from: ")
        request["report_filter"] = get_rows_for_sheets(sheets)

        response = requests.get(generate_report_url, json=request).json()

        if not is_error_response(response):
            report = response["report"]
            valid_input = True

    return report


def get_user_folder_path() -> str:
    valid_input = False
    output_folder = ""

    while not valid_input:
        output_folder = get_user_input("""Please enter a folder path to save
                            your files in: (<directory>/<sub_directory>/): """)

        # ToDo
        # if not isdir(output_folder):
        #    print(f'{output_folder} is not an existing folder path. Please try again.')
        # else:
        #    valid_input = True

        valid_input = len(output_folder) > 0

    if output_folder[-1] == '/':
        return output_folder

    return output_folder + '/'


def choose_json_or_xlsx() -> str:
    """
    Args:
        None

    Returns:
        'json' or 'xlsx', whatever the user chooses.
    """
    while True:
        prompt = 'Please specify the output file type (json/xlsx): '
        output_type = get_user_input(prompt)

        valid_inputs = ['json', 'xlsx']

        if output_type in valid_inputs:
            return f'.{output_type}'
        else:
            print(f'Invalid file type ({output_type})!')


def get_valid_file_name() -> str:
    """
    Args:
        None

    Returns:
        A valid file name.
    """
    while True:
        file_name = input('''Please enter a file name (no extension) for
            your report: ''')

        file_name = file_name.strip()

        # name can only have a-z, A-Z, 0-9, underscores ("_"), and hypens ("-")
        match_obj = match(r'^([\-_a-zA-Z0-9]+){1}$', file_name)

        if match_obj:
            return match_obj[0]
        else:
            print('''Invalid Input! Allowed characters are a-z, A-Z, 0-9,
                underscores ("_"), and hypens ("-").''')


def can_save_to_location(file_path: str) -> bool:
    """
    Args:
        file_path: A valid file path of the User's choice to the possibly
            existing file.

    Returns:
        True if User is allowed/allows the file to be saved to the specified
        file path; False otherwise.
    """
    if exists(file_path):
        prompt = f'''The file {file_path} already exists. Do
            you want to overwrite this file (y/n)? (This operation
            cannot be undone!): '''
        answer = get_user_input(prompt)
        return answer == 'y'

    return True


def save_json(report_dict: dict, output_file: str):
    json_dict_to_json_file(report_dict, output_file)


def save_xlsx(report_dict: dict, output_file: str):
    dataframes_dict = json_dict_to_dataframes_dict(report_dict)
    dataframes_dict_to_workbook(dataframes_dict, output_file)


def save_report_locally(report: dict) -> str:
    """
        Saves report to a local folder and returns the file location
        #ToDo prompt user if they want to overwrite or not
    """
    save_as = {".json": save_json, ".xlsx": save_xlsx}
    directory = get_database_path()
    output_folder = get_user_folder_path()
    file_name = get_valid_file_name()
    file_extension = choose_json_or_xlsx()

    output_file = "{}{}{}{}".format(directory, output_folder,
                                    file_name, file_extension)

    save_as[file_extension](report, output_file)

    return output_file


def start_report_retrieval():
    """
    This function simply queries the user and ask them to choose one of three
    options:
        1. Retrieve a Raw Report
        2. Retrieve a User Generated Report
        3. Generate a new Report
    """
    welcome_string = '''Welcome! We will now ask you to input some information
        in order to generate your custom report. Enter 'back' at any time to
        return to a previous step in the current report retrieval cycle.\n
    '''

    print(welcome_string)

    # ToDo add functionality for getting user_report
    function_map = {"1": retrieve_raw_report, "2": generate_new_report}

    while True:
        query_user_string = '''
        Please choose one of the following options with its corresponding
        number:
            1. Retrieve a Raw Report
            2. Generate a new Report
            To exit enter "done"
        '''
        option = get_user_input(query_user_string)

        if option == "done":
            break

        if option in function_map:
            report = function_map[option]()
            file_location = save_report_locally(report)
            print("You can find your report at " + file_location)
        else:
            print("Invalid response")


if __name__ == "__main__":
    start_report_retrieval()
    print('Bye!\n')
