"""
Author: ``@levxxvi``
Version: ``1.0.0``

Description:
A class to interact with the data source stored in a CSV file.

Requirements:
This class requires the installation of the pandas library.
The data source file path must be specified in the environment variables under "DATA_SOURCE_FILE".

Usage:
To use this class, create an instance of the Database class and call the desired method.
To execute this module from the root directory, run the following command:
    ``python server/data_source/data_access.py``
"""


import pandas as pd
import uuid
import os.path
from dotenv import load_dotenv
import os
import sys

load_dotenv()
sys.path.insert(0, os.getenv("PYTHONPATH"))

from dense_captioning_model import dense_captioning as dc


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
    2. The data source is a CSV file specified in the environment variables.
    3. The class provides methods to retrieve data from the data source.
    4. The class uses the Pandas library to read the CSV file and manipulate the data.

    Methods:
    --------
    >>> get_data_frame()
    ... # Retrieves a pandas DataFrame from the data source.
    >>> get_item_by_id(id)
    ... # Retrieves Panadas DataFrame of an item by its id.
    >>> get_id_by_keyword_description(description)
    ... # Retrieves the id of an item by its description.
    >>> delete_row(id)
    ... # Deletes a row from the data source by its id.
    >>> add_row(new_row)
    ... # Adds a row to the data source.

    Author: ``@levxxvi``
    """
    def __init__(
        self
    ) -> None:
        """
        Initializes the Database class.
        """
        load_dotenv()
        if not os.path.exists(os.getenv("DATA_SOURCE_FILE")):
            raise FileNotFoundError("The data source file does not exist.")
        self.file_path = os.getenv("DATA_SOURCE_FILE")
        self.df = pd.read_csv(self.file_path, dtype={"id": str})
        try:
            self.df["keywordDescriptions"] = self.df["keywordDescriptions"].apply(
                lambda x: x.split(", ") if pd.notna(x) else [""]
            )
        except:
            pass

    def get_data_frame(
        self
    ) -> pd.DataFrame:
        """
        Retrieves a pandas DataFrame from the data source.

        Args:
        -----
        None.

        Returns:
        --------
        ``pd.DataFrame``
            The DataFrame containing the data from the data source.

        Notes:
        ------
        1. The method reads the CSV file specified in the environment variables.
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

    def get_item_by_id(
        self,
        id: str
    ) -> pd.DataFrame:
        """
        Retrieves Panadas DataFrame of an item by its id.

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

    def get_id_keyword_description(
        self
    ) -> pd.DataFrame:
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

    def delete_row(
        self,
        id: str
    ) -> bool:
        """
        Deletes a row from the data source by its id.

        Args:
        -----
        id : ``str``
            The id of the item to delete.

        Returns:
        --------
        ``bool``
            True if the row was deleted successfully, False otherwise.

        Notes:
        ------
        1. The method deletes the row with the provided id from the data source.

        Example:
        --------
        >>> db = Database()
        >>> db.delete_row(1)

        Author: ``@levxxvi``
        """
        curr_len = len(self.df)
        self.df = self.df[self.df['id'] != id]
        if len(self.df) == curr_len:
            return False
        else:
            self.df.reset_index(drop=True, inplace=True)
            self.write_to_csv()
            return True

    def add_row(
        self, 
        new_row: dict
    ) -> dict:
        """
        Adds a row to the data source.

        Args:
        -----
        new_row : ``dict``
            A dictionary containing the new row data.

        Returns:
        --------
        ``dict``
            The new row added to the data source.


        Notes:
        ------
        1. The method appends the new row to the data source.
        2. The method generates a unique identifier for the new row.
        3. The method normalizes the keyword descriptions using the dense captioning model.
        4. The method saves the updated data source to the CSV file.
        5. The method returns the new row added to the data source.

        Example:
        --------
        >>> db = Database()
        >>> new_row = {
        ...     'id': 3,
        ...     'name': 'new item',
        ...     'description': 'a new item',
        ...     'imageUrl': 'https://url.com',
        ...     'keywordDescriptions': 'new, item'
        ... }
        >>> db.add_row(new_row)

        Author: ``@levxxvi``
        """
        new_row['id'] = str(uuid.uuid4())
        print(new_row)
        new_row['keywordDescriptions'] = dc.normalize_dense_caption_response(dc.create_dense_captions(new_row['imageUrl']))
        self.df.loc[len(self.df)] = new_row
        self.write_to_csv()
        return new_row

    def edit_row(
        self, 
        id: str, 
        new_row: dict
    ) -> dict:
        """
        Edits a row in the data source.

        Args:
        -----
        id : ``str``
            The id of the item to edit.
        new_row : ``dict``
            A dictionary containing the new row data.

        Returns:
        --------
        ``dict``
            The edited row.

        Notes:
        ------
        1. The method edits the row with the provided id in the data source.
        2. The method normalizes the keyword descriptions using the dense captioning model.
        3. The method saves the updated data source to the CSV file.
        4. The method returns the edited row.

        Example:
        --------
        >>> db = Database()
        >>> edited_row = {
        ...     'name': 'edited item',
        ...     'description': 'an edited item',
        ...     'imageUrl': 'https://url.com',
        ...     'keywordDescriptions': 'edited, item'
        ... }
        >>> db.edit_row(3, edited_row)

        Author: ``@levxxvi``
        """
        self.delete_row(id)
        new_row['id'] = id
        new_row['keywordDescriptions'] = dc.normalize_dense_caption_response(dc.create_dense_captions(new_row['imageUrl']))
        self.df.loc[len(self.df)] = new_row
        self.write_to_csv()
        return new_row
    
    def write_to_csv(
        self
    ) -> None:
        """
        Writes the current dataframe to the CSV file.

        Args:
        -----
        None.

        Returns:
        --------
        None.

        Notes:
        ------
        1. The method writes the current data to the CSV file.

        Example:
        --------
        >>> db = Database()
        >>> db.write_to_csv()
        """
        df_to_write = self.df.copy(deep=True)
        df_to_write["keywordDescriptions"] = df_to_write["keywordDescriptions"].apply(
            lambda x: ", ".join(x)
        )
        df_to_write.to_csv(self.file_path, index=False)


def main(
) -> None:
    """
    Demonstrates the usage of the Database class.

    Args:
    -----
    None.

    Returns:
    --------
    None.

    Notes:
    ------
    1. The method demonstrates the usage of the Database class.

    Example:
    --------
    >>> main()
    ... # Prints the retrieved data from the data source.

    Author: ``@levxxvi``
    """
    db = Database()
    data = db.get_data_frame()
    print(data.head())
    item = db.get_item_by_id("1")
    print(item)
    item_from_keyword = db.get_id_keyword_description()
    print(item_from_keyword)


if __name__ == "__main__":
    main()
