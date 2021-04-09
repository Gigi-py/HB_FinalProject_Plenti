
from server import connect_to_db
from model import User, Stock, Subscription, Stock_in_Subscription, Favorites, connect_to_db, db
import datetime
import requests
import csv

# USER INFO ==================================
#Create and return a new user:
def create_user(user_id, fname, lname, username, image_url, about):
    """Return list of user objects"""
    user = User(username = username, fname = fname, lname = lname,  img = image_url, about = about)
     # Set the password_hash with password

    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    return user


#check password for user:
def check_password(email, password):
    """ Check password and email for logging in"""

    user= get_user_by_email(email)
   
    if not user:
        return False
    if user.password == password:
        return True
    else:
        return False

# STOCK INFO ================================
#Create and return a new stock:

API_KEY = "J18XE5872X9Y79OQ"

def get_all_stocks():
    """Get stock name info from AA API to store in db """
    url = 'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey='+ API_KEY
    res = requests.get(url)
    params = dict(key=API_KEY, text='stocks', lang='en-es')
    res = requests.get(url, params=params)
    decoded = res.content.decode('utf-8')

    csv_read = csv.reader(decoded.splitlines(), delimiter=',')
    all_stocks = list(csv_read)
    return all_stocks

def save_stocks(all_stocks):
    """save all stocks (names, symbol, etc.. ) in the database from AA API  """
    sample_stocks = []
    for stock in all_stocks:
        if stock[0] in sample_stocks:
            stock = Stock(symbol = stock[0], stock_name=stock[1], asset_type=stock[3], ipo_date=stock[4])
       
        db.session.add(stockInfo)
        db.session.commit()

    return "Finished"

def create_stock(stock_id, symbol, name, 
                description, sector, 
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
def create_subscription(subscription_id, description, subscription_value):

    subscription = Subscription(subscription_id = subscription_id, description = description, 
                subscription_value = subscription_value, user_id = user_id)

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

#FAVORITE INFO=========================
# #Create and return a new Favorite stock:
def create_favorites(favorite_id, user_id, status, stock_id):
    favorites = Favorites (favorite_id = favorite_id, user_id = user_id, status = status, stock_id = stock_id)
    db.session.add(favorites)
    db.session.commit()
    return favorites

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
    """Return a stock by primary key."""
    return Stock.query.all()

def get_stock_by_id(stock_id):
    """Return a stock by primary key."""
    return Stock.query.get(stock_id)

# def get_fans_by_stock_id(stock_id):
#     """Return all fans of a stock."""
#     stock = get_stock_by_id(stock_id)
#     return stock.fans

#SUBSCRIPTION
def get_subscriptions_by_id(subsciption_id):
    """Return a subscription by primary key."""
    return Subscription.query.get(subscription_id)

# def get_stock_in_subscription(subsciption_id):
#     """Return a subscription by primary key."""
#     return Subscription.query.get(subscription_id)


#FAVORITES

def create_user_stock_relationship(user, stock):
    """Make stock object a favorite of user object."""
    user.favorites.append(stock)
    db.session.commit()

def delete_user_stock_relationship(user, stock):
    user.favorites.remove(stock)
    db.session.commit()

def get_favorites_by_user_id(user_id):
    """Return all favorite stocks of user."""
    user = get_user_by_id(user_id)
    return user.favorites

def get_stock_by_user_stock_id(user_id, stock_id):
    """Return a stock if favorited by that user. Return None if not favorited."""
    user = get_user_by_id(user_id)
    stock = get_stock_by_id(stock_id)
    if stock in user.favorites:
        return stock
    else:
        return None