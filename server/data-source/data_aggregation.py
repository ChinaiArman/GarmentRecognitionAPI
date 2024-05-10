"""
API data aggregation module used for aggregating data from multiple API sources.
"""

import aiohttp
import asyncio
import pandas as pd
import os
import json

HTTP_SUCCESS_CODE = 200


async def get_json_data(session, http_variables, offset, category):
    """
    Gets JSON data from api source with single HTTP request.
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
        # print(json.dumps(json_dict, indent=2))
        return json_dict
    else:
        print(f"Request failed with status code: {response.status}")
        return None


def write_asos_data(responses):
    """
    Writes data from ASOS API calls to CSV file.
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
    df_merged.to_csv("server/data-source/data-files/asost.csv", index=False)


def write_hm_data(responses):
    """
    Writes data from H&M API calls to CSV file.
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
    df_merged.to_csv("server/data-source/data-files/hmt.csv", index=False)


async def process_requests(write_to_csv, http_variables):
    """
    Executes multiple asynchronous HTTP requests.
    """
    # Use following line for handling rate limiting on certain APIs by setting connection limit
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
    Drives the program.
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
