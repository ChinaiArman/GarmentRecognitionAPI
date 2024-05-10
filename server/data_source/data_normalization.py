"""
Author: ``@ChinaiArman``
Version: 1.0.0

Description:
Normalizes data from different sources to a common format for further processing.

Requirements:
This script requires the installation of the pandas library.

Usage:
To execute this module, run the following command:
    ``python data_normalization.py``
"""


import pandas as pd
# import dense captioning model script
from server.dense_captioning_model import dense_captioning 


HM_COLUMN_KEY = {
    "id": "code",
    "name": "name",
    "description": "defaultArticle.color.text",
    "imageUrl": "images" 
}
ASOS_COLUMN_KEY = {
    "id": "id",
    "name": "name",
    "description": "",
    "imageUrl": "imageUrl"
}
FREE_CLOTHES = {
    "id": "id",
    "name": "productDisplayName",
    "description": "description",
    "imageUrl": "link"
}
FREE_CLOTHES_DESCRIPTION_COLUMNS = ["gender", "masterCategory", "subCategory", "articleType", "baseColour", "season", "year", "usage"]


def merge_description_columns(df: pd.DataFrame, column_list: list) -> pd.DataFrame:
    """
    Merges multiple columns into a single 'description' column.

    Args:
        df (pd.DataFrame): The input DataFrame containing the columns to be merged.
        column_list (list): A list of column names to be merged into a single 'description' column.

    Returns:
        pd.DataFrame: The DataFrame with the specified columns merged into a single 'description' column.

    Notes:
        The function concatenates the values of the specified columns into a single 'description' column and drops the original columns.

    Author: ``@ChinaiArman``
    """
    df['description'] = df[column_list].apply(lambda x: ', '.join(x.dropna().astype(str)), axis=1)
    df.drop(columns=column_list, inplace=True)
    return df.reset_index(drop=True)


def rename_columns(df: pd.DataFrame, column_key: dict) -> pd.DataFrame:
    """
    Renames the columns of a DataFrame based on a specified mapping.

    Args:
        df (pd.DataFrame): The input DataFrame to be processed.
        column_key (dict): A dictionary mapping the original column names to the new column names.

    Returns:
        pd.DataFrame: The DataFrame with the columns renamed according to the specified mapping.

    Notes:
        The function renames the columns of the DataFrame based on the mapping provided in the column_key dictionary.

    Author: ``@ChinaiArman``
    """
    for key, value in column_key.items():
        df.rename(columns={value: key}, inplace=True)
    return df.reset_index(drop=True)


def drop_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Drops columns from a DataFrame based on a specified list of column names.

    Args:
        df (pd.DataFrame): The input DataFrame to be processed.
        columns (list): A list of column names to be dropped from the DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with the specified columns dropped.

    Notes:
        The function drops the columns from the DataFrame that are not present in the specified list of columns.
    
    Author: ``@ChinaiArman``
    """
    for column in df.columns:
        if column not in columns:
            df.drop(column, axis=1, inplace=True)
    return df.reset_index(drop=True)
    

def normalize_dataframe(df: pd.DataFrame, column_key, description_column_list=None) -> pd.DataFrame:
    """
    Normalizes the columns of a DataFrame based on a specified mapping.

    Args:
        df (pd.DataFrame): The input DataFrame to be normalized.
        column_key (dict): A dictionary mapping the original column names to the new column names.
        description_column_list (list): A list of column names to be merged into a single 'description' column.

    Returns:
        pd.DataFrame: The normalized DataFrame with the columns renamed, merged, and dropped as specified.
    
    Notes:
        The function normalizes the DataFrame by renaming columns, merging specified columns into a single 'description' column,
        and dropping columns that are not present in the specified mapping.

    Author: ``@ChinaiArman``
    """
    if description_column_list:
        df = merge_description_columns(df, description_column_list)
    df = rename_columns(df, column_key)
    df = drop_columns(df, list(column_key.keys()))
    return df.reset_index(drop=True)


def merge_dataframes(df_list: list) -> pd.DataFrame:
    """
    """
    merged_df = pd.concat(df_list, axis=0, ignore_index=True)
    return merged_df


def generate_keywords(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    pass


if __name__ == "__main__":
    # Normalize data sources
    df = pd.read_csv("server/data-source/data-files/hm.csv")
    df = normalize_dataframe(df, HM_COLUMN_KEY)
    df2 = pd.read_csv("server/data-source/data-files/asos.csv")
    df2 = normalize_dataframe(df2, ASOS_COLUMN_KEY)
    df3 = pd.read_csv("server/data-source/data-files/free_clothes.csv")
    df3 = normalize_dataframe(df3, FREE_CLOTHES, description_column_list=FREE_CLOTHES_DESCRIPTION_COLUMNS)

    # Merge data sources
    merged_df = merge_dataframes([df, df2, df3])
    print(merged_df.head())
