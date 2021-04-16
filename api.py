import requests, json, csv, time
API_URL = "https://www.alphavantage.co/query"
API_KEY = "J18XE5872X9Y79OQ"

# https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=demo
# https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo

stock_symbols = ['PYPL','HLT', 'PINS', 'TWLO', 'W', 'MSFT', 'UPS', 'BAC', 'ADBE', 'SPOT', 'DIS', 'FB', 'SONO',
        'ZM', 'ETSY', 'TSLA', 'TCS', 'LULU', 'F', 'WBA'] #TO DO: call live once feature is set up properly

def get_stockprice():
    """Get stock name info from AA API to store in db """    
    stockprice_data = []
    for symbol in stock_symbols:
        data = { "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "outputsize" : "full",
            "datatype": "json", 
            "apikey": API_KEY} 


        response = requests.get(API_URL, data) 
        response_json = response.json().get('Global Quote')
        print(response_json)
        # if response_json.get('symbol') == None:
        #     time.sleep(60)
        #     print('sleeping')
        #     response = requests.get(API_URL, data)
        #     response_json = response.json()
        stockprice_data.append(serialize_api_price(response_json))
        print('data_append')
        
        return stockprice_data

def serialize_api_price(api_price):
    allowed_keys = [
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
            "apikey": API_KEY} 

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