from middleware.report_generator.src.active_report import ActiveReport
from middleware.query_engine import report_runner as qry
from unittest import TestCase
from unittest.mock import patch


@patch(qry.__name__ + '.input', create=True)
class TestGenerateReportAndActiveReportFeature(TestCase):
    def test_active_report_from_json_response(self, mocked_input):
        mocked_input.side_effect = ['Bassett', '0000010329', '2016,2017']

        response_json = qry.query_raw_report_api()
        merged_report = ActiveReport(None, None)
        merged_report = ActiveReport.from_workbooks_by_years_dicts(response_json['reports'])
        expr = (merged_report.json is not None) and (merged_report.dataframes is not None)
        self.assertTrue(expr)

    def test_active_report_and_gen_instructions(self, mocked_input):
        mocked_input.side_effect = ['Bassett', '0000010329', '2016,2017', '0,1', '0', '0']
        merged_report = ActiveReport.from_workbooks_by_years_dicts(qry.query_raw_report_api()['reports'])
        instructions = qry.generate_instructions(merged_report)
        valid_output = {'Document And Entity Information': [0], 'Consolidated Balance Sheets': [0]}
        self.assertEqual(instructions, valid_output)
