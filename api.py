import requests, json, csv, time
import os
API_URL = "https://www.alphavantage.co/query"

AA_API_KEY = os.environ['AA_API_KEY']
POLY_API_KEY = os.environ['POLY_API_KEY']
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

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
    print("\t", "*"*20, "IN api.py GET PRICE DATA fn \nsymbol = ", symbol)
    
    print("\tmaking get request to external api...")
    response = requests.get("https://api.polygon.io/v1/open-close/" + symbol + "/" + date + "?unadjusted=true&apiKey=" + POLY_API_KEY)
    response_json = response.json()
    # print(f"response_json: \n{response_json}")
    
    return response_json

def get_geocode(symbol):
    print("\t", "*"*20, "IN api.py GET GEOLOCATION DATA fn \nsymbol = ", symbol)
    
    response = requests.get("https://api.polygon.io/v1/meta/symbols/" + symbol + "/company?&apiKey=" + POLY_API_KEY)
    response_json = response.json()
    hq_address = response_json["hq_address"]

    geo_request = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + hq_address + "&key=AIzaSyCGBE_HYW8qt3BnNFW3gKoYb2GWHDThAt8")
    geo_request_json = geo_request.json()
    
    #getting the LatLng of the location
    latlng = geo_request_json['results'][0]['geometry']['location']

    return latlng
    # response_json = response.json()

