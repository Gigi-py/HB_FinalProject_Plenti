
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

#Create the 10 users
with open('data/users.json') as f:
    user_data = json.loads(f.read())

users_in_db = []

for user in user_data:
    fname, lname, username, image_url, about = (
        u['fname'],
        u['lname'],
        u['username'],
        u['image_url'],
        u['about']
    )
    email = f'{username}@username.com'
    password = 'test'
    db_user = crud.create_user(username,fname,lname,email,password,image_url,about)
    users_in_db.append(db_user)

    if u['username'] == 'gigi':
        db_user.favorites.extend(stocks_in_db)
    else:
        # Favorite 5 stocks
        favorite_list = sample(stocks_in_db, 5)
        for r in r_list:
            db_user.favorites.append(r)

db.session.commit()
