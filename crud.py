
from server import connect_to_db, Bcrypt
from model import User, Stock, Stockprice, Stockdetail, UserFavorite, Plan, Blog, Subscription, Stock_in_Subscription, Event, Comment, connect_to_db, db
import datetime
import api
import requests
import csv
import json
import os
import secrets

API_KEY = "J18XE5872X9Y79OQ"
# USER INFO ==================================
#Create and return a new user:
def create_user(app, username, fname, lname, email, password, avatar, address):
    """Return list of user objects"""
    bcrypt = Bcrypt(app)
    hashed_password = bcrypt.generate_password_hash(password).decode('UTF-8')
    user = User(username = username, fname = fname, lname = lname,  
                email = email, password = hashed_password, avatar=avatar, address=address)
    
    db.session.add(user)
    db.session.commit()

    return user

def check_password(email, password):
    """ Check password and email for logging in"""

    user = get_user_by_email(email)
   
    if not user:
        return False
    if user.password == password:
        return True
    else:
        return False

# STOCK INFO ================================

def get_all_stock_symbols():
    """Get stock name info from AA API to store in db """
    url = 'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey='+ API_KEY
    res = requests.get(url) # double check this line, might be a duplicate to line 65
    decoded = res.content.decode('utf-8')

    csv_read = csv.reader(decoded.splitlines(), delimiter=',')
    all_stocks = list(csv_read)
    
    return all_stocks

# def save_stocks(all_stocks):
#     """save all stocks (names, symbol etc.. ) in the database from AA API  """
#     sample_stocks = ['PYPL','HLT', 'PINS', 'TWLO', 'W', 'MSFT', 'UPS', 'BAC', 'ADBE', 'SPOT', 'DIS', 'FB', 'SONO', 'ZM', 'ETSY', 'TSLA', 'TCS', 'LULU', 'F', 'WBA']
#     count = 0
#     for stock in all_stocks:
#         print(stock)
#         if count != 0:
#             if stock[0] in sample_stocks:
#                 stockInfo = Stock(symbol = stock[0], stock_name=stock[1], exchange=stock[2],asset_type=stock[3],ipo_date=stock[4], sample = True)
#             else:
#                 stockInfo = Stock(symbol = stock[0], stock_name=stock[1], exchange=stock[2],asset_type=stock[3],ipo_date=stock[4])
       
#             db.session.add(stockInfo)
#             db.session.commit()
#         count += 1

#     return "Finished adding all stock symbols"

#Create and add a new stock to the database:
def create_stock(symbol, name, 
                description, industry, 
                asset_type, currency, 
                employees):

    stock = Stock(symbol = symbol, name = name, 
                description = description, industry = industry, 
                asset_type = asset_type, currency = currency, 
                employees = employees)
    db.session.add(stock)
    db.session.commit()

    return stock

#PRICE INFO++++++++++++++++++
def create_stockprice(symbol, openprice, high, low, closeprice, volume, date):
    
    stockprice = Stockprice(symbol=symbol, openprice = openprice, high = high, low = low, closeprice = closeprice, volume = volume, date = date)

    db.session.add(stockprice)
    db.session.commit()

    return stockprice


#Create and return new Stockdetail:
def get_stockdetail(symbol):
    #calling live API data from Polygon on each stock symbol
    stock_details_data = api.get_stock_details(symbol)
    logo, cik, country, industry, marketcap, employees, phone, ceo, url,description, exchange, name, symbol, hq_address, hq_state, hq_country, tags, similar=(
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
        stock_details_data["similar"])

    return stock_details_data

def get_stock_news(symbol):
    #calling live API news data from Polygon on each stock symbol
    stock_newss_data = api.get_stock_news(symbol)
    return stock_newss_data

def create_stockdetail(logo, cik, country, industry, marketcap, employees, phone, ceo, url, description, exchange, name, symbol, hq_address, hq_state, hq_country):
    
    stock_detail = Stockdetail(logo=logo, cik=cik,
    country=country,
    industry=industry,
    marketcap=marketcap,
    employees=employees,
    phone=phone,
    ceo=ceo,
    url=url,
    description=description,
    exchange=exchange,
    name=name,
    symbol=symbol, 
    hq_address=hq_address,
    hq_state=hq_state,
    hq_country=hq_country)

    db.session.add(stock_detail)
    db.session.commit()

    return stock_detail

def create_stocknews(symbol, timestamp, title, url, source, summary, image):
    stocknews = Stocknews(symbol, timestamp, title, url, source, summary, image)
    db.session.add(stocknews)
    db.session.commit()

    return stocknews

#SUBSCRIPTION INFO =============
# Create and return a new Subscription:
def create_subscription(user_name, plan_id):

    subscription = Subscription(user_name=user_name, plan_id=plan_id)

    db.session.add(subscription)
    db.session.commit()
    return subscription

def create_plan(name, stocks_per_month, investment_per_month):
    plan = Plan(name=name, stocks_per_month=stocks_per_month, investment_per_month=investment_per_month)
    db.session.add(plan)
    db.session.commit()
    return plan

#Create and return a new Stock_in_Subscription:
def create_stock_in_subscription(stock_in_subscription_id, user_id, stock_id, added_time,
                        stock_price):

    stock_in_subscription = Stock_in_Subscription(user_id = user_id, stock_id = stock_id,
                added_time = added_time, stock_price = stock_price
    )

    db.session.add(stock_in_subscription)
    db.session.commit()
    return stock_in_subscription

#Create sample blogs=========

#API Routes==============================
def get_quote():
    with open('data/quotes.json') as q:
        quotes = json.loads(q.read())
    return quotes

def get_users():
    """Return all users."""

    return User.query.all()

def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)

def get_user_by_username(username):
    """Return a user by username."""
    return User.query.filter(User.username == username).first()

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


#STOCK==============================

def get_all_stocks():
    all_stocks = Stock.query.all()
    return all_stocks

def get_stock_names():
    """Return all stock names."""
    company_names = []
    all_stocks = Stock.query.all()
    for stock in all_stocks:
        company_name = stock.name
        company_names.append(company_name)
    return company_names

def get_stock_by_symbol(symbol):
    """Return all stock names."""
    stock = Stock.query.filter(Stock.symbol == symbol).first()
    
    return stock

def get_stock_urls():
    """Return all stock urls."""
    urls = []
    all_stocks = Stock.query.all()
    for stock in all_stocks:
        url = stock.url
        company_names.append(url)
    return urls

#FAVORITES===============================================
def create_favorites(user_id, stock_id, is_favorite):
    """create and returns user favorites from stocks list """

    userFavorites = UserFavorite(
                    user_id = user_id,
                    stock_id = stock_id,
                    is_favorite = True)

    db.session.add(userFavorites)
    db.session.commit()

    return userFavorites

def delete_favorites(user_id, stock_id):
    """delete from database when user unfavorites stock"""
    fav_stock = db.session.query(UserFavorite).filter(UserFavorite.user_id == user_id,UserFavorite.stock_id == stock_id).first()
    db.session.delete(fav_stock)
    db.session.commit()
    
def get_user_favorites(user_id):
    """returns all user favorites"""
    favs_of_user = UserFavorite.query.filter(user_id=user_id).all()

    return favs_of_user

def get_fav_obj(user_id,stock_id):

    userfav = UserFavorite.query.filter_by(user_id=user_id, stock_id=stock_id).one()

    return userfav

#BLOGS============
def get_all_blogs():
    return Blog.query.all()

#PLANS=======
def get_plan_by_name(name):
    plan = Plan.query.filter(name==name).first()
    return plan



