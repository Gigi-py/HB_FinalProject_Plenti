import os
import json
from random import choice, randint, sample
from datetime import datetime
import crud, api
from model import connect_to_db, db
from server import app


connect_to_db(app, echo=False)

stockprices_in_db = []

price_data = api.get_stockprice()

print(price_data)

for price in price_data:
    openprice, high, low, closeprice, volume, date = (
        float(price['02. open']),
        float(price['03. high']),
        float(price['04. low']),
        float(price['05. price']),
        int(price['06. volume']),
        price['07. latest trading day']
        )
    
    #stockprice = Stockprice(stock_id=stock_id, openprice = openprice, high = high, low = low, closeprice = closeprice, volume = volume, date = date)

    db_stockprice = crud.create_stockprice(openprice, high, low, closeprice, volume, date)

    stockprices_in_db.append(db_stockprice)
    print(stockprices_in_db)