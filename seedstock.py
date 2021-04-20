
import os
import json
from random import choice, randint, sample
from datetime import datetime
import crud, api
from model import connect_to_db, db
from server import app

os.system('dropdb stocks')
os.system('createdb stocks')

connect_to_db(app, echo=False)
db.create_all()

#STOCK TABLE
stocks_in_db = []
stockprices_in_db = []

fundamental_data = api.get_fundamentals()
print(fundamental_data)

for stock in fundamental_data:
    symbol, name, description, industry, asset_type, currency, employees = (
        stock['Symbol'],
        stock['Name'],
        stock['Description'],
        stock['Industry'],
        stock['AssetType'],
        stock['Currency'],
        stock['FullTimeEmployees'],
        )
    
    db_stock = crud.create_stock(symbol, name, 
                description, industry, 
                asset_type, currency, employees)
    stocks_in_db.append(db_stock)
    print(stocks_in_db)

#STOCK PRICE TABLE
stockprices_in_db = []
price_data = api.get_stockprice()

for price in price_data:
    symbol, openprice, high, low, closeprice, volume, date = (
        price['01. symbol'],
        float(price['02. open']),
        float(price['03. high']),
        float(price['04. low']),
        float(price['05. price']),
        int(price['06. volume']),
        price['07. latest trading day']
        )
    
    stock_select =  Stock.query.filter(Stock.symbol == symbol).first()
    stock_id = stock_select.id
    db_stockprice = crud.create_stockprice(stock_id, openprice, high, low, closeprice, volume, date)
    stockprices_in_db.append(db_stockprice)

#STOCK DETAIL TABLE==========
symbol = 'PYPL'
stockdetails_in_db = []
stock_details_data = api.get_stock_details(symbol)

stock_id = Stock.query.filter(Stock.symbol == symbol).first().id

(logo, cik, country, industry, marketcap, employees, phone, ceo, url,
    description, exchange, name, symbol, hq_address, hq_state, hq_country, tags, similar)=(
        stock_details_data["logo"],
      stock_details_data["cik"],
      stock_details_data["country"], 
      stock_details_data["industry"],
      stock_details_data["marketcap"],
      stock_details_data["employees"],
      stock_details_data["phone"],
      stock_details_data["ceo"],
      stock_details_data["url"], 
      stock_details_data["description"],
      stock_details_data["exchange"],
      stock_details_data["name"],
      stock_details_data["symbol"],
      stock_details_data["hq_address"],
      stock_details_data["hq_state"],
      stock_details_data["hq_country"],
      stock_details_data["tags"],
      stock_details_data["similar"]
        )

db_stockdetail = crud.create_stockdetail(stock_id, logo, cik, country, industry, marketcap, employees, phone, ceo, url,
                    description, exchange, name, symbol, hq_address, hq_state, hq_country)
stockdetails_in_db.append(db_stockdetail)
