# Embedded Model Module

## Overview
This module contains functions to normalize text embeddings and perform semantic textual analysis. It leverages pre-trained transformer models to generate text embeddings and uses these embeddings to find semantic similarities between text data. The module also integrates with the dense captioning model to analyze images and generate keyword captions.

## Structure
- `semantic_textual_analysis.py`: Contains functions to load models, normalize embeddings, perform semantic analysis, and integrate with the dense captioning model.
- `main.py`: Serves as the entry point to demonstrate the usage of the embedded model for comparing images with items in the database.

## Requirements
Ensure you have the required Python libraries and environment variables set up:

### Libraries
```sh
pip install torch transformers pandas python-dotenv
```

## Environment Variables
Ensure the following environment variables are set in a .env file:
```sh
AZURE_VISION_ENDPOINT=your_azure_vision_endpoint
AZURE_VISION_KEY_1=your_azure_vision_key
EMBEDDED_MODEL=your_embedded_model
PYTHONPATH=server
```