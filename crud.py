
from server import connect_to_db
from model import User, Stock, Subscription, Stock_in_Subscription, Favorites, connect_to_db, db
import datetime
import requests
import csv

# USER INFO ==================================
#Create and return a new user:
def create_user(username, fname, lname, image_url, city, dob, about):
    """Return list of user objects"""
    user = User(username = username, fname = fname, lname = lname,  img = image_url, city = city, dob = dob, about = about)
     # Set the password_hash with password
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    return user


#check password for user:
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
ALPHAVANTAGE_API_KEY = "J18XE5872X9Y79OQ"
POLY_API_KEY = 'ehldCsvN37bNwxkDthi_G__QfTdDF3rT'

#Create and add a new stock to the database:
def create_stock(stock_id, symbol, company_name, 
                description, industry, 
                asset_type, ipo_date, 
                current_price, ipo_price):

    stock = Stock(stock_id = stock_id, symbol = symbol, name = name, 
                description = description, sector = sector, 
                asset_type = asset_type, ipo_date = ipo_date, 
                current_price = current_price, ipo_price = ipo_price)

    db.session.add(stock)
    db.session.commit()
    return stock

#SUBSCRIPTION INFO =============
# Create and return a new Subscription:
def create_subscription(subscription_id, created_date, updated_date, 
                        description, monthly_investment, user_id):

    subscription = Subscription(subscription_id = subscription_id, created_date = created_date, updated_date = updated_date, 
                    description = description, monthly_investment = monthly_investment, user_id = user_id)

    db.session.add(subscription)
    db.session.commit()
    return subscription

#Create and return a new Stock_in_Subscription:
def create_stock_in_subscription(subscription_id, user_id, stock_id, added_time,
                        stock_price):

    stock_in_subscription = Stock_in_Subscription(subscription_id = subscription_id, user_id = user_id, stock_id = stock_id,
                added_time = added_time, stock_price = stock_price
    )

    db.session.add(stock_in_subscription)
    db.session.commit()
    return stock_in_subscription

#OTHER FEATURES ==============================
# USERS
def get_user_by_id(user_id):
    """Return a user by primary key."""
    return User.query.get(user_id)

def get_user_by_username(username):
    """Return a user by username."""
    return User.query.filter_by(username=username).first()

def get_user_by_email(email):
    """Return a user by email."""
    return User.query.filter_by(email=email).first()

def update_user(username, fname, lname, email, password, image_url, about):
    
    if fname:
        user.fname = fname
    if lname:
        user.lname = lname
    if email:
        user.email = email
    if password:
        user.set_password(password)
    if image_url:
        user.image_url = image_url
    if about:
        user.about = about

    db.session.commit()

#STOCKS

def get_stock():
    """Return all stocks."""
    return Stock.query.all()

def get_stock_by_id(stock_id):
    """Return a stock by primary key."""
    return Stock.query.get(stock_id)

#SUBSCRIPTION

def get_subscriptions():
    """Return all subscriptions."""
    return Stock.query.all()

def get_subscriptions_by_id(subsciption_id):
    """Return a subscription by primary key."""
    return Subscription.query.get(subscription_id)
