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
        """
        self.db = Database()
        self.tokenizer, self.model = load_embedded_model()
