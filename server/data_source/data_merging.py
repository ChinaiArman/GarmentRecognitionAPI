"""
Author: ``@Ehsan138``
Version: ``1.0.0``

Description:
Merges two datasets: one containing image URLs and another containing styles information.
The function merges these datasets based on the image filenames and style IDs after processing them for compatibility.
The merged dataset is then saved as a new CSV file.

Requirements:
This script requires the installation of the pandas library.

Usage:
To execute this module from the root directory, run the following command:
    ``python server/data_source/data_merging.py``
"""


import pandas as pd


def merge_datasets(
    images_csv_path: str,
    styles_csv_path: str,
    output_csv_path: str
) -> None:
    """
    Merges two datasets: one containing image URLs and another containing styles information.

    Args:
    -----
    images_csv_path : ``str``
        The file path for the CSV file containing image URLs.
    styles_csv_path : ``str``
        The file path for the CSV file containing styles information.
    output_csv_path : ``str``
        The output file path for the merged dataset.

    Returns:
    -------
    ``None``
        The function saves the merged dataset to a CSV file specified by output_csv_path.

    Notes:
    -----
    1. The function modifies the 'filename' field in the images dataset by removing the '.jpg' extension and converts the 'id' in the styles dataset from integer to string to facilitate the merging based on these modified fields.

    Example:
    --------
    >>> images_csv_path = './data-files/images.csv'
    >>> styles_csv_path = './data-files/styles.csv'
    >>> output_csv_path = './data-files/initial_data.csv'
    >>> merge_datasets(images_csv_path, styles_csv_path, output_csv_path)
    ... # Merged dataset saved to ./data-files/initial_data.csv

    Author: ``@Ehsan138``
    """
    # Load the datasets
    images_df = pd.read_csv(images_csv_path)
    styles_df = pd.read_csv(styles_csv_path)

    # Convert 'id' in styles_df from int to string to match 'filename' in images_df
    styles_df['id'] = styles_df['id'].astype(str)

    # Remove '.jpg' from filenames in the images dataframe to match the ID format in the styles dataframe
    images_df['filename'] = images_df['filename'].str.replace('.jpg', '', regex=False)

    # Merge the dataframes based on the cleaned 'filename' in images_df and 'id' in styles_df
    merged_df = pd.merge(images_df, styles_df, left_on='filename', right_on='id')

    # Save the merged dataframe to a new CSV file
    merged_df.to_csv(output_csv_path, index=False)
    print(f"Merged dataset saved to {output_csv_path}")


def main() -> None:
    """
    Runs the data merging process.

    Args:
    -----
    None

    Returns:
    --------
    None

    Notes:
    ------
    1. This function calls the merge_datasets function with the paths to the CSV files containing image URLs and styles information.
    2. The merged dataset is saved to a new CSV file.

    Example:
    --------
    >>> main()
    ... # Merged dataset saved to ./data-files/initial_data.csv

    Author: ``@nataliecly``
    """
    # Paths to your CSV files (please change this to your own absolute paths if needed to run again)
    images_csv_path = './data-files/images.csv'
    styles_csv_path = './data-files/styles.csv'
    output_csv_path = './data-files/initial_data.csv'

    # Call the merge function
    merge_datasets(images_csv_path, styles_csv_path, output_csv_path)


if __name__ == "__main__":
    main()
