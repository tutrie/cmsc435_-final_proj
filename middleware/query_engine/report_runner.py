import sys
sys.path.insert(0, sys.path[0].replace(r'\middleware\query_engine', ''))
print(sys.path)
import json
import requests
from re import match
from os.path import exists, isdir
from middleware.report_generator.src.active_report import ActiveReport
from middleware.report_generator.utils.convert_objects.object_conversions import (
    json_dict_to_dataframes_dict,
    dataframes_dict_to_workbook
)


# # For production:
# base_url = 'http://18.217.8.244:8000/api/'

# For developement:
base_url = 'http://localhost:8000/api/'
raw_report_url = base_url + 'raw-reports/get-raw-reports'
generate_report_url = base_url + 'generate-report'
user_report_url = base_url + 'user-report'


def get_user_input(prompt: str) -> str:
    """
    Prompts a user for input.

    Args:
        prompt: A prompt to the user.

    Returns:
        A user inputted string stripped of whitespaces at each end.
    """
    value = input(prompt)
    return value.strip()


def get_user_input_as_list(prompt: str) -> list:
    """
    Promps user for a list of inputs.

    Args:
        prompt: A prompt to the user.

    Returns:
        The input into a list after seperating by commas.
    """
    as_list = []

    for val in get_user_input(prompt).split(','):
        val = val.strip()

        if len(val) > 0:
            as_list.append(val)

    return as_list


def get_user_int_list(target_list: list) -> list:
    """
    Prompts user for a list of integers.

    Args:
        target_list: A list corresponding to items that the User may want to
            pull information from.

    Returns:
        list: A list corresponding to the indices of items within target_list
            that the User wants to pull information from.
    """

    while True:
        for idx, target in enumerate(target_list):
            print(f'{idx}: {target}')

        print('''Please enter a comma-separated list (e.g. \'1, 2, 3, ...\')
            corresponding to the items you wish to pull from.\n''')

        item_list = get_user_input('Your Targets: ')

        item_list = item_list.split(',')

        to_keep = []    # rows of current report the user wants to see
        should_break = True

        for num in item_list:
            num = num.strip()

            if not num.isnumeric():
                print(f'''You entered a non-numeric value (\'{num}\').
                        Please only enter numbers between
                        0-{len(target_list)-1}'''
                      )

                should_break = False
                break

            elif int(num) < 0 or int(num) >= len(target_list):
                print(f'''You entered a numeric value (\'{num}\') that is out
                        of range. Please only enter numbers between
                        0-{len(target_list)-1}'''
                      )

                should_break = False
                break

            elif int(num) in to_keep:
                print(f'Duplicate target found: {num} - Skipping\n')

            else:
                to_keep.append(int(num))

        if should_break:
            break

    return sorted(to_keep)


def save_json(report_dict: dict, output_file: str) -> None:
    """
    Saves a dictionary as a JSON file to the given output file path.

    Args:
        report_dict: A dictionary represntation of a report.

        output_file: A full file path to where the report should be saved to.
    """
    json_dict_to_json_file(report_dict, output_file)


def save_xlsx(report_dict: dict, output_file: str):
    """
    Saves a dictionary as an Excel file to the given output file path.

    Args:
        report_dict: A dictionary represntation of a report.

        output_file: A full file path to where the report should be saved to.
    """
    dataframes_dict = json_dict_to_dataframes_dict(report_dict)
    dataframes_dict_to_workbook(dataframes_dict, output_file)


def can_save_to_location(file_path: str) -> bool:
    """
    Checks to see whether a given file path exists already and if so, prompts
    the user and asks whether it is okay to overwrite a existing file.

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


def choose_json_or_xlsx() -> str:
    """
    Promps the user to choose to save a file in either as a json or xlsx file
    format.

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
            print(f'\nInvalid file type ({output_type})!\n')


def get_valid_file_name() -> str:
    """
    Prompts the user for a valid file name.

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
            print('''\nInvalid Input! Allowed characters are a-z, A-Z, 0-9,
                underscores ('_'), and hypens ('-').\n''')


def get_user_folder_path() -> str:
    """
    Prompts the user for a valid folder path.

    Returns:
        A valid folder path.
    """
    valid_input = False
    output_folder = ''

    while not valid_input:
        output_folder = input('''Please enter a folder path to save
                            your files in: (<directory>/<sub_directory>/): ''')

        if not isdir(output_folder):
            print(
                f'\n{output_folder} is not an existing folder path. Please try again.\n')
        else:
            valid_input = True

    if output_folder[-1] == '/':
        return output_folder

    return output_folder + '/'


def save_single_report(report_dict: dict) -> None:
    """
    Call functions to save a single report.

    Args:
        report_dict: A dictionary represntation of a report.
    """
    save_as = {'.json': save_json, '.xlsx': save_xlsx}
    output_folder = get_user_folder_path()
    while True:
        file_name = get_valid_file_name()
        file_extension = choose_json_or_xlsx()

        output_file = '{}{}{}'.format(output_folder, file_name, file_extension)

        if can_save_to_location(output_file):
            save_as[file_extension](report_dict, output_file)
            break

    print(f'\nSuccessfully saved file at {output_file}.\n')


def save_multiple_reports_locally(report: dict) -> None:
    """
    Saves report to a local folder and returns the file location
    
    Args:
        report_dict: A dictionary represntation of a report.
    """
    for year, report_dict in report.items():
        print(f'\nFor the report created in the year {year}:\n')
        save_single_report(report_dict)


def is_error_response(response: object) -> bool:
    """
    Tests whether a response object returned a 200 OK status.

    Returns:
        True if response.status_code != 200; False otherwise.
    """
    return response.status_code != 200


def basic_request() -> dict:
    """
    Call functions to prompt user for basic report information.

    Returns:
        A request to be sent to the back-end to retrieve reports.
    """
    return {
        'company': get_user_input('Enter a company name: '),
        'cik': get_user_input('Enter CIK for the company: '),
        'years': get_user_input_as_list('Enter list of years seperated by commas: '),
    }


def query_raw_report_api() -> None:
    """
    Uses the request library to send a request to the API and receive a
    response from the API to process further.
    """
    while True:
        request = basic_request()
        response = requests.get(raw_report_url, params=request)
        response_json = json.loads(response.json())
        print(f'Response: {response}\n')
        print(f'Json: {response_json.keys()}')

        if is_error_response(response):
            print(f'Response returned with error code {response.status_code}')
            print(f'Response error: {response_json["error"]}')
            return None
        else:
            return response_json


def retrieve_raw_reports() -> None:
    """
    Get the json object of the response, and if the request was successful,
    save the reports to the local machine.
    """
    response_json = query_raw_report_api()
    if response_json:
        save_multiple_reports_locally(response_json['reports'])


def choose_rows_in_sheet(sheet_name: str, sheet_values: dict) -> list:
    """
    Prompts user to choose specific rows in Excel sheets.

    Returns:
        A list of indices corresponding to the selected rows.
    """
    print(f'Preparing to choose rows for sheet {sheet_name}')
    rows_idxs_to_keep = get_user_int_list(sheet_values.index)
    return rows_idxs_to_keep


def choose_sheet_names(merged_report: ActiveReport) -> list:
    """
    Prompts user to choose specific sheets from a workbook.

    Returns:
        A list of indices corresponding to the selected sheets.
    """
    sheet_names = list(merged_report.json.keys())
    print('Preparing to choose sheets to pull from:\n')
    sheet_idxs_to_keep = get_user_int_list(sheet_names)
    return [sheet_names[idx] for idx in sheet_idxs_to_keep]


def generate_instructions(merged_report: ActiveReport) -> dict:
    """
    Generate instructions to filter report.

    Returns:
        Instructions dictionary with key being a sheet name and the values
        being rows for that sheet to keep.
    """
    instructions = {}

    sheets_to_keep = choose_sheet_names(merged_report)

    for sheet in sheets_to_keep:
        instructions[sheet] = choose_rows_in_sheet(sheet, merged_report.dataframes[sheet])

    return instructions


def create_generated_report(username: str = None, password: str = None) -> None:
    """
    Creates a generated report for the user, per user input.
    """
    response_json = query_raw_report_api()
    if not response_json:
        return
    merged_report = ActiveReport.from_workbooks_by_years_dicts(response_json['reports'])
    instructions = generate_instructions(merged_report)
    generated_report_json = merged_report.filter_report(instructions)

    print('Preparing to save generated report locally:\n')
    save_single_report(generated_report_json)

    # response = requests.post(generate_report_url, auth=(username, password),
    #                          data=generated_report_json, timeout=15)
    # if response.status_code == 201:
    #     print('Generated report successfully saved to database.')
    # else:
    #     print(f'Response returned with error code {response.status_code}')
    #     print(f'Full response: {response}')


def start_report_retrieval() -> None:
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
    function_map = {'1': retrieve_raw_reports, '2': create_generated_report}

    while True:
        query_user_string = '''
        Please choose one of the following options with its corresponding
        number:
            1. Retrieve a Raw Report
            2. Generate a new Report
            To exit enter 'done'
        '''
        option = get_user_input(query_user_string)

        if option == 'done':
            break

        if option in function_map:
            function_map[option]()
        else:
            print('Invalid response')


if __name__ == '__main__':
    start_report_retrieval()
    print('Bye!\n')
