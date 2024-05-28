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
cd server                           # Change to the server directory
pip install -r requirements.txt     # Install the required libraries
```

### Environment Variables
Ensure the following environment variables are set in a .env file:
```sh
AZURE_VISION_ENDPOINT=""        # your_azure_vision_endpoint        
AZURE_VISION_KEY_1=""           # your_azure_vision_key
AZURE_VISION_KEY_2=""           # your_azure_vision_key
EMBEDDED_MODEL=""               # your_embedded_model
PYTHONPATH="server"             # Set the PYTHONPATH to "server"
DATA_SOURCE_FILE=""             # your_data_source_file
```

## Usage
1. Run the following command to demonstrate the usage of the embedded model:
```sh
cd ..                                       # Return to the root directory
python server/embedded_model/main.py        # Run the embedded model#
```
