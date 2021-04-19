from unittest import TestCase
from os.path import dirname, realpath
from middleware.query_engine import proxy


class TestValidateCIK(TestCase):
    def test_validate_cik_valid_input(self):
        response = proxy.is_valid_cik('0000010329')
        self.assertTrue(response)

    def test_validate_cik_invalid_input(self):
        response = proxy.is_valid_cik('0000010329d')
        self.assertFalse(response)


class TestValidateYears(TestCase):
    def test_validate_years_valid_input(self):
        response = proxy.is_valid_years(['2015', '2016', '2017', '2018'])
        self.assertTrue(response)

    def test_validate_years_invalid_input(self):
        response = proxy.is_valid_years(['2015', '2016', '2017', '2dkfsj018'])
        self.assertFalse(response)


class TestValidateReportType(TestCase):
    def test_validate_report_type_valid_input(self):
        response = proxy.is_valid_report_type('10-K')
        self.assertTrue(response)

    def test_validate_report_type_invalid_input(self):
        response = proxy.is_valid_report_type('dksjfd')
        self.assertFalse(response)


class TestValidateInstructions(TestCase):
    def test_validate_instructions_valid_input(self):
        instructions = {
            'sheet1': ['1', '2', '3', '4'],
            'sheet2': ['5', '6', '7', '8'],
        }
        response = proxy.is_valid_instructions(instructions)
        self.assertTrue(response)

    def test_validate_instructions_invalid_input(self):
        instructions = {
            'sheet1': ['1', '2', '3', '4'],
            'sheet2': ['5', '6', '7', 'a8'],
        }
        response = proxy.is_valid_instructions(instructions)
        self.assertFalse(response)


class TestValidateFilePath(TestCase):
    def test_validate_file_path_valid_input(self):
        file_path = dirname(realpath(__file__))
        response = proxy.is_valid_file_path(file_path)
        self.assertTrue(response)

    def test_validate_file_path_invalid_input(self):
        file_path = 'askljdlfjds'
        response = proxy.is_valid_file_path(file_path)
        self.assertFalse(response)


class TestValidateSheetNames(TestCase):
    def test_validate_sheet_names_valid_input_1(self):
        sheet_names = ['sljfjfd', '394_3', '-i383fs0()']
        response = proxy.is_valid_sheet_names(sheet_names)
        self.assertTrue(response)

    def test_validate_sheet_names_invalid_input_2(self):
        sheet_names = ['sljfjf;d']
        response = proxy.is_valid_sheet_names(sheet_names)
        self.assertFalse(response)

        sheet_names = ['s][]ljf~jfd']
        response = proxy.is_valid_sheet_names(sheet_names)
        self.assertFalse(response)


class TestValidateFileName(TestCase):
    def test_validate_file_name_valid_input(self):
        file_name = 'vn-sdsklfs9er34823_'
        response = proxy.is_valid_file_name(file_name)
        self.assertTrue(response)

    def test_validate_file_name_invalid_input(self):
        file_name = 'sdskl*f.s9e;r34823'
        response = proxy.is_valid_file_name(file_name)
        self.assertFalse(response)


class TestValidateNewRequest(TestCase):
    def test_validate_new_request_1(self):
        request = {
            'cik': '342893',
            'years': ['2015', '2016', '2017', '2018'],
            'report_type': '10-K',
            'report_filter': {
                'sheet1': ['1', '2', '3', '4'],
                'sheet2': ['5', '6', '7', '8'],
            }
        }
        response = proxy.validate_new_report_request(request)
        self.assertTrue(response)

    def test_validate_new_request_2(self):
        request = {
            'cik': '342893',
            'years': ['2015', '2016', '2017', '2018'],
            'report_type': '10-K',
            'sheet_names': ['sljfjfd', '394_3', '-i383fs0()'],
            'report_filter': {
                'sheet1': ['1', '2', '3', '4'],
                'sheet2': ['5', '6', '7', 'adfsd8'],
            }
        }
        response, msg = proxy.validate_new_report_request(request)
        self.assertFalse(response)


class TestValidateRawRequest(TestCase):
    def test_validate_raw_request_valid_input(self):
        request = {
            'cik': '342893',
            'years': ['2015', '2016', '2017', '2018'],
            'report_type': '10-K'
        }
        response, msg = proxy.validate_raw_report_request(request)
        self.assertTrue(response)

    def test_validate_raw_request_invalid_input(self):
        request = {
            'cik': '342893',
            'years': ['2015', '2016kg', '2017', '2018'],
            'report_type': '10-K'
        }
        response, msg = proxy.validate_raw_report_request(request)
        self.assertFalse(response)


class TestValidateOldRequest(TestCase):
    def test_validate_old_request_valid_input_1(self):
        request = {
            'file_name': 'myFile.json'
        }
        response = proxy.validate_old_request(request)
        self.assertTrue(response)

