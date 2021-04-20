import os
import json
from random import choice, randint, sample
from datetime import datetime
import crud, api
from model import connect_to_db, db, Stock, Stockprice
from server import app, bcrypt

connect_to_db(app, echo=False)
db.session.query(Stockprice).delete()
db.session.commit()
db.create_all()

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
