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

### Libraries
Ensure you have the required Python libraries installed:
```sh
cd server                         # Change to the server directory
pip install -r requirements.txt   # Install the required libraries
```

### Environment Variables
Ensure the following environment variables are set in a .env file:
```sh
AZURE_VISION_ENDPOINT=""    # your_azure_vision_endpoint    
AZURE_VISION_KEY_1=""       # your_azure_vision_key    
AZURE_VISION_KEY_2=""       # your_azure_vision_key
RAPID_API_KEY=""            # your_rapid_api_key
EMBEDDED_MODEL=""           # your_embedded_model
DATA_SOURCE_FILE=""         # your_data_source_file
PYTHONPATH="server"         # Set the PYTHONPATH to "server"
```

## Usage
1. Start the server by running the following command:
```sh
cd ..                   # Return to the root directory
python server/app.py    # Start the server
```
2. Access the API documentation at `http://localhost:5000/` to view the available endpoints and interact with the API.

### Flask Server Deployment (only for the server)
The API server can be deployed to a cloud platform such as Azure or AWS with minimal changes.
1. Ensure that the required environment variables are set in the deployment environment.

2. In app.py, change the initialization of the Flask app (line 29 in `server/app.py`) to the following:
    ```python
    app = Flask(__name__)
    ```

3. In app.py, change the root route of the Flask server (line 330 in `server/app.py`) to the following:
    ```python
    return jsonify("Hello World")
    ```

4. Deploy the server folder to the cloud platform of your choice.