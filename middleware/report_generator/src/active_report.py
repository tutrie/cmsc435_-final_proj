from middleware.report_generator.utils.convert_objects.object_conversions import (
    json_dict_to_dataframes_dict,
    dataframes_dict_to_json_dict
)
from functools import reduce
from os.path import join, dirname, realpath
import pandas as pd


def join_pandas_dataframes(report_dict: dict) -> dict:
    dataframes_dict = {}
    for json in report_dict:
        dataframes_dict[json] = json_dict_to_dataframes_dict(report_dict[json])
    list_of_views = []
    for df_dict in dataframes_dict.values():
        list_of_views.append(list(df_dict.items()))
    to_return = {}
    for idx in range(len(list_of_views[0])):
        to_return[list_of_views[0][idx][0]] = [list_of_views[0][idx][1]]
        for other_df in list_of_views[1:]:
            to_return[list_of_views[0][idx][0]].append(other_df[idx][1])

    for keys in to_return:
        #print(to_return[keys])
        #to_return[keys] = reduce(lambda x, y: x.join(y, how='outer', on=x.columns.tolist().append(y.columns.tolist()), rsuffix='_dp'), to_return[keys])
        to_return[keys] = pd.concat(
           to_return[keys], axis=1)
        to_return[keys].columns = to_return[keys].columns.astype(str)

    return to_return


class ActiveReport:
    """
    A class representing the current report being requested the User.

    Fields:
        self.json: The dictionary equivalent of the JSON file the report
            corresponds to.

        self.dataframes: A dictionary of Pandas dataframes where key is the
            sheet name of the dataframe while the value is the inner dictionary
            corresponding to the dataframe itself.

        self.generated_report: A dictionary of Pandas dataframes where key is
            the sheet name of the dataframe while the value is the inner
            dictionary corresponding to the dataframe itself. This will only be
            created when ActiveReport object is filtered to generate a report
            based on the inputs of the User.
    """

    def __init__(self, json_dict: dict, dataframes_dict: dict):
        self.json = json_dict
        self.dataframes = dataframes_dict

    # @classmethod
    # def from_year(cls, cik: str, year: str, report_type: str):
    #     """
    #     Args:
    #         cik: CIK number of target company.

    #         year: Year to pull financial files from.

    #         report_type: Report type to pull information from (10-K or 10-Q).

    #     Returns:
    #         An ActiveReport object
    #     """
    #     # TODO: this file path thing may need updating. Quick solution
    #     dir_path = dirname(realpath(__file__)).replace("src", "mocks")
    #     file_name = f'{report_type}-{year[-2:]}.json'
    #     json_file_path = join(dir_path, 'mock_database', cik,
    #                           year, report_type, file_name)

    #     json_dict = json_file_to_json_dict(json_file_path)
    #     dataframes_dict = json_dict_to_dataframes_dict(json_dict)

    #     return cls(json_dict, dataframes_dict)

    # @classmethod
    # def from_year_list(cls, cik: str, years: list, report_type: str):
    #     """
    #     Args:
    #         cik: CIK number of target company.

    #         years: List of years (of type string) to pull financial files from.

    #         report_type: Report type to pull information from (10-K or 10-Q).

    #     Returns:
    #         An ActiveReport object of the collated/merged reports across years.
    #     """
    #     dir_path = dirname(realpath(__file__)).replace("src", "mocks")

    #     report_dicts = {}
    #     for year in years:
    #         file_name = f'{report_type}-{year[-2:]}.json'
    #         json_file_path = join(dir_path, 'mock_database', cik,
    #                               year, report_type, file_name)

    #         report_dicts[file_name] = json_file_to_json_dict(json_file_path)

    #     # DUMMY FUNCTION HERE!!! Don't forget to import the function first!
    #     dataframes_dict = join_pandas_dataframes(report_dicts)
    #     json_dict = dataframes_dict_to_json_dict(dataframes_dict)

    #     return cls(json_dict, dataframes_dict)

    @classmethod
    def from_workbooks_by_years_dicts(cls, wbks_by_year: dict) -> object:
        dataframes_dict = join_pandas_dataframes(wbks_by_year)
        json_dict = dataframes_dict_to_json_dict(dataframes_dict)
        return cls(json_dict, dataframes_dict)

    def filter_report(self, instructions: dict) -> dict:
        """
        Args:
            instructions: A dictionary of integer lists when the keys are the
                sheet names to pull data from while the values are rows from
                said sheets to retrieve the data from.

        Sets:
            self.generated_report

        Returns:
            self.generated_report
        """
        self.generated_report = {}
        for sheet, rows in instructions.items():
            int_rows = [int(val) for val in rows]
            # rows is list of ints
            self.generated_report[sheet] = self.dataframes[sheet].iloc[int_rows]

        return dataframes_dict_to_json_dict(self.generated_report)
