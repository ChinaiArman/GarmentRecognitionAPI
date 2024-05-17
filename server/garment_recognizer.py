"""
"""


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

