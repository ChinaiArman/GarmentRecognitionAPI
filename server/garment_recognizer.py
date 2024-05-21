"""
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
    db : ``Database``
        An instance of the Database class
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
        self.db = Database()
        self.tokenizer, self.model = load_embedded_model()

    def insert_row(
        self,
        data: dict
    ) -> None:
        """
        Inserts a new row of data into the data source.

        Args:
        -----
        data : ``dict``
            A dictionary containing the new row data.

        Returns:
        --------
        None.

        Notes:
        ------
        1. The method inserts a new row into the data source.

        Example:
        --------
        >>> gr = GarmentRecognizer()
        >>> gr.insert_row({'id': 1, 'name': 'shirt', 'color': 'blue'})
        ... # Inserts the row into the data source.

        Author: ``@nataliecly``
        """
        self.db.add_row(data)
    
    def delete_row(
        self,
        id: str
    ) -> None:
        """
        Deletes a row from the data source by its id.

        Args:
        -----
        id : ``str``
            The id of the item to delete.

        Returns:
        --------
        None.

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
        return self.db.delete_row(id)

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
        item_ids = image_model_wrapper(file_path_or_url, size)
        return [
            self.db.get_item_by_id(item_id).to_dict("records")[0]
            for item_id in item_ids
        ]
    
    def get_item_by_id(
        self,
        id: int
    ) -> dict:
        """
        Retrieves an item from the data source by its id.

        Args:
        -----
        id : ``int``
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
        item = self.db.get_item_by_id(id)
        return item.to_dict("records")[0] if not item.empty else None
    
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
        >>> items = gr.get_items_by_keywords(['shirt', 'blue'])
        >>> print(items)
        ... # Prints a list of items that contain the keywords 'shirt' and 'blue'.

        Author: ``@ChinaiArman``    
        """
        items = keyword_model_wrapper(keywords, size)
        return [
            self.db.get_item_by_id(item_id).to_dict("records")[0]
            for item_id in items
        ]


def main():
    garment_recognizer = GarmentRecognizer()
    print("Get items by semantic search...")
    url = "http://assets.myntassets.com/v1/images/style/properties/be5106fa146a771fdb128833b4ab9b8b_images.jpg"
    print(garment_recognizer.get_item_by_semantic_search(url, 5))


if __name__ == "__main__":
    main()
