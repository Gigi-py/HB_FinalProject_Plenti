
from server import connect_to_db
from model import User, Stock, Stockprice, UserFavorite, Plan, Blog, Subscription, Stock_in_Subscription, Event, Comment
import datetime
import requests
import csv
import json
import os

# USER INFO ==================================
#Create and return a new user:
def create_user(username, fname, lname, image_url, city, about, password):
    """Return list of user objects"""
    user = User(username = username, fname = fname, lname = lname,  
                image_url = image_url, city = city, about = about, password = password)
    
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
def create_stockprice(openprice, high, low, closeprice, volume, date):
    
    stockprice = Stockprice(openprice = openprice, high = high, low = low, 
    closeprice = closeprice, volume = volume, date = date)

    db.session.add(stockprice)
    db.session.commit()

    return stockprice

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