"""data models for Plenti"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

#USER================================================
class User(db.Model):
#user table
    __tablename__ ='user'

    username = db.Column(db.String, unique=True, nullable = False, primary_key=True) 
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    avatar = db.Column(db.String, default = 'static/img/JLo.jpeg')
    address = db.Column(db.String)
    
    def __repr__(self):
        return f'<User {self.fname} {self.lname}>'


class UserFavorite(db.Model):
    __tablename__ = 'userfavorite'
    favorite_id = db.Column(db.Integer, autoincrement= True, primary_key=True)
    username = db.Column(db.String, db.ForeignKey('user.username'))
    symbol = db.Column(db.String, db.ForeignKey('stock.symbol'))
   
    stock = db.relationship('Stock', backref = 'userfavorite')
    user = db.relationship('User', backref = 'userfavorite')

    def __repr__(self):
        return f'<userFavorites favorite_id={self.username} is_favorite={self.symbol}>'

#STOCKS =========================================
class Stock(db.Model):
    """Stocks Table"""

    __tablename__ = 'stock'

    symbol = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    industry = db.Column(db.String)
    exchange = db.Column(db.String)
    asset_type = db.Column(db.String)
    currency = db.Column(db.String)
    ipodate = db.Column(db.String)
    employees = db.Column(db.Integer)
    sample = db.Column(db.Boolean)
    
    def __repr__(self):
        return f'<Stock {self.symbol}>'


class Stockprice(db.Model):

    __tablename__ = 'stockprice'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    symbol = db.Column(db.String, db.ForeignKey('stock.symbol'))
    openprice = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    closeprice = db.Column(db.Float)
    volume = db.Column(db.Integer)
    date = db.Column(db.String)
    stock = db.relationship("Stock", backref="stockprice")

    def __repr__(self):
            return f'<Stockprice {self.symbol}>'

class Stockdetail(db.Model):
#from POLYGON
    __tablename__ = 'stockdetail'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    symbol = db.Column(db.String, db.ForeignKey('stock.symbol'))
    logo = db.Column(db.String)
    cik = db.Column(db.String)
    country = db.Column(db.String)
    industry = db.Column(db.String)
    marketcap = db.Column(db.BigInteger)
    employees = db.Column(db.BigInteger)
    phone = db.Column(db.String)
    ceo = db.Column(db.String)
    url = db.Column(db.String)
    description = db.Column(db.String)
    exchange = db.Column(db.String)
    name = db.Column(db.String)
    hq_address = db.Column(db.String)
    hq_state = db.Column(db.String)
    hq_country = db.Column(db.String)
    stock = db.relationship("Stock", backref="stockdetail")

    def __repr__(self):
            return f'<Stockdetail {self.symbol}>'

class Stocknews(db.Model):

    __tablename__ = 'stocknews'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    symbol = db.Column(db.String, db.ForeignKey('stock.symbol'))
    title = db.Column(db.String)
    url = db.Column(db.String)
    source = db.Column(db.String)
    summary = db.Column(db.String)
    summary = db.Column(db.String)
    stock = db.relationship("Stock", backref="stocknews")

#SUBSCRIPTION ======================================
class Plan(db.Model):
    """Different monthly plans"""

    __tablename__ = 'plan'

    id = db.Column(db.Integer, autoincrement= True, primary_key=True)
    name = db.Column(db.String)
    stocks_per_month = db.Column(db.Integer)
    investment_per_month = db.Column(db.Integer) 

    def __repr__(self):
        return f'<Plan {self.name}>'

class Subscription(db.Model):
    id = db.Column(db.Integer, autoincrement= True, primary_key=True)
    user_name = db.Column(db.String, db.ForeignKey('user.username'))
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'))
    Subscription_start_timestamp = db.Column(db.DateTime)
    Subscription_end_timestamp = db.Column(db.DateTime)

    plan = db.relationship("Plan", backref="subscriptions")
    user = db.relationship("User", backref="subscriptions")


    def __repr__(self):
        return f'<Subscription by {self.user_name} of {self.plan.name} >'

class Stock_in_Subscription(db.Model):
    """Add stock to a subcription box"""

    __tablename__ = 'stock_in_subscription'

    id = db.Column(db.Integer, autoincrement= True, primary_key=True)
    stock_symbol = db.Column(db.String, db.ForeignKey('stock.symbol'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'), nullable=False) 
    subscription = db.relationship("Subscription",
                             backref="stock_in_subscription")
    def __repr__(self):
        return f'<stock_in_subscription {self.subscription_id} of {self.stock_symbol}>'

#BLOG=================
class Blog(db.Model):

    __tablename__ = 'blog'
    id = db.Column(db.Integer, autoincrement= True, primary_key=True)
    title = db.Column(db.String)
    url = db.Column(db.String)

    def __repr__(self):
        return f'<blog {self.title}'

#EVENTS======================
class Event(db.Model):
    """An event."""

    __tablename__ = 'event'

    id = db.Column(db.Integer, autoincrement=True, 
                    primary_key=True)
    name = db.Column(db.String)
    date = db.Column(db.DateTime)
    description = db.Column(db.Text)
    image_url = db.Column(db.String, default='static/img/Plenti_logo.png')
    status = db.Column(db.String(10), default='FUTURE')

    def __repr__(self):
        return f'<Meetup {self.name} at {self.date}>'
        
class Comment(db.Model):    
    """A meetup comment."""

    __tablename__ = 'comment'

    id = db.Column(db.Integer, autoincrement=True, 
                    primary_key=True)
    user_name = db.Column(db.String, db.ForeignKey('user.username'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    body = db.Column(db.Text)

    writer = db.relationship('User', backref='comment') 
    event = db.relationship('Event', backref='comment')

    def __repr__(self):
            return f'<Comment on Meetup {self.meetup_id} by User {self.user_name}>'

def connect_to_db(flask_app, db_uri='postgresql:///stocks', echo=False):
    
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("connected to db!!!")

if __name__ == '__main__':
    from server import app

    connect_to_db(app)