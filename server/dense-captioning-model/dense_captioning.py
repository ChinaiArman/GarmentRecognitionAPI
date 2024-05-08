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
    """
    # Load environment variables.
    load_dotenv()
    endpoint = os.getenv('AZURE_VISION_ENDPOINT')
    key = os.getenv('AZURE_VISION_KEY_1')
    if not endpoint:
        print("Missing environment variable 'AZURE_VISION_ENDPOINT'.")
        print("Please ensure the .env file is present and this variable is declared.")
        return
    if not key:
        print("Missing environment variable 'AZURE_VISION_KEY'.")
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
        print("Invalid file path.")
        return
    except OSError:
        try:
            image_data = requests.get(filepath_or_url).content
        except requests.exceptions.RequestException:
            print(f"Invalid URL. Error")
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
