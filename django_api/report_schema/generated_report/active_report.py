from report_schema import object_conversions
import pandas as pd
import numpy as np


def join_pandas_dataframes(report_dict: dict) -> dict:
    """
    :param report_dict: a dictionary of dictionaries
    :return: It breaks them all up sheet by sheet and merges the dataframes together, returns merged report
    stored as dictionary of dataframes
    """
    dataframes_dict = {}
    for json in report_dict:
        dataframes_dict[json] = object_conversions.json_dict_to_dataframes_dict(report_dict[json])
    list_of_views = []
    for df_dict in dataframes_dict.values():
        list_of_views.append(list(df_dict.items()))
    to_return = {}
    for idx in range(len(list_of_views[0])):
        to_return[list_of_views[0][idx][0]] = [list_of_views[0][idx][1]]
        for other_df in list_of_views[1:]:
            to_return[list_of_views[0][idx][0]].append(other_df[idx][1])

    for keys in to_return:
        to_return[keys] = pd.concat(
           to_return[keys], axis=1).fillna(value=0.0)
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

    def __init__(self, wbks_by_year: dict):
        """
        :param wbks_by_year: Given to us by the report_runner
        """
        self.dataframes_dict = join_pandas_dataframes(wbks_by_year)
        self.json_dict = object_conversions.dataframes_dict_to_json_dict(self.dataframes_dict)
        self.generated_report = self.dataframes_dict

    def filter_report(self, instructions: dict):
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
            self.generated_report[sheet] = self.dataframes_dict[sheet].iloc[int_rows]

    def return_json_report(self) -> dict:
        """
        :return: retruns the json dict object of the generated_report
        """
        return object_conversions.dataframes_dict_to_json_dict(self.generated_report)

    def min_max_avg(self):
        """
        :return: does min/max/avg analysis on self.generate_report object. Adds the columns to each sheet
        """
        skip_first = 0
        for frame in self.generated_report:
            if skip_first == 1:
                self.generated_report[frame] = self.generated_report[frame].applymap(
                    lambda x: x.strip() if isinstance(x, str) else x).replace(to_replace='', value=0.0)
                analysis = self.generated_report[frame].astype(np.float64).select_dtypes(np.number)\
                    .stack().groupby(level=0).agg(['min', 'max', 'mean'])
            else:
                skip_first = 1
                analysis = self.generated_report[frame].select_dtypes(np.number)\
                    .stack().groupby(level=0).agg(['min', 'max', 'mean'])
            self.generated_report[frame] = pd.concat([self.generated_report[frame], analysis], axis=1)
