"""
Author: ``@levxxvi``
Version: 1.0.0

Description:
A class to interact with the data source stored in a CSV file.

Requirements:
This class requires the installation of the pandas library.
The data source file must be located at "server/data-source/data.csv".

Usage:
To use this class, create an instance of the Database class and call the desired method.
In the command line, you can run the following commands to interact with the data source:
    ``python data_access.py``
"""


import pandas as pd
import os.path


class Database:
    """
    Class to interact with the data source.

    Args:
        None.

    Attributes:
        file_path (str): The path to the data source file.

    Raises:
        FileNotFoundError: If the data source file does not exist.

    Notes:
        - The class is used to interact with the data source.
        - The data source is a CSV file located at "server/data-source/data.csv".
        - The class provides methods to retrieve data from the data source.
        - The class uses the Pandas library to read the CSV file and manipulate the data.

    Author: ``@levxxvi``
    """
    def __init__(self) -> None:
        """
        Initializes the Database class.
        """
        if not os.path.exists("server/data-source/data.csv"):
            raise FileNotFoundError("The data source file does not exist.")
        self.file_path = "server/data-source/data.csv"

    def get_data_frame(self) -> pd.DataFrame:
        """
        Retreives a pandas DataFrame from the data source.

        Args:
            None.

        Returns:
            pd.DataFrame: The DataFrame containing the data from the data source.

        Notes:
            - The method reads the CSV file located at "server/data-source/data.csv".
            - The method returns the data as a pandas DataFrame.

        Author: ``@levxxvi``
        """
        df = pd.read_csv(self.file_path)
        return df

    def get_item_by_id(self, id) -> pd.DataFrame:
        """
        Retreives Panadas DataFrame of an item by its id.

        Args:
            id: The id of the item to retrieve.

        Returns:
            pd.DataFrame: The DataFrame containing the item data.

        Notes:
            - The method uses the get_data_frame() method to retrieve the data.
            - The method filters the data by the provided id and returns the item as a DataFrame.

        Author: ``@levxxvi``
        """
        df = self.get_data_frame()
        item = df.loc[df['id'] == id]
        return item
    
    def get_id_by_keyword_description(self, description):
        """
        """
        pass


if __name__ == "__main__":
    db = Database()
    data = db.get_data_frame()
    print(data.head())
    item = db.get_item_by_id(1)
    print(item)
