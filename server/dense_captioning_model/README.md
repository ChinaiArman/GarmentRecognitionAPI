# Dense Captioning Module

## Overview
This module generates keyword captions of images using Azure's dense captioning technology. It analyzes images to produce dense captions along with metadata such as image dimensions and model version. The module uses the Azure Cognitive Services SDK to interact with the Azure Vision service.

## Structure
- `dense_captioning.py`: Contains functions to interact with Azure's dense captioning service and process the image analysis results.
- `main.py`: Serves as the entry point to run the dense captioning model on a given image file path or URL.

## Requirements
Ensure you have the required Python libraries and environment variables set up:

### Libraries
```sh
pip install azure-ai-vision requests python-dotenv
```

## Environment Variables
Ensure the following environment variables are set in a .env file:
```sh
AZURE_VISION_ENDPOINT=your_azure_vision_endpoint
AZURE_VISION_KEY_1=your_azure_vision_key
```