
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
top_stocks = ['paypal', 'hilton', 'pinterest', 'twilio', 'wayfair', 
            'microsoft', 'ups', 'bankofamerica', 'adobe', 'spotify', 
            'disney', 'facebook', 'sonos', 'zoom', 'etsy', 'tesla', 
            'container store', 'lBrands', 'ford', 'walgreens']

with open('data/stocks.json') as f:
    stock_data = json.loads(f.read())

#create stocks, and store them in a list
stocks_in_db = []
for stock in stock_data:
    symbol, company_name, description, industry, asset_type, ipo_date, 
    current_price, ipo_price = (
    stock['Symbol'],
    stock['Name'],
    stock['Description'],
    stock['Industry'],
    stock['AssetType'],
    stock['IPO_Date'],
    stock['Price'],
    stock['IPO_Price']
    )

db_stock = crud.create_stock(stock_id, symbol, company_name, 
                description, industry, 
                asset_type, ipo_date, 
                current_price, ipo_price)
stocks_in_db.append(db_stock)

# Create 5 test users (MVP)
with open('data/users.json') as f:
    user_data = json.loads(f.read())

users_in_db = []

for user in user_data:

    username, fname, lname, image_url, city, dob, about = (
        user['username'],
        user['fname'],
        user['lname'],
        user['image_url'],
        user['city'],
        user['dob'],
        user['about']
    )

    email = f'{username}@gmail.com'
    password = 'test'

    db_user = crud.create_user(username,fname,lname,image_url,city,dob,about)
    users_in_db.append(db_user)

db.session.commit()
