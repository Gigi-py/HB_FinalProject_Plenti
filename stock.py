import requests, json, csv
API_URL = "https://www.alphavantage.co/query"
API_KEY = "J18XE5872X9Y79OQ"

stock_symbols = ['PYPL','HLT', 'PINS', 'TWLO', 'W', 'MSFT', 'UPS', 'BAC', 'ADBE', 'SPOT', 'DIS', 'FB', 'SONO',
        'ZM', 'ETSY', 'TSLA', 'TCS', 'LULU', 'F', 'WBA']

def get_fundamentals():
    fundamental_data = []
    for symbol in stock_symbols:
        data = { "function": "OVERVIEW",
            "symbol": symbol,
            "outputsize" : "full",
            "datatype": "json", 
            "apikey": API_KEY} 

        response = requests.get(API_URL, data) 
        response_json = response.json() 
        fundamental_data.append(serialize_api_obj(response_json))
    return fundamental_data

def serialize_api_obj(api_obj):
    allowed_keys = [
      "Symbol",
      "AssetType",
      "Name",
      "Description", "Industry",
      "Price",
      "IPO_Date"  
    ]

    return {k: v for k, v in api_obj.items() if k in allowed_keys}

def get_price():
    price_data = []
    for symbol in stock_symbols:
        data = { "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "outputsize" : "full",
                "datatype": "json",
                "apikey": API_KEY
                }
    
        response = requests.get(API_URL, data) 
        response_json = response.json() 
        price_data.append(response_json)
    
    return price_data

