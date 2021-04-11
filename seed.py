
# import relevant libraries and functions

import os
import json
from random import choice, randint, sample
from datetime import datetime
import crud
from model import connect_to_db, db
from server import app

os.system('dropdb stocks')
os.system('createdb stocks')

connect_to_db(app, echo=False)
db.create_all()

# load stock data from JSON file
# There are 20 stocks

with open('data/stocks.json') as f:
    stock_data = json.loads(f.read())

#check model.py to make sure it's consistent
stocks_in_db = []
for stock in stock_data:
    symbol, name, description, industry, asset_type = (
    stock['Symbol'],
    stock['Name'],
    stock['Description'],
    stock['Industry'],
    stock['AssetType'],
    )

db_stock = crud.create_stock(symbol, name, description, industry, asset_type)
stocks_in_db.append(db_stock)

#Create the 10 test users
with open('data/users.json') as f:
    user_data = json.loads(f.read())

users_in_db = []

for user in user_data:
    print(user)
    print(type(user))
    fname, lname, username, image_url, about = (
        user['fname'],
        user['lname'],
        user['username'],
        user['image_url'],
        user['about']
    )
    email = f'{username}@gmail.com'
    password = 'test'

    db_user = crud.create_user(username,fname,lname,password,image_url,about)
    users_in_db.append(db_user)

    if user['username'] == 'gigi':
        db_user.favorites.extend(stocks_in_db)
    else:
        # Favorite 5 stocks
        favorite_list = sample(stocks_in_db, 5)
        for stock in favorite_list:
            db_user.favorites.append(stock)

db.session.commit()
