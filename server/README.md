# Garment Recognition API Server

## Overview
This project provides an API for recognizing garments from images and keywords. The API supports searching for garments by image, adding new garments, and editing or deleting existing garments. It leverages multiple models and data processing scripts to perform its tasks.

## Structure
- `server/app.py`: Main application logic for the API server.
- `server/garment_recognizer.py`: Contains the GarmentRecognizer class, which provides methods to interact with the data source and models.
- `server/data_files/`: Contains scripts for interacting with, aggregating, normalizing, and merging data sources.
  - `data_access.py`: Interacts with the data source stored in a CSV file.
  - `data_aggregation.py`: Aggregates data from multiple API sources and writes the data to CSV files.
  - `data_merging.py`: Merges datasets based on image filenames and style IDs.
  - `data_normalization.py`: Normalizes data from different sources to a common format and writes it to a CSV file.
  - `main.py`: Runs the data aggregation and normalization processes.
- `server/dense_captioning_model/`: Contains scripts related to generating keyword captions for images.
  - `dense_captioning.py`: Generates keyword captions using Azure's dense captioning technology.
  - `main.py`: Main entry point for the dense captioning model.
- `server/embedded_model/`: Contains scripts for semantic textual analysis.
  - `semantic_textual_analysis.py`: Contains functions to normalize text embeddings and perform semantic textual analysis.
  - `main.py`: Main entry point to demonstrate the usage of the embedded model.

## Requirements
Ensure you have the required Python libraries installed:
```sh
pip install pandas aiohttp python-dotenv flask flask_cors marshmallow torch transformers
```

## Environment Variables
Ensure the following environment variables are set in a .env file:
```sh
AZURE_VISION_ENDPOINT=your_azure_vision_endpoint
AZURE_VISION_KEY_1=your_azure_vision_key
EMBEDDED_MODEL=your_embedded_model
DATA_SOURCE_FILE=server/data_source/data_files/initial_data.csv
PYTHONPATH=server
```


# VENV Installation Instructions
Start from ```root``` directory.
1. Install VENV
    - ```python3 -m venv .venv```
    - ```cd .venv```
2. Activate VENV Instance:
    - Mac:
        - Activation command: ```source bin/activate```
        - Deactivation command: ```source bin/deactivate```
    - Windows:
        - Activation command: ```Scripts\activate.bat```
        - Deactivation command: ```Scripts\deactivate.bat```
    Your interpreter should now be set to the Virtual Environment instance of python.
    - ```cd ..```
3. Install Packages:
    - ```cd server```
    - Installation command: ```pip install -r requirements.txt```
    - Update command: ```pip freeze > requirements.txt```
4. Test: 
    - ```python app.py``` > Visit port 5000