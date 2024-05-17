"""
"""

import pandas as pd
from data_source.data_access import Database
from embedded_model.semantic_textual_analysis import model_wrapper, load_embedded_model


class GarmentRecognizer:
    """
    """
    def __init__(
        self
    ) -> None:
        """
        Initializes the Database class.
        """
        self.db = Database()
        self.tokenizer, self.model = load_embedded_model()

    def delete_row(self, id: str) -> None:
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
        self.db.delete_row(id)

    def get_item_by_semantic_search(self, file_path_or_url: str, size: int) -> list:
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
        item_ids = model_wrapper(file_path_or_url, size)
        return [
            self.db.get_item_by_id(item_id).to_dict("records")[0]
            for item_id in item_ids
        ]


def main():
    garment_recognizer = GarmentRecognizer()
    print("Get items by semantic search...")
    url = "http://assets.myntassets.com/v1/images/style/properties/be5106fa146a771fdb128833b4ab9b8b_images.jpg"
    print(garment_recognizer.get_item_by_semantic_search(url, 5))


if __name__ == "__main__":
    main()
