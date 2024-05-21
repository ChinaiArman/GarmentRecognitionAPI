"""
Author: ``@ChinaiArman``
Version: ``1.0.0``

Description:
This module contains functions to normalize text embeddings and perform semantic textual analysis.

Requirements:
This module requires the transformers library and the torch library.
This module requires the dense_captioning_model module.

Usage:
To execute this module from the root directory, run the following command:
    ``python server/embedded_model/semantic_textual_analysis.py``
"""

import torch.nn.functional as F
from torch import Tensor, cuda, no_grad
from transformers import AutoTokenizer, AutoModel
import pandas as pd

pd.options.mode.copy_on_write = True

from dotenv import load_dotenv
import os
import sys

load_dotenv()
sys.path.insert(0, os.getenv("PYTHONPATH"))

from dense_captioning_model import dense_captioning as dc
from data_source import data_access as da


def load_embedded_model(
) -> tuple[
        AutoTokenizer,
        AutoModel
    ]:
    """
    Load the pre-trained transformer model and tokenizer for generating text embeddings.

    Args:
    -----
    None.

    Returns:
    --------
    ``tuple``
        A tuple containing the tokenizer and model objects.

    Notes:
    ------
    1. The model and tokenizer are pre-trained on a large corpus and can be used to generate embeddings for text data.
    2. The model used here is the GTE-base model, which is a transformer-based model.
    3. The tokenizer is used to convert text data into input tensors for the model.
    4. The model generates embeddings for the input text, which can be used for various NLP tasks.

    Example:
    --------
    >>> tokenizer, model = load_embedded_model()
    >>> # Use the tokenizer and model objects for further processing.

    Author: ``@Ehsan138``
    """
    # Load the pre-trained tokenizer from the transformers library
    tokenizer = AutoTokenizer.from_pretrained(os.getenv("EMBEDDED_MODEL"))
    # Load the pre-trained model from the transformers library
    model = AutoModel.from_pretrained(os.getenv("EMBEDDED_MODEL"))
    return tokenizer, model


def average_pool(
    last_hidden_states: Tensor,
    attention_mask: Tensor
) -> Tensor:
    """
    Applies average pooling to the last hidden states of a transformer model output, considering the attention mask.

    Args:
    -----
    last_hidden_states : ``Tensor``
        The output tensor from the last hidden layer of a transformer model, typically of shape (batch_size, sequence_length, hidden_size).
    attention_mask : ``Tensor``
        An attention mask tensor of shape (batch_size, sequence_length) where `True` indicates a token's presence and `False` indicates padding.

    Returns:
    --------
    ``Tensor``
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

    Author: ``@cc-dev-65535``
    """
    # Apply attention mask to zero out padded tokens
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    # Sum the hidden states and divide by the number of non-padded tokens to get the average
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


def normalize_embeddings(
    embeddings: Tensor
) -> list:
    """
    Normalizes each vector in the embeddings tensor to have a unit L2 norm. This means that the length or magnitude
    of each vector will be scaled to 1. The normalization is performed across the last dimension of the tensor,
    which typically corresponds to the feature or embedding dimension.

    Args:
    -----
    embeddings : ``Tensor``
        The embeddings tensor to normalize. This tensor could typically have a shape like (batch_size, embedding_dimension), where each row represents an embedding vector.

    Returns:
    --------
    ``List``
        The normalized embeddings tensor, stored as a list, with each vector having a unit norm. The shape of the tensor remains unchanged.

    Notes:
    ------
    1. The L2 norm, used here, scales the vector components such that the square root of the sum of the squared components equals 1.
    2. This operation is commonly used to prepare embeddings for cosine similarity calculations, as it ensures that the angle between vectors reflects their semantic similarity more than their magnitude.

    Example:
    --------
    >>> embeddings = torch.tensor([[3.0, 4.0], [1.0, 2.0]])
    >>> normalized_embeddings = normalize_embeddings(embeddings)
    >>> print(normalized_embeddings)
    ... tensor([[0.6000, 0.8000], [0.4472, 0.8944]])
    # Explanation:
    # The first vector [3.0, 4.0] has an original length of 5. After normalization, its components are scaled so that
    # its length becomes 1, calculated as sqrt(0.6^2 + 0.8^2) = 1.
    # The second vector [1.0, 2.0] is normalized similarly, from a length of sqrt(5) to 1.

    Author: ``@Ehsan138``
    """
    # Normalize embeddings to have unit L2 norm (length = 1)
    embeddings = F.normalize(embeddings, p=2, dim=1)
    # Calculate cosine similarity scores between the first embedding and the rest
    scores = (embeddings[:1] @ embeddings[1:].T) * 100
    # Return the similarity scores as a list
    return scores[0].tolist()


def image_model_wrapper(
    filepath_or_url: str,
    size: int
) -> list:
    """
    Wrapper function to call the dense captioning model and then perform semantic textual analysis.

    Args:
    -----
    filepath_or_url : ``str``
        The filepath or url of the image to be analyzed.
    size : ``int``
        The number of similar items to return.

    Returns:
    --------
    ``list``
        A list of the top `size` similar items based on the analysis.

    Notes:
    ------
    1. The function calls the dense captioning model to generate keywords from the image.
    2. The keywords are then used to perform semantic textual analysis to find similar items in the database.
    3. The function returns the IDs of the top `size` similar items based on the analysis.
    4. If no keywords are generated from the image, an empty list is returned.

    Example:
    --------
    >>> url = "https://image-url.com/image.jpg"
    >>> size = 5
    >>> similar_items = model_wrapper(url, size)
    >>> print(similar_items)
    ... ["item1", "item2", "item3", "item4", "item5"]

    Author: ``@ChinaiArman``
    """
    keywords = dc.normalize_dense_caption_response(
        dc.create_dense_captions(filepath_or_url)
    )
    if not keywords:
        return []
    df = vector_comparison(keywords)
    return df["id"].tolist()[:size]


def keyword_model_wrapper(
    keywords: list,
    size: int
) -> list:
    """
    Wrapper function to call the semantic textual analysis function.

    Args:
    -----
    keywords : ``list``
        A list of keywords generated from the image.
    size : ``int``
        The number of similar items to return.
    
    Returns:
    --------
    ``list``
        A list of the top `size` similar items based on the analysis.

    Notes:
    ------
    1. The function calls the semantic textual analysis function to find similar items in the database based on the input keywords.
    2. The function returns the IDs of the top `size` similar items based on the analysis.

    Example:
    --------
    >>> keywords = ["apple", "banana"]
    >>> size = 5
    >>> similar_items = keyword_model_wrapper(keywords, size)
    >>> print(similar_items)
    ... ["item1", "item2", "item3", "item4", "item5"]

    Author: ``@ChinaiArman``
    """
    if not keywords:
        return []
    df = vector_comparison(keywords)
    return df["id"].tolist()[:size]


def vector_comparison(
    keywords: list
) -> pd.DataFrame:
    """
    Performs semantic textual analysis to compare the input keywords with the database keywords.

    Args:
    -----
    keywords : ``list``
        A list of keywords generated from the image.

    Returns:
    --------
    ``pd.DataFrame``
        A DataFrame containing the IDs and similarity scores of the database items.

    Example:
    --------
    >>> vector_comparison(keywords)
    ... # Returns a DataFrame with the IDs and similarity scores of the database items.

    Notes:
    ------
    1. This function retrieves the database keywords and their descriptions.
    2. It calculates the similarity scores between the input keywords and the database keywords.
    3. The function returns a DataFrame with the IDs and similarity scores of the database items.

    Author: ``@nataliecly``
    """
    db = da.Database()
    database_keywords = db.get_id_keyword_description()
    embeddings = semantic_textual_analysis(
        keywords, database_keywords["keywordDescriptions"].tolist()
    )
    database_keywords.loc[:, "vector"] = embeddings
    database_keywords = database_keywords.sort_values(by="vector", ascending=False)
    return database_keywords


def semantic_textual_analysis(
    keywords: list,
    database_keywords: list
) -> list:
    """
    Perform semantic textual analysis to calculate similarity scores between a list of keywords and a list of database keywords.

    Args:
    -----
        keywords : ``list``
            A list of keywords to be analyzed.
        database_keywords : ``list``
            A list of keywords from the database for comparison.

    Returns:
    --------
    ``list``
        A list of similarity scores between the input keywords and the database keywords.

    Notes:
    ------
    1. This function uses a pre-trained model to calculate text embeddings for the input keywords and database keywords.
    2. The similarity scores are calculated by taking the dot product of the normalized embeddings.
    3. The scores are scaled by multiplying them by 100.

    Examples:
    ---------
    >>> keywords = ["apple"]
    >>> database_keywords = [["fruit", "apple"], ["fruit", "banana"], ["fruit", "orange"]]
    >>> semantic_textual_analysis(keywords, database_keywords)
    ... [90.51500701904297, 81.43607330322266, 81.61931610107422]

    Author: ``@cc-dev-65535``
    """
    # Load the pre-trained model and tokenizer
    tokenizer, model = load_embedded_model()
    device = "cuda:0" if cuda.is_available() else "cpu"
    print(f"Device: {device}")
    model.to(device)
    cuda.empty_cache()
    print(f"Memory allocated: {cuda.memory_allocated()}")

    # Tokenize the input texts
    input_sentence = ", ".join(keywords)
    sentence_list = [", ".join(keyword_list) for keyword_list in database_keywords]
    batch_dict = tokenizer(
        [input_sentence] + sentence_list,
        max_length=512,
        padding=True,
        truncation=True,
        return_tensors="pt",
    ).to(device)

    # Pass input to model to get text embeddings
    print("Begin embedded model processing...")
    with no_grad():
        outputs = model(**batch_dict)
    embeddings = average_pool(outputs.last_hidden_state, batch_dict["attention_mask"])

    # Normalize the embeddings
    normalized_embeddings = normalize_embeddings(embeddings)
    return normalized_embeddings


def main(
) -> None:
    """
    Example usage of the semantic_textual_analysis function.

    Args:
    -----
    None.

    Returns:
    --------
    None.

    Notes:
    ------
    1. This function demonstrates the usage of the semantic_textual_analysis function with sample input.
    2. The function prints the similarity scores between the input keywords and the database keywords.

    Example:
    --------
    >>> main()
    ... [90.51500701904297, 81.43607330322266, 81.61931610107422]

    Author: ``@Ehsan138``
    """
    # Example usage of the semantic_textual_analysis function
    print(
        semantic_textual_analysis(
            ["brown", "dog"],
            [
                ["cat"],
                ["fish"],
                ["brown", "bear"],
                ["brown", "hot dog"],
                ["brown", "german shepherd"],
            ],
        )
    )


if __name__ == "__main__":
    main()
