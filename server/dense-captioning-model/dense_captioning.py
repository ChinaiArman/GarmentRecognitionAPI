"""
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
    Generate dense captions for an image given a local file path or a URL.
    """
    # Load environment variables.
    load_dotenv()
    endpoint = os.getenv('AZURE_VISION_ENDPOINT')
    key = os.getenv('AZURE_VISION_KEY')
    if not endpoint:
        print("Missing environment variable 'AZURE_VISION_ENDPOINT'.")
        print("Please ensure the .env file is present and this variable is declared.")
        exit(1)
    if not key:
        print("Missing environment variable 'AZURE_VISION_KEY'.")
        print("Please ensure the .env file is present and this variable is declared.")
        exit(1)

    # Create an Image Analysis client.
    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    # Determine if the input is a URL or a local file path and load the image data.
    if filepath_or_url.startswith('http://') or filepath_or_url.startswith('https://'):
        try:
            image_data = requests.get(filepath_or_url).content
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve image from URL: {e}")
            exit()
    else:
        try:
            with open(filepath_or_url, "rb") as f:
                image_data = f.read()
        except FileNotFoundError:
            print("Invalid file path.")
            exit()
        except OSError as e:
            print(f"Error reading the file: {e}")
            exit()

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
    if response.dense_captions is not None and response.dense_captions.list:
        for caption in response.dense_captions.list:
            print(f"   '{caption.text}', {caption.bounding_box}, Confidence: {caption.confidence:.4f}")
    print(f"\tImage height: {response.metadata.height}")
    print(f"\tImage width: {response.metadata.width}")
    print(f"\tModel version: {response.model_version}")
