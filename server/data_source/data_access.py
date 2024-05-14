"""
Author: ``@levxxvi``
Version: ``1.0.0``

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
    -----
    None.

    Attributes:
    -----------
    file_path : ``str``
        The path to the data source file.

    Raises:
    -------
    ``FileNotFoundError``
        If the data source file does not exist.

    Notes:
    ------
    1. The class is used to interact with the data source.
    2. The data source is a CSV file located at "server/data_source/data.csv".
    3. The class provides methods to retrieve data from the data source.
    4. The class uses the Pandas library to read the CSV file and manipulate the data.

    Methods:
    --------
    >>> get_data_frame()
    ... # Retreives a pandas DataFrame from the data source.
    >>> get_item_by_id(id)
    ... # Retreives Panadas DataFrame of an item by its id.
    >>> get_id_by_keyword_description(description)
    ... # Retreives the id of an item by its description.

    Author: ``@levxxvi``
    """
    def __init__(self) -> None:
        """
        Initializes the Database class.
        """
        if not os.path.exists("server/data_source/data.csv"):
            raise FileNotFoundError("The data source file does not exist.")
        self.file_path = "server/data_source/data.csv"
        self.df = pd.read_csv(self.file_path)
        try:
            self.df['keywordDescriptions'] = self.df['keywordDescriptions'].apply(lambda x: x.split(', '))
        except:
            pass

    def get_data_frame(self) -> pd.DataFrame:
        """
        Retreives a pandas DataFrame from the data source.

        Args:
        -----
        None.

        Returns:
        --------
        ``pd.DataFrame``
            The DataFrame containing the data from the data source.

        Notes:
        ------
        1. The method reads the CSV file located at ``server/data_source/data.csv``.
        2. The method returns the data as a pandas DataFrame.

        Example:
        --------
        >>> db = Database()
        >>> data = db.get_data_frame()
        >>> print(data.head())
        ... id  |  name             |  description  |  imageUrl          |  keywordDescriptions
        ... 1   |  amazing shirt    |  a shirt      |  https://url.com   |  shirt, red, amazing

        Author: ``@levxxvi``
        """
        return self.df

    def get_item_by_id(self, id: str) -> pd.DataFrame:
        """
        Retreives Panadas DataFrame of an item by its id.

        Args:
        -----
        id : ``str``
            The id of the item to retrieve.

        Returns:
        --------
        ``pd.DataFrame``
            The DataFrame containing the item data.

        Notes:
        ------
        1. The method filters the data by the provided id and returns the item as a DataFrame.

        Example:
        --------
        >>> db = Database()
        >>> item = db.get_item_by_id(1)
        >>> print(item)
        ... id  |  name          |  description  |  imageUrl          |  keywordDescriptions
        ... 1   |  amazing shirt |  a shirt      |  https://url.com   |  shirt, red, amazing

        Author: ``@levxxvi``
        """
        item = self.df.loc[self.df['id'] == id]
        return item
    
    def get_id_keyword_description(self) -> pd.DataFrame:
        """
        Retrieves a pandas DataFrame containing only the 'id' and 'keywordDescriptions' columns of all items.

        Args:
        -----
        None.

        Returns:
        --------
        ``pd.DataFrame``
            A DataFrame containing only the 'id' and 'keywordDescriptions' columns for all items.

        Notes:
        ------
        1. Returns a DataFrame with only the 'id' and 'keywordDescriptions' columns.

        Example:
        --------
        >>> db = Database()
        >>> detailed_items = db.get_id_keyword_description()
        >>> print(detailed_items)
        ... id  |  keywordDescriptions
        ... 1   |  casual, comfortable, cool
        ... 2   |  elegant, formal, sleek

        Author: ``@Ehsan138``
        """
        return self.df[['id', 'keywordDescriptions']]



def main() -> None:
    """
    """
    pass


if __name__ == "__main__":
    # db = Database()
    # data = db.get_data_frame()
    # print(data.head())
    # item = db.get_item_by_id(1)
    # print(item)
    main()
