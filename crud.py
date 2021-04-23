
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
def get_stockdetails(symbol):
    #calling live API data from Polygon on each stock symbol
    stock_details_data = api.get_stock_details(symbol)
    print(stock_details_data)
    
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
    stock_news_data = api.get_news_details(symbol)
    for news in stock_news_data:
        symbol, timestamp, title, url, source, summary = (
        news["symbols"],
        news["timestamp"],
        news["title"],
        news["url"],
        news["source"], 
        news["summary"])

    return stock_news_data

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
def create_stock_in_subscription(stock_symbol, subscription_id):

    stock_in_subscription = Stock_in_Subscription(stock_symbol=stock_symbol, subscription_id=subscription_id)

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

def get_stock_in_subscription(subscription_id):
    return Stock_in_Subscription.query.filter(subscription_id==subscription_id).all()

#FAVORITES===============================================
def create_favorites(username, symbol):
    """create and returns user favorite stock"""

    user_fav = UserFavorite(
                    username = username,
                    symbol = symbol)

    db.session.add(user_fav)
    db.session.commit()

    return user_fav

def get_user_favorites(username):
    """returns all user favorites"""
    favs_of_user = UserFavorite.query.filter(username==username).all()

    return favs_of_user
    
def delete_favorites(username, symbol):
    """delete from database when user unfavorites stock"""
    fav_stock = UserFavorite.query.filter(username == username, symbol == symbol).first()
    db.session.delete(fav_stock)
    db.session.commit()
    
    return fav_stock
    
def get_fav_obj(username, symbol):

    userfav = UserFavorite.query.filter(username==username, symbol==symbol).first()

    return userfav

#BLOGS============
def get_all_blogs():
    return Blog.query.all()

#PLANS=======
def get_plan_by_name(name):
    plan = Plan.query.filter(name==name).first()
    return plan

def get_plan_by_id(id):
    plan = Plan.query.filter(id==id).first()
    return plan






