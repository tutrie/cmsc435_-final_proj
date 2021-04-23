import sys
sys.path.insert(0, sys.path[0].replace('/middleware/query_engine', ''))
print(sys.path)
from middleware.report_generator.utils.convert_objects.object_conversions import (
    json_dict_to_json_file,
    json_dict_to_dataframes_dict,
    dataframes_dict_to_workbook
)
from middleware.report_generator.src.active_report import ActiveReport
from os.path import exists, isdir
from re import match
import requests

# # For production:
# base_url = 'http://18.217.8.244:8000/api/'

# For developement:
base_url = 'http://127.0.0.1:8000/api/'
raw_report_url = base_url + 'raw-reports/get-raw-reports'
generate_report_url = base_url + 'generate-report'
user_report_url = base_url + 'user-report'


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

    for val in get_user_input(prompt).split(','):
        val = val.strip()

        if len(val) > 0:
            as_list.append(val)

    return as_list


def get_user_int_list(target_list: list) -> list:
    """
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

            elif int(num) < 0 or int(num) > len(target_list):
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


def save_json(report_dict: dict, output_file: str):
    json_dict_to_json_file(report_dict, output_file)


def save_xlsx(report_dict: dict, output_file: str):
    dataframes_dict = json_dict_to_dataframes_dict(report_dict)
    dataframes_dict_to_workbook(dataframes_dict, output_file)


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
                underscores ('_'), and hypens ('-').''')


def get_user_folder_path() -> str:
    valid_input = False
    output_folder = ''

    while not valid_input:
        output_folder = get_user_input("""Please enter a folder path to save
                            your files in: (<directory>/<sub_directory>/): """)

        if not isdir(output_folder):
            print(
                f'{output_folder} is not an existing folder path. Please try again.')
        else:
            valid_input = True

    if output_folder[-1] == '/':
        return output_folder

    return output_folder + '/'


def save_single_report(report_dict: dict) -> None:
    save_as = {'.json': save_json, '.xlsx': save_xlsx}

    while True:
        output_folder = get_user_folder_path()
        file_name = get_valid_file_name()
        file_extension = choose_json_or_xlsx()

        output_file = '{}{}{}'.format(output_folder, file_name, file_extension)

        if can_save_to_location(output_file):
            save_as[file_extension](report_dict, output_file)

    print(f'Successfully saved file at {output_file}.')


def save_multiple_reports_locally(report: dict) -> None:
    """
        Saves report to a local folder and returns the file location
        #ToDo prompt user if they want to overwrite or not
    """
    for year, report_dict in report.items():
        print(f'For the report created in the year {year}:\n')
        save_single_report(report)


def is_error_response(response):
    return response.status_code != 200


def basic_request() -> dict:
    return {
        'company': get_user_input('Enter a company name: '),
        'cik': get_user_input('Enter CIK for the company: '),
        'years': get_user_input_as_list('Enter list of years seperated by commas: '),
    }


def retrieve_raw_report() -> None:
    while True:
        request = basic_request()
        response = requests.get(raw_report_url, params=request)
        print(f'Response: {response}\n')
        print(f'Dir: {dir(response)}\n')
        print(f'url: {response.url}\n')
        print(f'test: {response.text}\n')
        print(f'Json: {response.json()}\n')
        print(f'Status_code: {response.status_code}\n')
        if is_error_response(response):
            print(f'Response returned with error code {response.status_code}')
            print(f'Response error: {response.json()["error"]}')
        else:
            save_multiple_reports_locally(response.json()['reports'])


def choose_rows_in_sheet(sheet_name, sheet_values: dict) -> list:
    print(f'Preparing to choose rows for sheet {sheet_name}')
    rows_idxs_to_keep = get_user_int_list(sheet_values['index'])
    return rows_idxs_to_keep


def choose_sheet_names(merged_report: ActiveReport) -> list:
    sheet_names = list(merged_report.json.keys())
    print('Preparing to choose sheets to pull from:\n')
    sheet_idxs_to_keep = get_user_int_list(sheet_names)
    return [sheet_names[idx] for idx in sheet_idxs_to_keep]


def generate_instructions(merged_report: ActiveReport) -> dict:
    instructions = {}

    sheets_to_keep = choose_sheet_names(merged_report)

    for sheet in sheets_to_keep:
        instructions[sheet] = choose_rows_in_sheet(sheet, merged_report[sheet])

    return instructions


def create_generated_report(username: str, password: str) -> None:
    reports = retrieve_raw_report()
    merged_report = ActiveReport.from_workbooks_by_years_dicts(
        reports['reports'])

    instructions = generate_instructions(merged_report)
    generated_report_json = merged_report.filter_report(instructions)

    print('Preparing to save generated report locally:\n')
    save_single_report(generated_report_json)
    response = requests.post(generate_report_url, auth=(username, password),
                             data=generated_report_json, timeout=15)
    if response.status_code == 201:
        print('Generated report successfully saved to database.')
    else:
        print(f'Response returned with error code {response.status_code}')
        print(f'Full response: {response}')


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
    function_map = {'1': retrieve_raw_report, '2': create_generated_report}

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
