"""
"""

import pandas as pd


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
    """
    df['description'] = df[column_list].apply(lambda x: ', '.join(x.dropna().astype(str)), axis=1)
    df.drop(columns=column_list, inplace=True)
    return df.reset_index(drop=True)


def rename_columns(df: pd.DataFrame, column_key: dict) -> pd.DataFrame:
    """
    """
    for key, value in column_key.items():
        df.rename(columns={value: key}, inplace=True)
    return df.reset_index(drop=True)


def drop_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    """
    for column in df.columns:
        if column not in columns:
            df.drop(column, axis=1, inplace=True)
    return df.reset_index(drop=True)
    

def normalize_dataframe(df: pd.DataFrame, column_key, description_column_list=None) -> pd.DataFrame:
    """
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