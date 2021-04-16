
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

#create stocks, and store them in a list
stocks_in_db = []
stockprices_in_db = []

fundamental_data = api.get_fundamentals()
price_data = api.get_stockprice()

print(fundamental_data)
print(price_data)

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

for price in price_data:
    openprice, high, low, closeprice, volumn, date = (
        price['02. open'],
        price['03. high'],
        stock['04. low'],
        stock['05. price'],
        stock['06. volume'],
        stock['07. latest trading day']
        )

    db_stockprice = crud.create_stockprice(open, high, low, price, volume, date)

    stockprices_in_db.append(db_stockprice)
    print(stockprices_in_db)


# Create 5 test users (MVP)
# with open('data/users.json') as f:
#     user_data = json.loads(f.read())

# users_in_db = []

# for user in user_data:

#     username, fname, lname, image_url, city, about = (
#         user['username'],
#         user['fname'],
#         user['lname'],
#         user['image_url'],
#         user['city'],
#         user['about']
#     )

#     email = f'{username}@gmail.com'
#     password = 'test'

#     db_user = crud.create_user(username,fname,lname,image_url,city,about,password)
#     users_in_db.append(db_user)

# db.session.commit()

