"""
"""


# need to add these to requirements.txt
import torch.nn.functional as F
from torch import Tensor
from transformers import AutoTokenizer, AutoModel
import pandas as pd


def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    """
    """
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


def normalize_embeddings(embeddings: Tensor):
    """
    makes the embedding results a decimal from 0-1
    """
    pass


def model_wrapper(url: str, size: int) -> list:
    """
    calls vector_comparison, returns 'size' top results.
    will generate the keywords for the image here from dense_captioning_model.py
    """
    pass


def vector_comparison(keywords: list) -> pd.DataFrame:
    """
    calls semantic_textual_analysis, returns an updated dataframe with an extra vector column with the analysis
    """
    pass


def semantic_textual_analysis(keywords: list, database_keywords: list) -> list:
    """
    keywords = the keywords of the image being compared
    database_keywords = list of keywords from the database
    returns a new column with the vectors for the analysis
    """
    pass


def main() -> None:
    """
    """
    pass


if __name__ == '__main__':
    pass