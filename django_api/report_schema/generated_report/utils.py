import json

import pandas as pd
import numpy as np


def min_max_avg(generated_report: dict) -> dict:
    """
    :return: does min/max/avg analysis on self.generate_report object. Adds the columns to each sheet
    """
    skip_first = 0

    generated_report = json_dict_to_dataframes_dict(generated_report)

    for frame in generated_report:
        if skip_first == 1:
            generated_report[frame] = generated_report[
                frame].applymap(
                lambda x: x.strip() if isinstance(x, str) else x).replace(
                to_replace='', value=0.0)
            analysis = generated_report[frame].astype(
                np.float64).select_dtypes(np.number) \
                .stack().groupby(level=0).agg(['min', 'max', 'mean'])
        else:
            skip_first = 1
            analysis = generated_report[frame].select_dtypes(np.number) \
                .stack().groupby(level=0).agg(['min', 'max', 'mean'])

        generated_report[frame] = pd.concat(
            [generated_report[frame], analysis], axis=1)

    return generated_report


def json_dict_to_dataframes_dict(json_dict: dict) -> dict:
    """
    Args:
        json_dict: Dictionary of dictionaries that represents the JSON.

    Returns:
        Dictionary of Pandas dataframes where key is the sheet name of the
        dataframe while the value is the dataframe itself.
    """
    dataframes = {}
    if not isinstance(json_dict, dict):
        json_dict = json.loads(json_dict)
    for sheet_name, json_df_dict in json_dict.items():
        dataframes[sheet_name] = dict_to_dataframe(json_df_dict)

    return dataframes


def dict_to_dataframe(json_dict: dict) -> object:
    """
    Args:
        json_dict: A dictionary representation of Pandas dataframe

    Returns:
        Pandas dataframe construced from dictionary.
    """
    return pd.read_json(json.dumps(json_dict, ensure_ascii=False))
