"""
Author: ``@cc-dev-65535``
Version: ``1.0.0``

Description:
A class that acts as an interface to provide access to the models that recognize garments.
The class also provides methods to interact with the data source.

Requirements:
This class requires the installation of the pandas, torch, and transformers libraries.
The data source file path must be specified in the environment variables under "DATA_SOURCE_FILE".

Usage:
To use this class, create an instance of the GarmentRecognizer class and call the desired method.
To execute this module from the root directory, run the following command:
    ``python server/garment_recognizer.py``
"""

from data_source.data_access import Database
from embedded_model.semantic_textual_analysis import image_model_wrapper, load_embedded_model, keyword_model_wrapper


class GarmentRecognizer:
    """
    Class to recognize garments and interact with the data source.

    Args:
    -----
    None.

    Attributes:
    -----------
    tokenizer: ``Tokenizer``
        The tokenizer used to tokenize the text data.
    model: ``Model``
        The model used to extract the semantic meaning of the text data.

    Methods:
    --------
    >>> insert_row(data)
    ... # Inserts a row into the data source.
    >>> delete_row(id)
    ... # Deletes a row from the data source by its id.
    >>> get_item_by_semantic_search(file_path_or_url, size)
    ... # Gets a list of items from data source similar to the provided image by using a semantic search.
    >>> get_item_by_id(id)
    ... # Retrieves an item from the data source by its id.
    >>> get_items_by_keywords(keywords, size)
    ... # Retrieves items from the data source by their keywords.
    
    Notes:
    ------
    1. The class provides methods to interact with the data source and recognize garments.
    2. The class uses the Database class to interact with the data source.
    3. The class uses the embedded model to extract the semantic meaning of the text data.

    Author: ``@ChinaiArman``
    """
    def __init__(
        self
    ) -> None:
        """
        Initializes the Database class.
        """
        self.tokenizer, self.model = load_embedded_model()

    def insert_row(
        self,
        data: dict
    ) -> dict:
        """
        Inserts a new row of data into the data source.

        Args:
        -----
        data : ``dict``
            A dictionary containing the new row data.

        Returns:
        --------
        ``dict``
            A dictionary containing the inserted row data.

        Notes:
        ------
        1. The method inserts a new row into the data source.
        2. The method returns the id of the inserted row.

        Example:
        --------
        >>> gr = GarmentRecognizer()
        >>> gr.insert_row({'id': 1, 'name': 'shirt', 'description': 'A blue shirt.', 'imageUrl': 'http://example.com/image.jpg'})
        ... # Inserts the row into the data source.

        Author: ``@nataliecly``
        """
        db = Database()
        return db.add_row(data)
    
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
        >>> gr = GarmentRecognizer()
        >>> gr.delete_row(1)
        ... # Deletes the row with id 1 from the data source.

        Author: ``@levxxvi``
        """
        db = Database()
        return db.delete_row(id)

    def get_item_by_semantic_search(
        self,
        file_path_or_url: str,
        size: int
    ) -> list:
        """
        Gets a list of items from data source similar to the provided image by using a semantic search.

        Args:
        -----
        file_path_or_url : ``str``
            The path to the image file or the URL of the image.
        size : ``int``
            The number of items to return in the list.

        Returns:
        --------
        ``list``
            A list of those items similar to the provided image, up to `size` in length.

        Notes:
        ------
        1. The method uses the embedded model to extract the semantic meaning of the provided image.
        2. The method then uses the semantic meaning to find similar items in the data source.
        3. The method returns a list of specified size of the most similar items in the data source.

        Example:
        --------
        >>> gr = GarmentRecognizer()
        >>> gr.get_item_by_semantics('path/to/image.jpg', 5)
        ... # Returns a list of 5 items from data source most similar to the provided image.

        Author: ``@cc-dev-65535``
        """
        db = Database()
        item_ids = image_model_wrapper(
            file_path_or_url,
            size,
            self.model,
            self.tokenizer
        )
        return [
            db.get_item_by_id(item_id).fillna("").to_dict("records")[0]
            for item_id in item_ids
        ]
    
    def get_item_by_id(
        self,
        id: str
    ) -> dict:
        """
        Retrieves an item from the data source by its id.

        Args:
        -----
        id : ``str``
            The id of the item to retrieve.

        Returns:
        --------
        ``dict``
            The item data.

        Notes:
        ------
        1. The method retrieves the item with the provided id from the data source.

        Example:
        --------
        >>> gr = GarmentRecognizer()
        >>> item = gr.get_item_by_id(1)
        >>> print(item)
        ... # Prints the item with id 1 from the data source.

        Author: ``@Ehsan138``
        """
        db = Database()
        item = db.get_item_by_id(id)
        if len(item) == 0:
            print("in here")
            return None
        return item.fillna("").to_dict("records")[0] if not item.empty else None
    
    def get_items_by_keywords(
        self,
        keywords: list,
        size: int
    ) -> list:
        """
        Retrieves items from the data source by their keywords.
        
        Args:
        -----
        keywords : ``list``
            A list of keywords to search for.
        size : ``int``
            The number of items to return in the list.
        
        Returns:
        --------
        ``list``
            A list of items that contain the provided keywords.

        Notes:
        ------
        1. The method retrieves items from the data source that contain the provided keywords.

        Example:
        --------
        >>> gr = GarmentRecognizer()
        >>> items = gr.get_items_by_keywords(['shirt', 'blue'], 5)
        >>> print(items)
        ... # Prints a list of items that contain the keywords 'shirt' and 'blue'.

        Author: ``@ChinaiArman``    
        """
        db = Database()
        items = keyword_model_wrapper(
            keywords,
            size,
            self.model,
            self.tokenizer
        )
        return [
            db.get_item_by_id(item_id).fillna("").to_dict("records")[0]
            for item_id in items
        ]
    
    def edit_row(
        self, 
        id: str, 
        data: dict
    ) -> dict:
        """
        Edits a garment in the data source.

        Args:
        -----
        id : ``str``
            The id of the garment to edit.
        data : ``dict``
            The new data for the garment.

        Returns:
        --------
        ``dict``
            The edited garment data.

        Notes:
        ------
        1. The method edits the garment with the provided id in the data source.

        Example:
        --------
        >>> gr = GarmentRecognizer()
        >>> gr.edit_garment(1, {'name': 'shirt', 'description': 'A red shirt.', 'imageUrl': 'http://example.com/image.jpg'})
        ... # Edits the garment with id 1 in the data source.

        Author: ``@levxxvi``
        """
        db = Database()
        if not all(key in data for key in ['name', 'description', 'imageUrl', 'id']):
            raise ValueError()
        return db.edit_row(id, data)


def main(
) -> None:
    """
    Main function to demonstrate the usage of the GarmentRecognizer class.

    Args:
    -----
    None.

    Returns:
    --------
    None.

    Notes:
    ------
    1. The function demonstrates the usage of the GarmentRecognizer class.
    
    Example:
    --------
    >>> main()
    ... # Demonstrates the usage of the GarmentRecognizer class.

    Author: ``@Ehsan138``
    """
    garment_recognizer = GarmentRecognizer()
    print("Get items by semantic search...")
    url = "http://assets.myntassets.com/v1/images/style/properties/be5106fa146a771fdb128833b4ab9b8b_images.jpg"
    print(garment_recognizer.get_item_by_semantic_search(url, 5))


if __name__ == "__main__":
    main()
