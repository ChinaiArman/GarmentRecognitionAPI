"""
API data aggregation module used for aggregating data from multiple API sources.
"""

import aiohttp
import asyncio
import pandas as pd
import os
import json


HTTP_SUCCESS_CODE = 200


async def get_asos_data(session, page, category):
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


async def get_hm_data(session, page, category):
    """
    Gets JSON data from api source with single HTTP request.
    """
    api_url = "https://apidojo-hm-hennes-mauritz-v1.p.rapidapi.com/products/list"
    api_params = {
        "country": "us",
        "lang": "en",
        "currentpage": page,
        "pagesize": "30",
        "categories": category,
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
        # print(json.dumps(json_dict, indent=2))
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
    Writes data from API calls to CSV file.
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


async def process_requests(
    async_get_request, write_to_csv, pages=[""], categories=[""]
):
    """
    Executes multiple asynchronous HTTP requests.
    """
    # Use following line for handling rate limiting on certain APIs by setting connection limit
    connector = aiohttp.TCPConnector(limit_per_host=1)
    async with aiohttp.ClientSession(connector=connector) as session:
        async_coroutines = [
            async_get_request(session, page, category)
            for category in categories
            for page in pages
        ]

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
    asos_offset = [str(num) for num in range(0, 48 * 8, 48)]
    await process_requests(get_asos_data, write_asos_data, asos_offset)

    # Get data from H&M
    hm_pages = [str(num) for num in range(1, 7)]
    hm_categories = ["men_all", "ladies_all"]
    await process_requests(get_hm_data, write_hm_data, hm_pages, hm_categories)


if __name__ == "__main__":
    asyncio.run(main())
