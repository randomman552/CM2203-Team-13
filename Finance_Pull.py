from functools import lru_cache

import requests
import ast
import os

url = "https://alpha-vantage.p.rapidapi.com/query"
headers = {
    'x-rapidapi-key': os.environ.get("rapidapi-key", ""),
    'x-rapidapi-host': "alpha-vantage.p.rapidapi.com"
}


def data_check(content_dict):
    """
    Function to check content dict contains valid data.
    Will raise exceptions otherwise:
        LookupError - Data was not found or does not exist
        RuntimeError - We encountered an API limit
    """
    if content_dict is None or len(content_dict) == 0:
        raise LookupError("Data not found")
    if "message" in content_dict:
        raise RuntimeError("API limit reached")


@lru_cache(maxsize=10)
def Apigenfetch(stockname):
    querystring = {"function": "GLOBAL_QUOTE", "symbol": stockname}
    response = requests.request("GET", url, headers=headers, params=querystring)
    responsedict = response.__dict__['_content']
    dict_str = responsedict.decode("UTF-8")
    contentdict = ast.literal_eval(dict_str).get("Global Quote")

    data_check(contentdict)
    return contentdict


@lru_cache(maxsize=10)
def Apihistfetch(stockname):
    querystring = {"function": "TIME_SERIES_DAILY", "symbol": stockname, "outputsize": "full"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    responsedict = response.__dict__['_content']
    dict_str = responsedict.decode("UTF-8")
    contentdict = ast.literal_eval(dict_str).get("Time Series (Daily)")

    data_check(contentdict)
    return contentdict


@lru_cache(maxsize=10)
def Apioverfetch(stockname):
    querystring = {"function": "OVERVIEW", "symbol": stockname}
    response = requests.request("GET", url, headers=headers, params=querystring)
    responsedict = response.__dict__['_content']
    dict_str = responsedict.decode("UTF-8")
    contentdict = ast.literal_eval(dict_str)

    data_check(contentdict)
    return contentdict


def stock_page(stockname):
    a = Apioverfetch(stockname)
    b = Apigenfetch(stockname)

    try:
        c = {**a, **b}
    except RuntimeError:
        return RuntimeError
    else:
        return c
