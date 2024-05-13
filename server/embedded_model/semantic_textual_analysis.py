"""
"""

import torch.nn.functional as F
from torch import Tensor
from transformers import AutoTokenizer, AutoModel
import pandas as pd

# Initialize tokenizer and model from a pre-trained transformer.
tokenizer = AutoTokenizer.from_pretrained("thenlper/gte-base")
model = AutoModel.from_pretrained("thenlper/gte-base")

def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    """
    Applies average pooling to the last hidden states of a transformer model output, considering the attention mask.

    Args:
    -----
    last_hidden_states : Tensor
        The output tensor from the last hidden layer of a transformer model, typically of shape (batch_size, sequence_length, hidden_size).
    attention_mask : Tensor
        An attention mask tensor of shape (batch_size, sequence_length) where `True` indicates a token's presence and `False` indicates padding.

    Returns:
    --------
    Tensor
        The average-pooled embeddings tensor of shape (batch_size, hidden_size).

    Notes:
    ------
    1. The function masks out padded positions in the input tensor (setting them to zero) before computing the average to ensure that only valid tokens contribute to the resulting embeddings.
    2. This operation is essential for handling variable sequence lengths and preventing skewed representation due to padding.

    Example:
    --------
    >>> last_hidden_states = torch.randn(2, 3, 768)  # Simulated transformer output for 2 examples, each with 3 tokens.
    >>> attention_mask = torch.tensor([[1, 1, 0], [1, 0, 0]])  # First example has 2 tokens, second has 1.
    >>> averaged_embeddings = average_pool(last_hidden_states, attention_mask)
    >>> print(averaged_embeddings.shape)
    ... torch.Size([2, 768])

    Author: ``@Ehsan138``
    """
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


def normalize_embeddings(embeddings: Tensor):
    """
    Normalizes each vector in the embeddings tensor to have a unit L2 norm. This means that the length or magnitude
    of each vector will be scaled to 1. The normalization is performed across the last dimension of the tensor, 
    which typically corresponds to the feature or embedding dimension.

    Args:
        embeddings (Tensor): The embeddings tensor to normalize. This tensor could typically have a shape 
                             like (batch_size, embedding_dimension), where each row represents an embedding vector.

    Returns:
        Tensor: The normalized embeddings tensor, with each vector having a unit norm. The shape of the tensor remains unchanged.

    Notes:
        The L2 norm, used here, scales the vector components such that the square root of the sum of the squared components equals 1.
        This operation is commonly used to prepare embeddings for cosine similarity calculations, as it ensures that the angle between
        vectors reflects their semantic similarity more than their magnitude.

    Example:
        >>> embeddings = torch.tensor([[3.0, 4.0], [1.0, 2.0]])
        >>> normalized_embeddings = normalize_embeddings(embeddings)
        >>> print(normalized_embeddings)
        tensor([[0.6000, 0.8000],
                [0.4472, 0.8944]])
        # Explanation: 
        # The first vector [3.0, 4.0] has an original length of 5. After normalization, its components are scaled so that
        # its length becomes 1, calculated as sqrt(0.6^2 + 0.8^2) = 1.
        # The second vector [1.0, 2.0] is normalized similarly, from a length of sqrt(5) to 1.

    Author: ``@Ehsan138``
    """
    return F.normalize(embeddings, p=2, dim=1)


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