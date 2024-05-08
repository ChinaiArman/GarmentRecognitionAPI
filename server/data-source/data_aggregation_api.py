"""
API access file used for aggregating data from multiple API sources.
"""

import aiohttp
import asyncio
import pandas as pd
import os
import json

HTTP_SUCCESS_CODE = 200


async def get_asos_data(page, session):
    """
    Gets JSON data from api source with single HTTP request.
    """
    api_url = "https://asos2.p.rapidapi.com/products/v2/list"
    api_params = {
        "store": "US",
        "offset": page,
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

    response = await session.request(
        method="GET", url=api_url, params=api_params, headers=api_headers, ssl=False
    )

    if response.status == HTTP_SUCCESS_CODE:
        json_dict = await response.json()
        # print(json.dumps(json_dict, indent=2))
        return json_dict
    else:
        print(f"Request failed with status code: {response.status}")
        return None


async def get_hm_data(page, session):
    """
    Gets JSON data from api source with single HTTP request.
    """
    api_url = "https://apidojo-hm-hennes-mauritz-v1.p.rapidapi.com/products/list"
    api_params = {
        "country": "us",
        "lang": "en",
        "currentpage": page,
        "pagesize": "30",
        "categories": "men_all",
        "concepts": "H&M MAN",
    }
    api_headers = {
        "X-RapidAPI-Key": os.getenv("RAPID_API_KEY", ""),
        "X-RapidAPI-Host": "apidojo-hm-hennes-mauritz-v1.p.rapidapi.com",
    }

    response = await session.request(
        method="GET", url=api_url, params=api_params, headers=api_headers, ssl=False
    )

    if response.status == HTTP_SUCCESS_CODE:
        json_dict = await response.json()
        print(json.dumps(json_dict, indent=2))
        return json_dict
    else:
        print(f"Request failed with status code: {response.status}")
        return None


def write_asos_data(responses):
    """
    Writes data from API calls to CSV file.
    """
    df_list = []
    for response in responses:
        df = pd.json_normalize(response["products"])
        df_list.append(df)

    df_merged = pd.concat(df_list)
    df_merged.to_csv("server/data-source/data-files/asos.csv", index=False)


def write_hm_data(responses):
    """
    Writes data from API calls to CSV file.
    """
    df_list = []
    for response in responses:
        df = pd.json_normalize(response["results"])
        df_list.append(df)

    df_merged = pd.concat(df_list)
    df_merged.to_csv("server/data-source/data-files/hm.csv", index=False)


async def process_requests(pages, async_get_request, write_to_csv):
    """
    Executes multiple asynchronous HTTP requests.
    """
    # Use following line for handling rate limiting on certain APIs by setting connection limit
    # connector = aiohttp.TCPConnector(limit_per_host=1)
    async with aiohttp.ClientSession() as session:
        async_coroutines = [async_get_request(page, session) for page in pages]

        responses = await asyncio.gather(*async_coroutines)
        responses_filtered = [
            response for response in responses if response is not None
        ]

    write_to_csv(responses_filtered)


async def main():
    """
    Drives the program.
    """
    # Get data from ASOS
    asos_offset = ["0", "48", "96"]
    await process_requests(asos_offset, get_asos_data, write_asos_data)

    # Get data from H&M
    hm_pages = ["0", "1", "2", "3"]
    await process_requests(hm_pages, get_hm_data, write_hm_data)


if __name__ == "__main__":
    asyncio.run(main())
