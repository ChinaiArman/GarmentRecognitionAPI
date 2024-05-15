"""
Author: ``@ChinaiArman``
Version: ``1.0.0``

Description:
Main function to demonstrate the usage of the embedded model.
Shows the top results of an image when compared to other items in the database.

Requirements:
This module requires the semantic_textual_analysis module.
This module requires the data_access module.

Usage:
To use this module, run the following command:
    ``python server/embedded_model/main.py <filepath_or_url> <size>``
where <filepath_or_url> is the file path or URL of the image and <size> is the number of results to return.
"""


import semantic_textual_analysis as sta
import argparse

from dotenv import load_dotenv
import os
import sys

load_dotenv()
sys.path.insert(0, os.getenv("PYTHONPATH"))

from data_source import data_access as da


def main(
) -> None:
    """
    Main function to demonstrate the usage of the embedded model.

    Args:
    -----
    None.

    Returns:
    --------
    None.

    Notes:
    ------
    1. The function defines a console parser and adds arguments.
    2. This function calls the model_wrapper function from the semantic_textual_analysis module.
    3. The function uses the Database class from the data_access module to retrieve the item descriptions.
    4. The function prints the results of the model to the console.

    Example:
    --------
    >>> python main.py "image.jpg" 5
    ... # Prints the top 5 results of the dense captioning model.

    Author: ``@ChinaiArman``
    """
    parser = argparse.ArgumentParser(description="Generates keyword captions of images using Azure's dense captioning technology.")
    parser.add_argument("filepath_or_url", action="store", help="An image file path or URL")
    parser.add_argument("size", action="store", help="The number of results to return.")
    args = parser.parse_args()

    db = da.Database()

    try:
        results = sta.model_wrapper(args.filepath_or_url, int(args.size))
    except Exception:
        raise ValueError("size must be an integer.")

    print("Results: ")
    for row_id in results:
        print(f"\t{db.get_item_by_id(row_id)}")
    

if __name__ == "__main__":
    main()
