"""
"""

import os
import argparse
import requests
from dotenv import load_dotenv
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures, ImageAnalysisResult
from azure.core.credentials import AzureKeyCredential


def create_dense_captions(filepath: str) -> ImageAnalysisResult:
    """
    """
    # Load environment variables.
    load_dotenv()
    endpoint = os.getenv('AZURE_VISION_ENDPOINT')
    key = os.getenv('AZURE_VISION_KEY')
    if not endpoint or not key:
        print("Missing environment variable 'AZURE_VISION_ENDPOINT' or 'AZURE_VISION_KEY'")
        print("Please ensure the .env file is present and the above environment variables are declared.")
        exit()

    # Create an Image Analysis client.
    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    # Load image and convert to 'bytes' object.
    try: 
        with open(filepath, "rb") as f:
            image_data = f.read()
    except FileNotFoundError:
        print("Invalid file path.")
        exit()
    except OSError:
        image_data = requests.get(filepath).content

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
    parser.add_argument("file", action="store", help="An image file")
    args = parser.parse_args()

    # Call azure dense captioning model.
    response = create_dense_captions(args.file)

    # Print dense caption results to the console.
    print("Image analysis results:")
    print("\tDense Captions:")
    if response.dense_captions is not None:
        for caption in response.dense_captions.list:
            print(f"   '{caption.text}', {caption.bounding_box}, Confidence: {caption.confidence:.4f}")
    print(f"\tImage height: {response.metadata.height}")
    print(f"\tImage width: {response.metadata.width}")
    print(f"\tModel version: {response.model_version}")
