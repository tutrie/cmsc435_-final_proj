import json


def dataframes_dict_to_json_dict(dataframes_dict: dict) -> dict:
    """
    Turns a dictionary of dataframes into a dictionary of dictionary
    represntations of those dataframes.

    Args:
        dataframes_dict: Dictionary of Pandas dataframes where key is the sheet
            name of the dataframe while the value is the inner dictionary
            corresponding to the dataframe itself.

    Returns:
        Dictionary of dictionaries where key is the sheet name of the dataframe
        while the value is the dictionary representation of the dataframe.
    """
    json_dict = {}
    for sheet_name, df in dataframes_dict.items():
        json_dict[sheet_name] = dataframe_to_dict(df)

    return json_dict


def dataframe_to_dict(dataframe: object) -> dict:
    """
    Turns a dataframe into its dictionary representation.

    Args:
        dataframe: A pandas dataframe

    Returns:
        Dictionary representation of pandas dataframe
    """
    return json.loads(dataframe.to_json(force_ascii=False))
