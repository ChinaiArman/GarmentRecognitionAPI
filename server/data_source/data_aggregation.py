"""
Author: ``@cc-dev-65535``
Version: 1.0.0

Description: 
Aggregates data from multiple API sources and writes the data to CSV files. 

Requirements:
This module requires the installation of the pandas library.
This module requires the installation of the aiohttp library.
API keys should be passed in as environment variables and set appropriately.

Usage:
In the command line, execute the module using the command:
    ``python data_aggregation.py``
"""

import aiohttp
import asyncio
import pandas as pd
import os


HTTP_SUCCESS_CODE = 200


async def get_json_data(session, http_variables, offset, category):
    """
    Gets JSON data from api source with a single HTTP request.

    Args:
        session (aiohttp.ClientSession): The aiohttp client session.
        http_variables (dict): The HTTP variables for the HTTP request.
        offset (str): The offset query parameter for the request.
        category (str): The category query parameter for the request.

    Returns:
        dict: The JSON data returned from the API.

    Notes:
        - This function makes an HTTP GET request to the specified API URL.
        - It uses the provided session, HTTP variables, offset, and category.
        - If the response status is 200, it returns the JSON data.
        - Otherwise, it prints an error message and returns None.

    Author: ``@cc-dev-65535``
    """
    if offset is not None:
        param_name = http_variables["offset"]["param_name"]
        http_variables["api_params"][param_name] = offset
    if category is not None:
        param_name = http_variables["categories"]["param_name"]
        http_variables["api_params"][param_name] = category
    response = await session.request(
        method="GET",
        url=http_variables["api_url"],
        params=http_variables["api_params"],
        headers=http_variables["api_headers"],
        ssl=False,
    )

    if response.status == HTTP_SUCCESS_CODE:
        json_dict = await response.json()
        return json_dict
    else:
        print(f"Request failed with status code: {response.status}")
        return None


def write_asos_data(responses):
    """
    Writes data from ASOS API calls to CSV file.

    Args:
        responses (list): List of JSON responses from ASOS API.

    Returns:
        None

    Notes:
        - This function takes a list of JSON responses from ASOS API calls.
        - It normalizes the JSON data into a pandas DataFrame.
        - It modifies the "imageUrl" column to include the "https://" prefix.
        - It selects specific columns from the DataFrame.
        - It concatenates the DataFrames into a single DataFrame.
        - It writes the merged DataFrame to a CSV file in specified file location.

    Author: ``@cc-dev-65535``
    """
    df_list = []

    for response in responses:
        df = pd.json_normalize(response["products"])
        try:
            df["imageUrl"] = df["imageUrl"].apply(lambda x: f"https://{x}")
        except KeyError:
            continue
        df = df[["id", "name", "colour", "brandName", "imageUrl"]]
        df_list.append(df)
    df_merged = pd.concat(df_list)
    df_merged.to_csv("server/data-source/data-files/asos.csv", index=False)


def write_hm_data(responses):
    """
    Writes data from H&M API calls to CSV file.

    Args:
        responses (list): List of JSON responses from H&M API.

    Returns:
        None

    Notes:
        - This function takes a list of JSON responses from H&M API calls.
        - It normalizes the JSON data into a pandas DataFrame.
        - It modifies the "images" column to extract the base URL.
        - It selects specific columns from the DataFrame.
        - It concatenates the DataFrames into a single DataFrame.
        - It writes the merged DataFrame to a CSV file in specified file location.

    Author: ``@cc-dev-65535``
    """
    df_list = []

    for response in responses:
        df = pd.json_normalize(response["results"])
        try:
            df["images"] = df["images"].apply(lambda x: x[0]["baseUrl"])
        except KeyError:
            continue
        df = df[["code", "name", "defaultArticle.color.text", "images"]]
        df_list.append(df)
    df_merged = pd.concat(df_list)
    df_merged.to_csv("server/data-source/data-files/hm.csv", index=False)


async def process_requests(write_to_csv, http_variables):
    """
    Executes multiple asynchronous HTTP requests and writes the returned data to a CSV file.

    Args:
        write_to_csv (function): The function to write returned API data to CSV file.
        http_variables (dict): The HTTP request variables for the HTTP requests.

    Returns:
        None

    Notes:
        - This function takes a write_to_csv function and HTTP variables.
        - It creates an aiohttp client session.
        - It creates a list of async coroutines for each combination of offset and category.
        - It gathers the responses from the async coroutines.
        - It filters out any invalid HTTP responses.
        - It calls the write_to_csv function with the valid responses.

    Author: ``@cc-dev-65535``
    """
    connector = aiohttp.TCPConnector(limit_per_host=1)
    async with aiohttp.ClientSession(connector=connector) as session:
        async_coroutines = [
            get_json_data(session, http_variables, offset, category)
            for category in http_variables["categories"]["param_list"]
            for offset in http_variables["offset"]["param_list"]
        ]

        responses = await asyncio.gather(*async_coroutines)
        responses_filtered = [
            response for response in responses if response is not None
        ]

    write_to_csv(responses_filtered)


def create_http_variables(
    api_url, api_params=None, api_headers=None, offset=None, categories=None
):
    """
    Creates a dictionary of HTTP variables for HTTP requests.

    Args:
        api_url (str): The URL of the API.
        api_params (dict, optional): The HTTP query parameters. Defaults to None.
        api_headers (dict, optional): The HTTP headers. Defaults to None.
        offset (dict, optional): The offset query parameter name and values. Defaults to None.
        categories (dict, optional): The categories query parameter name and values. Defaults to None.

    Returns:
        dict: The dictionary of HTTP variables (headers, query parameters, etc.).

    Author: ``@cc-dev-65535``
    """
    if api_params == None:
        api_params = {}
    if api_headers == None:
        api_headers = {}
    if offset == None:
        offset = {"param_name": None, "param_list": [None]}
    if categories == None:
        categories = {"param_name": None, "param_list": [None]}
    return {
        "api_url": api_url,
        "api_params": api_params,
        "api_headers": api_headers,
        "offset": offset,
        "categories": categories,
    }


async def main():
    """
    Gets JSON data from multiple API sources.

    Returns:
        None

    Notes:
        - This function is the entry point of the program.
        - It defines the HTTP variables for ASOS API.
        - It calls the process_requests function to get data from ASOS API.
        - It defines the HTTP variables for H&M API.
        - It calls the process_requests function to get data from H&M API.
        - API keys should be passed in as environment variables.
        - This function can be expanded to get data from additional desired APIs.

    Author: ``@cc-dev-65535``
    """
    # Get data from ASOS
    api_url = "https://asos2.p.rapidapi.com/products/v2/list"
    api_params = {
        "store": "US",
        "categoryId": "2623",
        "limit": "48",
        "country": "US",
        "sort": "freshness",
        "currency": "USD",
        "sizeSchema": "US",
        "lang": "en-US",
    }
    api_headers = {
        "X-RapidAPI-Key": os.getenv("RAPID_API_KEY", ""),
        "X-RapidAPI-Host": "asos2.p.rapidapi.com",
    }
    asos_offset = {
        "param_name": "offset",
        "param_list": [str(num) for num in range(0, 48 * 8, 48)],
    }
    http_variables = create_http_variables(
        api_url, api_params, api_headers, asos_offset
    )
    await process_requests(write_asos_data, http_variables)

    # Get data from H&M
    api_url = "https://apidojo-hm-hennes-mauritz-v1.p.rapidapi.com/products/list"
    api_params = {
        "country": "us",
        "lang": "en",
        "pagesize": "30",
    }
    api_headers = {
        "X-RapidAPI-Key": os.getenv("RAPID_API_KEY", ""),
        "X-RapidAPI-Host": "apidojo-hm-hennes-mauritz-v1.p.rapidapi.com",
    }
    hm_offset = {
        "param_name": "currentpage",
        "param_list": [str(num) for num in range(1, 7)],
    }
    hm_categories = {
        "param_name": "categories",
        "param_list": ["men_all", "ladies_all"],
    }
    http_variables = create_http_variables(
        api_url, api_params, api_headers, hm_offset, hm_categories
    )
    await process_requests(write_hm_data, http_variables)


if __name__ == "__main__":
    asyncio.run(main())
