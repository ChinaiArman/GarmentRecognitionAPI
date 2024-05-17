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
        """
        

