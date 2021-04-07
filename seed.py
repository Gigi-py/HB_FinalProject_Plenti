
# import relevant libraries and functions

import os
import json
from random import choice, randint, sample
from datetime import datetime
import crud
import model
from faker import Faker
from model import connect_to_db, db
from server import app

os.system('dropdb stocks')
os.sytem('creatdb stocks')

connect_to_db(app, echo=False)
db.create_all()

#load stock data from JSON file
#There are 20 stocks
with open('data/stocks.json') as f:
    stock_data = json.loads(f.read())

#check model.py to make sure it's consisten
stocks_in_db = []
for stock in stock_data:
    stock_id, symbol, name, company_overview, sector, asset_type, ipo_date, current_price, ipo_price = (
    stock['stock_id'],
    stock['symbol'],
    stock['company_overview'],
    stock['industry_type'],
    stock['asset_type'],
    stock['ipo_date'],
    stock['current_price'],
    stock['ipo_price']
    )

db_stock = crud.create_stock(stock_id, symbol, name, company_overview, sector, asset_type, ipo_date, current_price, ipo_price)
stocks_in_db.append(db_stock)
