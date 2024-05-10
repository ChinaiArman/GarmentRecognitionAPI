"""
Author: ``@ChinaiArman``
Version: 1.0.0

Generates keyword captions of images using Azure's dense captioning technology.
This module requires the following environment variables to be set:
    - AZURE_VISION_ENDPOINT: The endpoint of the Azure Vision service.
    - AZURE_VISION_KEY_1: The key for the Azure Vision service.

The module uses the Azure Cognitive Services SDK to interact with the Azure Vision service.
To execute this module, run the following command:
    ``python dense_captioning.py <filepath_or_url>``
where <filepath_or_url> is the file path or URL of the image.

The module returns the result of the image analysis, which includes the dense captions and metadata.
The dense captions are printed to the console, along with the image height, width, and model version.
"""

import os
import argparse
import requests
from dotenv import load_dotenv
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures, ImageAnalysisResult
from azure.core.credentials import AzureKeyCredential


def create_dense_captions(filepath_or_url: str) -> ImageAnalysisResult:
    """
    Generates keyword captions of images using Azure's dense captioning technology.

    Args:
        filepath_or_url (str): The file path or URL of the image.

    Returns:
        ImageAnalysisResult: The result of the image analysis.

    Notes:
        - The function requires the following environment variables to be set:
            - AZURE_VISION_ENDPOINT: The endpoint of the Azure Vision service.
            - AZURE_VISION_KEY_1: The key for the Azure Vision service.
        - The function uses the Azure Cognitive Services SDK to interact with the Azure Vision service.
        - The function returns the result of the image analysis, which includes the dense captions and metadata.

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
    except FileNotFoundError:
        print("Error: Invalid file path.")
        return
    except OSError:
        try:
            image_data = requests.get(filepath_or_url).content
        except requests.exceptions.RequestException:
            print(f"Error: Invalid URL")
            return

    # Call dense captioning model to create keyword captions.
    response = client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.DENSE_CAPTIONS],
        gender_neutral_caption=True,
    )
    return response


if __name__ == "__main__":
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
