"""
Author: ``@ChinaiArman``
Version: ``1.0.0``

Description:
This script is the main entry point for the dense captioning model.
It takes an image file path or URL as an argument and generates keyword captions using Azure's dense captioning technology.

Requirements:
This script requires the following environment variables to be set:
    - AZURE_VISION_ENDPOINT: The endpoint of the Azure Vision service.
    - AZURE_VISION_KEY_1: The key for the Azure Vision service.
The module uses the Azure Cognitive Services SDK to interact with the Azure Vision service.

Usage:
To execute this script from the root directory, run the following command:
    ``python server/dense_captioning_model/main.py <filepath_or_url>``
where <filepath_or_url> is the file path or URL of the image.
"""


import dense_captioning as dc
import argparse


def main():
    """
    Main function to demonstrate the usage of the dense captioning model.

    Args:
    -----
    None.

    Returns:
    --------
    None.

    Notes:
    ------
    1. The function defines a console parser and adds arguments.
    2. This function calls the create_dense_captions function from the dense_captioning module.
    3. The function prints the dense captions and metadata to the console.
    4. The function extracts and prints normalized keywords from the dense caption response.

    Example:
    --------
    >>> python main.py "image.jpg"
    ... # Prints the dense captions and normalized keywords of the image.

    Author: ``@ChinaiArman``
    """
    # Define console parser and add arguments.
    parser = argparse.ArgumentParser(description="Generates keyword captions of images using Azure's dense captioning technology.")
    parser.add_argument("filepath_or_url", action="store", help="An image file path or URL")
    args = parser.parse_args()

    # Call azure dense captioning model.
    response = dc.create_dense_captions(args.filepath_or_url)

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
    keywords_list = dc.normalize_dense_caption_response(response)
    print(keywords_list)


if __name__ == "__main__":
    main()
