# Data Files Module

## Overview

This module contains various scripts to interact with, aggregate, normalize, and merge data sources for the Odd Fabric Garment Recognition API. It provides the necessary functionalities to process data from multiple sources and prepare it for use by the AI models.

## Structure

- **data_access.py**: Interacts with the data source stored in a CSV file.
- **data_aggregation.py**: Aggregates data from multiple API sources and writes the data to CSV files.
- **data_merging.py**: Merges datasets based on image filenames and style IDs.
- **data_normalization.py**: Normalizes data from different sources to a common format and writes it to a CSV file.
- **main.py**: Runs the data aggregation and normalization processes.

## Requirements

Ensure you have the required Python libraries installed:
```sh
pip install pandas aiohttp python-dotenv