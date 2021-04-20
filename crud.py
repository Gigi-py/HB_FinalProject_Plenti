
from server import connect_to_db
from flask_bcrypt import Bcrypt
from model import User, Stock, Stockprice, Stockdetail, UserFavorite, Plan, Blog, Subscription, Stock_in_Subscription, Event, Comment, connect_to_db, db
import datetime
import api
import requests
import csv
import json
import os

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
def create_stockprice(stock_id, openprice, high, low, closeprice, volume, date):
    
    stockprice = Stockprice(stock_id=stock_id, openprice = openprice, high = high, low = low, closeprice = closeprice, volume = volume, date = date)

    db.session.add(stockprice)
    db.session.commit()

    return stockprice


#Create and return new Stockdetail:
def create_stockdetail(stock_id, logo, cik, country, industry, marketcap, employees, phone, ceo, url,
                    description, exchange, name, symbol, hq_address, hq_state, hq_country):

    stock_detail = Stockdetail(stock_id=stock_id, logo=logo, cik=cik,
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

#SUBSCRIPTION INFO =============
# Create and return a new Subscription:
def create_subscription(user_id, plan_id, subscription_start_timestamp, subscription_end_timestamp):

    subscription = Subscription(user_id=user_id, plan_id=plan_id, Subscription_start_timestamp=subscription_start_timestamp, Subscription_end_timestamp=subscription_end_timestamp)

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




