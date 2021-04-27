from pprint import pprint

import requests
import ast

url = "https://alpha-vantage.p.rapidapi.com/query"
headers = {
    'x-rapidapi-key': "d63b107930msh667bcccd45e4cc6p158fe8jsn4bc129f88ec1",
    # Watson: f9230c8520msh42bb7e7174822d7p10904bjsn6d131581edfa
    # Hayes: d63b107930msh667bcccd45e4cc6p158fe8jsn4bc129f88ec1
    # Hayes2: dbd23c2e57msh0de22e14f38eda0p1c3f84jsn621b3a32ceab
    'x-rapidapi-host': "alpha-vantage.p.rapidapi.com"
}
gen_fetch = {}


def Apigenfetch(stockname):
    querystring = {"function": "GLOBAL_QUOTE", "symbol": stockname}
    response = requests.request("GET", url, headers=headers, params=querystring)
    responsedict = response.__dict__['_content']
    dict_str = responsedict.decode("UTF-8")
    contentpredict = ast.literal_eval(dict_str)
    try:
        contentdict = contentpredict['Global Quote']
    except:
        print("ERROR: Apigenfetch API limit reached, cannot request for a minute.")
        return {}
    else:
        return contentdict


def Apihistfetch(stockname):
    querystring = {"function": "TIME_SERIES_DAILY", "symbol": stockname, "outputsize": "full"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    responsedict = response.__dict__['_content']
    dict_str = responsedict.decode("UTF-8")
    contentpredict = ast.literal_eval(dict_str)
    try:
        contentdict = contentpredict['Time Series (Daily)']
    except:
        print("ERROR: Apihistfetch API limit reached, cannot request for a minute.")
        return {}
    else:
        return contentdict


def Apioverfetch(stockname):
    querystring = {"function": "OVERVIEW", "symbol": stockname}
    response = requests.request("GET", url, headers=headers, params=querystring)
    responsedict = response.__dict__['_content']
    dict_str = responsedict.decode("UTF-8")
    contentdict = ast.literal_eval(dict_str)
    try:
        contentdict["Symbol"]
    except:
        print("ERROR: Apioverfetch API limit reached, cannot request for a minute.")
        return {}
    else:
        return contentdict


def calcCloseAverage(dictOfDays):
    average = 0
    for x in dictOfDays:
        average += float(dictOfDays[x]['4. close'])
    average = average / len(dictOfDays)
    return average


def stock_page(stockname):
    a = Apioverfetch(stockname)
    b = Apigenfetch(stockname)
    try:
        c = {**a, **b}
    except a == {} or b == {}:
        return {"errorAPI": "API Limit reached, try again in a minute"}
    else:
        return c
