# Data Source 
This folder contains the data files and modules for accessing, aggregating, merging, and normalizing the data.

## File Explanations
- the **data_files** folder
    
    This folder contains the CSV files that have data pulled from clothing data API's. It includes `asos.csv`, `free_clothes.csv`, and `hm.csv`. 

- ```data_acess.py```

    This file contains the Database class along with its methods to interact with the CSV data source. 
   
    Methods in the Database class include `get_data_frame`, `get_item_by_id`, ` get_id_keyword_description`, `delete_row`, `add_row`, `edit_row` and `write_to_csv`.

- ```data_aggregation.py```

    This file is the data aggregation module which aggregates data from multiple API sources and writes the data to its respective CSV files. 

    Functions in this module include `get_json_data`, `write_asos_data`, `write_hm_data`, `process_requests`, and `create_http_variables`.

- ```data_merging.py```

    This file is the data merging module which combines all the datasets together into a new CSV file. 

    The function in this module include the `merge_datasets`.

- ```data_normalization.py```

    This file is the data normalization module which normalizes data from multiple sources into one common format and writes them to a new CSV file.

    Functions in this module include `merge_description_columns`, `rename_columns`, `drop_columns`, `normalize_dataframe`, `merge_dataframes`, `generate_keywords`, and `write_dataframe_to_csv`.

- ```data.csv```

    This CSV file contains all the data after it's been aggregated and normalized. This serves as the main data source for the API. 

- ```data_small.csv```

    This is a smaller CSV file containing about less than half of the data in the main `data.csv` file. Its purpose was to test the running of the API on slower, less-powerful machines.

- ```main.py```

    This main file runs the processes for data aggregation and normalization.


## Requirements

### Libraries
Ensure you have the required Python libraries installed:
```sh
pip install -r requirements.txt
```

### Environment Variables
Ensure the following environment variables are set in a .env file:
```sh
AZURE_VISION_ENDPOINT=your_azure_vision_endpoint
AZURE_VISION_KEY_1=your_azure_vision_key
AZURE_VISION_KEY_2=your_azure_vision_key
RAPID_API_KEY=your_rapid_api_key
DATA_SOURCE_FILE=your_data_source_file
PYTHONPATH=server
```

## Usage
This file <b>should NOT be run after the initial setup</b>. The data aggregation and normalization processes should be run only once to generate the main data source file.

To run the data aggregation and normalization processes, execute the following command:
```sh
python server/data_source/main.py
```