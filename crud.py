
from server import connect_to_db
from model import User, Stock, Subscription, Stock_in_Subscription, connect_to_db, db
import datetime
import requests
import csv
import json

# USER INFO ==================================
#Create and return a new user:
def create_user(username, fname, lname, image_url, city, about, password):
    """Return list of user objects"""
    user = User(username = username, fname = fname, lname = lname,  image_url = image_url, city = city, about = about, password = password)
    
    db.session.add(user)
    db.session.commit()
    return user

# STOCK INFO ================================
ALPHAVANTAGE_API_KEY = "J18XE5872X9Y79OQ"
POLY_API_KEY = 'ehldCsvN37bNwxkDthi_G__QfTdDF3rT'

#Create and add a new stock to the database:
def create_stock(symbol, company_name, 
                description, industry, 
                asset_type, ipo_date, 
                current_price):

    stock = Stock(symbol = symbol, company_name = company_name, 
                description = description, industry = industry, 
                asset_type = asset_type, ipo_date = ipo_date, 
                current_price = current_price)
    db.session.add(stock)
    db.session.commit()
    return stock

#SUBSCRIPTION INFO =============
# Create and return a new Subscription:
def create_subscription(created_date, updated_date, 
                        description, monthly_investment, user_id):

    subscription = Subscription(created_date = created_date, updated_date = updated_date, 
                    description = description, monthly_investment = monthly_investment, user_id = user_id)

    db.session.add(subscription)
    db.session.commit()
    return subscription

#Create and return a new Stock_in_Subscription:
def create_stock_in_subscription(stock_in_subscription_id, user_id, stock_id, added_time,
                        stock_price):

    stock_in_subscription = Stock_in_Subscription(user_id = user_id, stock_id = stock_id,
                added_time = added_time, stock_price = stock_price
    )

    db.session.add(stock_in_subscription)
    db.session.commit()
    return stock_in_subscription

#OTHER FEATURES ==============================
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