"""
Author: ``@ChinaiArman``
Version: ``1.0.0``

Description:
Generates keyword captions of images using Azure's dense captioning technology.
The module returns the result of the image analysis, which includes the dense captions and metadata.
The dense captions are printed to the console, along with the image height, width, and model version.

Requirements:
This module requires the following environment variables to be set:
    - AZURE_VISION_ENDPOINT: The endpoint of the Azure Vision service.
    - AZURE_VISION_KEY_1: The key for the Azure Vision service.
The module uses the Azure Cognitive Services SDK to interact with the Azure Vision service.

Usage:
To execute this module, run the following command:
    ``python dense_captioning.py <filepath_or_url>``
where <filepath_or_url> is the file path or URL of the image.
"""


import os
import argparse
import requests
from dotenv import load_dotenv
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures, ImageAnalysisResult
from azure.core.credentials import AzureKeyCredential
import spacy
nlp = spacy.load('en_core_web_sm')


def create_dense_captions(filepath_or_url: str) -> ImageAnalysisResult:
    """
    Generates keyword captions of images using Azure's dense captioning technology.

    Args:
    -----
    filepath_or_url : ``str``
        The file path or URL of the image.

    Returns:
    --------
    ``ImageAnalysisResult``
        The result of the image analysis.

    Notes:
    ------
    1. The function requires the following environment variables to be set:
            - AZURE_VISION_ENDPOINT: The endpoint of the Azure Vision service.
            - AZURE_VISION_KEY_1: The key for the Azure Vision service.
    2. The function uses the Azure Cognitive Services SDK to interact with the Azure Vision service.
    3. The function returns the result of the image analysis, which includes the dense captions and metadata.

    Example:
    --------
    >>> response = create_dense_captions("image.jpg")
    >>> print(response.dense_captions.list)
    ... # Prints the dense captions of the image.

    Author: ``@ChinaiArman``
    """
    # Load environment variables.
    load_dotenv()
    endpoint = os.getenv('AZURE_VISION_ENDPOINT')
    key = os.getenv('AZURE_VISION_KEY_1')
    if not endpoint:
        print("Error: Missing environment variable 'AZURE_VISION_ENDPOINT'.")
        print("Please ensure the .env file is present and this variable is declared.")
        return
    if not key:
        print("Error: Missing environment variable 'AZURE_VISION_KEY'.")
        print("Please ensure the .env file is present and this variable is declared.")
        return

    # Create an Image Analysis client.
    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    # Load image and convert to 'bytes' object.
    try: 
        with open(filepath_or_url, "rb") as f:
            image_data = f.read()
    except:
        try:
            image_data = requests.get(filepath_or_url).content
        except:
            print(f"Error: Invalid Filepath or URL")
            return

    # Call dense captioning model to create keyword captions.
    response = client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.DENSE_CAPTIONS],
        gender_neutral_caption=True,
    )
    return response


def normalize_dense_caption_response(response: ImageAnalysisResult) -> list:
    """
    Generates a list of normalized keywords from the dense captioning response.

    Args:
    -----
    response : ``ImageAnalysisResult``
        The response from Azure's dense captioning model.

    Returns:
    --------
    ``list``
        A list of normalized keywords extracted from the dense captioning response.

    Notes:
    ------
    1. The function extracts the keywords from the dense captioning response.
    2. The function filters the keywords based on a confidence threshold of 0.8.

    Example:
    --------
    >>> keywords_list = normalize_dense_caption_response(response)
    >>> print(keywords_list)
    ... # Prints the list of normalized keywords extracted from the dense captioning response.

    Author: ``@nataliecly``
    """
    if response.dense_captions is not None and response.dense_captions.list:
        keywords = [caption.text for caption in response.dense_captions.list if caption.confidence > 0.8]
        return keywords


def main() -> None:
    """
    Main function to run the dense captioning model.

    Args:
    -----
    None.

    Returns:
    --------
    None.

    Notes:
    ------
    1. The function defines a console parser and adds arguments.
    2. The function calls the Azure dense captioning model with the provided image file path or URL.
    3. The function prints the dense caption results to the console.

    Example:
    --------
    >>> python dense_captioning.py "image.jpg"
    ... # Prints the dense captions of the image.

    @Author: ``@ChinaiArman``
    """
    # Define console parser and add arguments.
    parser = argparse.ArgumentParser(description="Generates keyword captions of images using Azure's dense captioning technology.")
    parser.add_argument("filepath_or_url", action="store", help="An image file path or URL")
    args = parser.parse_args()

    # Call azure dense captioning model.
    response = create_dense_captions(args.filepath_or_url)

    # Print dense caption results to the console.
    print("Image analysis results:")
    print("\tDense Captions:")
    if response is not None:
        if response.dense_captions is not None and response.dense_captions.list:
            for caption in response.dense_captions.list:
                print(f"   '{caption.text}', {caption.bounding_box}, Confidence: {caption.confidence:.4f}")
        print(f"\tImage height: {response.metadata.height}")
        print(f"\tImage width: {response.metadata.width}")
        print(f"\tModel version: {response.model_version}")
    else:
        print("\tNo captions generated.")

    # Extract and print normalized keywords from dense caption response.
    print("\nNormalized Keywords:")
    keywords_list = normalize_dense_caption_response(response)
    print(keywords_list)

if __name__ == "__main__":
    main()
