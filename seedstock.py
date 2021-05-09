
import os
import json
from random import choice, randint, sample
from datetime import datetime
import crud, api
from model import connect_to_db, db, User, Stock, Stockprice, Stockdetail, Stocknews, UserFavorite, Plan, Blog, Subscription, Stock_in_Subscription, Event, Comment
from server import app

db.session.query(Stock).delete()
connect_to_db(app, echo=False)
db.create_all()

#STOCK TABLE==============
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

