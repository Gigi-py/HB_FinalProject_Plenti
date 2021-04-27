import requests, json, csv, time
import os
API_URL = "https://www.alphavantage.co/query"

AA_API_KEY = os.environ['AA_API_KEY']
POLY_API_KEY = os.environ['POLY_API_KEY']

# https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo
# https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo

stock_symbols = ['PYPL','HLT', 'PINS', 'TWLO', 'W',
 'MSFT', 'UPS', 'BAC', 'ADBE', 'SPOT', 'DIS', 'FB', 'SONO',
        'ZM', 'ETSY', 'TSLA', 'TCS', 'LULU', 'F', 'WBA'] #TO DO: call live once feature is set up properly

def get_stockprice():
    """Get stock name info from AA API to store in db """    
    stockprice_data = []
    for symbol in stock_symbols:
        data = { "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "outputsize" : "full",
            "datatype": "json", 
            "apikey": AA_API_KEY} 

        response = requests.get(API_URL, data) 
        response_json = response.json().get('Global Quote')
        if response_json == None:
            time.sleep(60)
            print('sleeping')
            response = requests.get(API_URL, data)
            response_json = response.json().get('Global Quote')
        stockprice_data.append(serialize_api_price(response_json))
        print('data_append')
        
    return stockprice_data

def serialize_api_price(api_price):
    allowed_keys = ["01. symbol",
      "02. open",
      "03. high",
      "04. low",
      "05. price", 
      "06. volume",
      "07. latest trading day"
    ]

    return {k: v for k, v in api_price.items() if k in allowed_keys}

def get_fundamentals():
    fundamental_data = []
    for symbol in stock_symbols:
        data = { "function": "OVERVIEW",
            "symbol": symbol,
            "outputsize" : "full",
            "datatype": "json", 
            "apikey": AA_API_KEY} 

        response = requests.get(API_URL, data) 
        response_json = response.json() 
        print(response_json)
        if response_json.get('Symbol') == None:
            time.sleep(60)
            print('sleeping')
            response = requests.get(API_URL, data)
            response_json = response.json()
        fundamental_data.append(serialize_api_obj(response_json))
        print('data_append')
    return fundamental_data

def serialize_api_obj(api_obj):
    allowed_keys = [
      "Symbol",
      "AssetType",
      "Name",
      "Description", 
      "Industry",
      "Currency",
      "FullTimeEmployees"  
    ]

    return {k: v for k, v in api_obj.items() if k in allowed_keys}

#POLYGON API=================

def get_stock_details(symbol):
    """Get stock info from POLYGON API to store in db """    

    response = requests.get("https://api.polygon.io/v1/meta/symbols/" + symbol + "/company?&apiKey=" + POLY_API_KEY)
    response_json = response.json()
    
    return response_json

#Create and return new Stockdetail:

# def serialize_api_details(api_details):
#     allowed_keys = [
#       "logo",
#       "listdate",
#       "cik",
#       "country", 
#       "industry",
#       "marketcap",
#       "employees",
#       "phone",
#       "ceo",
#       "url", 
#       "description",
#       "exchange",
#       "name",
#       "symbol",
#       "hq_address",
#       "hq_state",
#       "hq_country",
#       "tags",
#       "similar"]

#     return {k: v for k, v in api_details.items() if k in allowed_keys}

        
def get_news_details(symbol):
    """Get stock news info from POLYGON API to store in db """    
    response = requests.get("https://api.polygon.io/v1/meta/symbols/" + symbol + "/news?perpage=50&page=1&apiKey=" + POLY_API_KEY)
    response_json = response.json()
    
    allowed_keys = [
      "timestamp",
      "title",
      "url",
      "source", 
      "summary",
      "image"
    ]

    return response_json

def get_price_data(symbol, date):
    response = requests.get("https://api.polygon.io/v1/open-close/" + symbol + "/" + date + "?unadjusted=true&apiKey=" + POLY_API_KEY)
    response_json = response.json()
    
    return response_json