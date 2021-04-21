
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

def save_stocks():
    sample_stocks = ['PYPL','HLT', 'PINS', 'TWLO', 'W']

    """save all stocks (names, symbol etc.. ) in the database from AA API  """
    all_stocks = get_all_stock_symbols()
    for stock in all_stocks:
        if stock[0] not in sample_stocks:
            stockInfo = Stock(symbol = stock[0], name=stock[1], asset_type=stock[3], ipodate=stock[4])
            db.session.add(stockInfo)
            db.session.commit()

    return "saved all stock symbols to database"


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
def create_stockdetail(symbol, logo, cik, country, industry, marketcap, employees, phone, ceo, url,
                    description, exchange, name, hq_address, hq_state, hq_country):

    stock_detail = Stockdetail(symbol=symbol, logo=logo, cik=cik,
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
def create_subscription(user_name, plan_id, subscription_start_timestamp, subscription_end_timestamp):

    subscription = Subscription(user_name=user_name, plan_id=plan_id, Subscription_start_timestamp=subscription_start_timestamp, Subscription_end_timestamp=subscription_end_timestamp)

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
def create_blog():

    sample_articles = [{"title": "What is a Stock", "url": "https://learn.robinhood.com/articles/6FKal8yK9kk22uk65x3Jno/what-is-a-stock/"},
    {"title": "What is a portfolio", "url":"https://learn.robinhood.com/articles/4vaR9PkTzes8u3ibLAWrD1/what-is-a-portfolio/"},
    {"title": "What is an Initial Public Offering", "url": "https://learn.robinhood.com/articles/6UsdUrlnUvxiDpDT4D2bup/what-is-an-initial-public-offering-ipo/"},
    {"title": "What is Venture Capital", "url": "https://learn.robinhood.com/articles/4XRFKEfckD73crXUgLBsoK/what-is-venture-capital/"},
    {"title": "What is an Investment Company", "url": "https://learn.robinhood.com/articles/2FxgvV1Nt0LoTq59xJzj3/what-is-an-investment-company/"},
    {"title": "What is a Stock Option", "url": "https://learn.robinhood.com/articles/YtqceruIQSiHncrlcecPL/what-is-a-stock-option/"}
    ]
    
    articles_in_db = []
    for article in sample_articles:
        title = article['title']
        url = article['url']
        article = Blog(title=title, url=url)
        articles_in_db.append(article)
        db.session.add(article)
        db.session.commit()

    return articles_in_db

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



