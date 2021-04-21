
import os
import json
from random import choice, randint, sample
from datetime import datetime
import crud, api
from model import connect_to_db, db, User, Stock, Stockprice, Stockdetail, UserFavorite, Plan, Blog, Subscription, Stock_in_Subscription, Event, Comment
from server import app

os.system('dropdb stocks')
os.system('createdb stocks')

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
    
    db_stockprice = crud.create_stockprice(symbol, openprice, high, low, closeprice, volume, date)
    stockprices_in_db.append(db_stockprice)

#STOCK DETAIL TABLE==========
stockdetails_in_db = []
stock_details_data = api.get_stock_details(symbol)

for stock_detail in stock_details_data:
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

db_stockdetail = crud.create_stockdetail(symbol, logo, cik, country, industry, marketcap, employees, phone, ceo, url,
                    description, exchange, name, hq_address, hq_state, hq_country)
stockdetails_in_db.append(db_stockdetail)

#SEED USER TABLE=================
with open('data/users.json') as f:
    user_data = json.loads(f.read())

users_in_db = []

for user in user_data:

    username, fname, lname, avatar, address = (
        user['username'],
        user['fname'],
        user['lname'],
        user['avatar'],
        user['address']
    )

    email = f'{username}@gmail.com'
    password = 'test'

    db_user = crud.create_user(app, username, fname, lname, email, password, avatar, address)
    users_in_db.append(db_user)

db.session.commit()

#SEED PLAN==========
plans = [{
    "name": "starter",
    "stocks_per_month": 10,
    "investment_per_month": 20
    },
    {
    "name": "pro",
    "stocks_per_month": 10,
    "investment_per_month": 50
    },
    {
    "name": "premium",
    "stocks_per_month": 10,
    "investment_per_month": 100
    }]

plans_in_db = []
for plan in plans:
    name, stocks_per_month, investment_per_month = (plan['name'], plan['stocks_per_month'], plan['investment_per_month'])
    db_plan = crud.create_plan(name, stocks_per_month, investment_per_month)
    plans_in_db.append(db_plan)

db.session.commit()

#SEED SUBSCRIPTION===========
subscriptions_in_db = []
user_name = users_in_db[0].username
plan_id = plans_in_db[0].id
subscription_start_timestamp = datetime.utcnow()
subscription_end_timestamp = datetime.utcnow()
db_subscription = crud.create_subscription(user_name, plan_id, subscription_start_timestamp, subscription_end_timestamp)
subscriptions_in_db.append(db_subscription)

db.session.commit()

