"""
Author: ``@ChinaiArman``
Version: ``1.0.0``

Description:
Normalizes data from different sources to a common format and writes to a CSV file.

Requirements:
This script requires the installation of the pandas library.

Usage:
To execute this module, run the following command:
    ``python server/data_source/data_normalization.py``
"""

import pandas as pd

from dotenv import load_dotenv
import os
import sys

load_dotenv()
sys.path.insert(0, os.getenv("PYTHONPATH"))

from dense_captioning_model import dense_captioning as dc


HM_COLUMN_KEY = {
    "id": "code",
    "name": "name",
    "description": "defaultArticle.color.text",
    "imageUrl": "images",
}
ASOS_COLUMN_KEY = {
    "id": "id",
    "name": "name",
    "description": "",
    "imageUrl": "imageUrl",
}
FREE_CLOTHES = {
    "id": "id",
    "name": "productDisplayName",
    "description": "description",
    "imageUrl": "link",
}
FREE_CLOTHES_DESCRIPTION_COLUMNS = [
    "gender",
    "masterCategory",
    "subCategory",
    "articleType",
    "baseColour",
    "season",
    "year",
    "usage",
]


def merge_description_columns(df: pd.DataFrame, column_list: list) -> pd.DataFrame:
    """
    Merges multiple columns into a single 'description' column.

    Args:
    -----
    df : ``pd.DataFrame``
        The input DataFrame containing the columns to be merged.
    column_list : ``list``
        A list of column names to be merged into a single 'description' column.

    Returns:
    --------
    ``pd.DataFrame``
        The DataFrame with the specified columns merged into a single 'description' column.

    Notes:
    ------
    1. The function concatenates the values of the specified columns into a single 'description' column and drops the original columns.

    Example:
    --------
    >>> df = pd.read_csv("data.csv")
    >>> print(df.head())
    ...        random   |  column    |   names   |   to    |   be    |   normalized
    ...        1        |    abc     |   xyz     |   def   |   gef   |   url1
    >>> df = merge_description_columns(df, ["column", "names", "to", "be"])
    >>> print(df.head())
    ...        random  |   normalized   |  column
    ...        1       |  xyz, def, gef |  abc

    Author: ``@ChinaiArman``
    """
    df["description"] = df[column_list].apply(
        lambda x: ", ".join(x.dropna().astype(str)), axis=1
    )
    df.drop(columns=column_list, inplace=True)
    return df.reset_index(drop=True)


def rename_columns(df: pd.DataFrame, column_key: dict) -> pd.DataFrame:
    """
    Renames the columns of a DataFrame based on a specified mapping.

    Args:
    -----
    df : ``pd.DataFrame``
        The input DataFrame to be processed.
    column_key : ``dict``
        A dictionary mapping the original column names to the new column names.

    Returns:
    --------
    ``pd.DataFrame``
        The DataFrame with the columns renamed according to the specified mapping.

    Notes:
    ------
    1. The function renames the columns of the DataFrame based on the mapping provided in the column_key dictionary.

    Example:
    --------
    >>> df = pd.read_csv("data.csv")
    >>> print(df.head())
    ...        random  |  column    |   names   |   to    |   be    |   normalized
    ...        1       |    abc     |   xyz     |   def   |   gef   |   url1
    >>> df = rename_columns(df, {"id": "random", "name": "column"})
    >>> print(df.head())
    ...        id  |  name    |  names   |  to     |  be     |  normalized
    ...        1   |  abc     |  xyz     |  def    |  gef    |  url1

    Author: ``@ChinaiArman``
    """
    for key, value in column_key.items():
        df.rename(columns={value: key}, inplace=True)
    return df.reset_index(drop=True)


def drop_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Drops columns from a DataFrame based on a specified list of column names.

    Args:
    -----
    df : ``pd.DataFrame``
        The input DataFrame to be processed.
    columns : ``list``
        A list of column names to be dropped from the DataFrame.

    Returns:
    --------
    ``pd.DataFrame``
        The DataFrame with the specified columns dropped.

    Notes:
    ------
    1. The function drops the columns from the DataFrame that are not present in the specified list of columns.

    Example:
    --------
    >>> df = pd.read_csv("data.csv")
    >>> print(df.head())
    ...        random    |  column    |   names   |   to    |   be    |   normalized
    ...        1         |    abc     |   xyz     |   def   |   gef   |   url1
    >>> df = drop_columns(df, ["random", "names"])
    >>> print(df.head())
    ...        column    |   to    |   be   |   normalized
    ...        abc       |   def   |   gef  |   url1

    Author: ``@ChinaiArman``
    """
    for column in df.columns:
        if column not in columns:
            df.drop(column, axis=1, inplace=True)
    return df.reset_index(drop=True)


def normalize_dataframe(
    df: pd.DataFrame,
    column_key: dict,
    description_column_list: list = None,
    sample: int = None,
) -> pd.DataFrame:
    """
    Normalizes the columns of a DataFrame based on a specified mapping.

    Args:
    -----
    df : ``pd.DataFrame``
        The input DataFrame to be normalized.
    column_key : ``dict``
        A dictionary mapping the original column names to the new column names.

    Keyword Args:
    -------------
    description_column_list : ``list``
        A list of column names to be merged into a single 'description' column. Default is None.
    sample : ``int``
        The number of rows to sample from the DataFrame. Default is None.

    Returns:
    --------
        pd.DataFrame: The normalized DataFrame with the columns renamed, merged, and dropped as specified.

    Notes:
    ------
    1.  The function normalizes the DataFrame by renaming columns, merging specified columns into a single 'description' column, and dropping columns that are not present in the specified mapping.
    2.  If the 'sample' parameter is provided, the function samples the specified number of rows from the DataFrame.

    Example:
    --------
    >>> df = pd.read_csv("data.csv")
    >>> print(df.head())
    ...        random    |  column    |   names   |   to    |   be    |   normalized
    ...        1         |    abc     |   xyz     |   def   |   gef   |   url1
    ...        2         |    hij     |   klm     |   nop   |   qrs   |   url2
    >>> normalized_df = normalize_dataframe(df, column_key, description_column_list=["names", "to", "be"], sample=1)
    >>> print(normalized_df.head())
    ...        id  |  name    |  description    |  imageUrl
    ...        1   |  abc     |  xyz, def, gef  |  url1

    Author: ``@ChinaiArman``
    """
    if description_column_list:
        df = merge_description_columns(df, description_column_list)
    if sample:
        df = df.sample(n=sample)
    df = rename_columns(df, column_key)
    df = drop_columns(df, list(column_key.keys()))
    return df.reset_index(drop=True)


def merge_dataframes(df_list: list) -> pd.DataFrame:
    """
    Merges multiple DataFrames into a single DataFrame.

    Args:
    -----
    df_list : ``list``
        A list of DataFrames to be merged.

    Returns:
    --------
    ``pd.DataFrame``
        The merged DataFrame containing the data from all the input DataFrames.

    Notes:
    ------
    1. The function concatenates the DataFrames in the list along the row axis and ignores the original index.
    2. All the DataFrames in the list must have the same columns for the merge to be successful.

    Example:
    --------
    >>> df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    >>> df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
    >>> merged_df = merge_dataframes([df1, df2])
    >>> print(merged_df)
    ...    A  |  B
    ... 0  1  |  3
    ... 1  2  |  4
    ... 2  5  |  7
    ... 3  6  |  8

    Author: ``@ChinaiArman``
    """
    merged_df = pd.concat(df_list, axis=0, ignore_index=True)
    return merged_df


def generate_keywords(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates keyword descriptions for a DataFrame containing image URLs.

    Args:
    -----
    df : ``pd.DataFrame``
        The input DataFrame to be normalized.

    Returns:
    --------
    ``pd.DataFrame``
        The normalized DataFrame with the new column 'keywordDescriptions' containing the generated keyword descriptions.

    Notes:
    ------
    1. The function generates keyword descriptions for the images in the DataFrame using Azure's dense captioning technology.
    2. The generated descriptions are stored in a new column 'keywordDescriptions' in the DataFrame.

    Example:
    --------
    >>> df = pd.read_csv("data.csv")
    >>> print(df.head())
    ...        id |  name |  description |  imageUrl
    ...        1  |  abc  |  xyz         |  url1
    >>> keyword_df = generate_keywords(df)
    >>> print(keyword_df.head())
    ...        id  |  name |  description  |  imageUrl  |  keywordDescriptions
    ...        1   |   abc |      xyz      |    url1    |  "description1"

    Author: ``@nataliecly``
    """
    descriptions = []
    for _, row in df.iterrows():
        try:
            imageUrl = row["imageUrl"]
            description = dc.normalize_dense_caption_response(dc.create_dense_captions(imageUrl))
            description = ", ".join(description)
            descriptions.append(description)
        except Exception as e:
            print(f"Error: {e}")
            descriptions.append("")
    df["keywordDescriptions"] = descriptions
    return df


def write_dataframe_to_csv(df: pd.DataFrame) -> None:
    """
    Writes a DataFrame to a CSV file.

    Args:
    -----
    df : ``pd.DataFrame``
        The DataFrame to be written to a CSV file.

    Returns:
    --------
    None

    Notes:
    ------
    1. This function writes the DataFrame to a CSV file stored in the 'DATA_SOURCE_FILE' environment variable.
    2. The id column of the DataFrame is converted to unique sequential integers for all rows before writing.

    Example:
    --------
    >>> df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    >>> write_dataframe_to_csv(df)
    ... # Dataframe saved as CSV file to a file specified in the environment variable 'DATA_SOURCE_FILE'.

    Author: ``@cc-dev-65535``
    """
    df.loc[:, "id"] = df.index
    df.to_csv(os.getenv("DATA_SOURCE_FILE"), index=False)


def main() -> None:
    """
    Normalizes and generates a modified CSV file.

    Args:
    -----
    None

    Returns:
    --------
    None

    Notes:
    ------
    1. The function normalizes the data sources by reading CSV files and applying data normalization.
    2. The normalized data sources are merged into a single DataFrame.
    3. Keyword descriptions are generated for the merged DataFrame and added as a column.
    4. The merged DataFrame is written to a CSV file.

    Example:
    --------
    >>> main()
    ... # Normalizes multiple CSV files and writes them to a new CSV file.

    Author: ``@cc-dev-65535``
    """
    # Normalize data sources
    df = pd.read_csv("server/data_source/data_files/hm.csv")
    df = normalize_dataframe(df, HM_COLUMN_KEY)
    df2 = pd.read_csv("server/data_source/data_files/asos.csv")
    df2 = normalize_dataframe(df2, ASOS_COLUMN_KEY)
    df3 = pd.read_csv("server/data_source/data_files/free_clothes.csv")
    df3 = normalize_dataframe(df3, FREE_CLOTHES, description_column_list=FREE_CLOTHES_DESCRIPTION_COLUMNS, sample=2000)

    # Merge data sources
    merged_df = merge_dataframes([df, df2, df3])

    # Generate keyword descriptions
    keyword_df = generate_keywords(merged_df)

    # Write merged DataFrame to CSV
    write_dataframe_to_csv(keyword_df)


if __name__ == "__main__":
    main()
