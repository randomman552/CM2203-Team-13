import requests
import ast

url = "https://alpha-vantage.p.rapidapi.com/query"
headers = {
    'x-rapidapi-key': "f9230c8520msh42bb7e7174822d7p10904bjsn6d131581edfa",
    'x-rapidapi-host': "alpha-vantage.p.rapidapi.com"
    }

def Apigenfetch(stockname):
    querystring = {"function":"GLOBAL_QUOTE","symbol":stockname}
    response = requests.request("GET", url, headers=headers, params=querystring)
    responsedict = (response.__dict__)['_content']
    dict_str = responsedict.decode("UTF-8")
    contentpredict = ast.literal_eval(dict_str)
    contentdict = contentpredict['Global Quote']
    return contentdict

def Apihistfetch(stockname):
    querystring = {"function":"TIME_SERIES_DAILY","symbol":stockname,"outputsize":"full"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    responsedict = (response.__dict__)['_content']
    dict_str = responsedict.decode("UTF-8")
    contentpredict = ast.literal_eval(dict_str)
    contentdict = contentpredict['Time Series (Daily)']
    return contentdict

def Apioverfetch(stockname):
    querystring = {"function":"OVERVIEW","symbol":stockname}
    response = requests.request("GET", url, headers=headers, params=querystring)
    responsedict = (response.__dict__)['_content']
    dict_str = responsedict.decode("UTF-8")
    contentdict = ast.literal_eval(dict_str)
    return contentdict

def calcCloseAverage(dictOfDays):
    average = 0
    for x in dictOfDays:
        average += float(dictOfDays[x]['4. close'])
    average = average/len(dictOfDays)
    return average