"""data models for Plenti"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt


import json

db = SQLAlchemy()

#USER================================================
class User(db.Model):
#user table
    __tablename__ ='user'

    id = db.Column(db.Integer, autoincrement=True, 
                    primary_key=True)
    username = db.Column(db.String, unique=True, nullable = False) 
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
    is_favorite = db.Column(db.Boolean, default = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))
   
    stock = db.relationship('Stock', backref = 'userFavorites')
    user = db.relationship('User', backref = 'userFavorites')

    def __repr__(self):
        return f'<userFavorites favorite_id={self.favorite_id} is_favorite={self.is_favorite}>'



#STOCKS ===================================
class Stock(db.Model):
    """Stocks Table"""

    __tablename__ = 'stock'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    symbol = db.Column(db.String)
    name = db.Column(db.String)
    description = db.Column(db.String)
    industry = db.Column(db.String)
    asset_type = db.Column(db.String)
    currency = db.Column(db.String)
    company_url = db.Column(db.String)
    employees = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<Stock {self.id} {self.symbol}>'


class Stockprice():

    __tablename__ = 'stockprice'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'))
    openprice = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    closeprice = db.Column(db.Float)
    volume = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    stock = db.relationship("Stock", backref="stockprice")

    def __repr__(self):
            return f'<Stockprice {self.closeprice}>'

#SUBSCRIPTION ===================================
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'))
    Subscription_start_timestamp = db.Column(db.DateTime)
    Subscription_end_timestamp = db.Column(db.DateTime)

    plan = db.relationship("Plan", backref="subscriptions")
    user = db.relationship("User", backref="subscriptions")


    def __repr__(self):
        return f'<Subscription by {self.user_id} of {self.plan_id} >'

class Stock_in_Subscription(db.Model):
    """Add stock to a subcription box"""

    __tablename__ = 'stock_in_subscription'

    id = db.Column(db.Integer, autoincrement= True, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'), nullable=False) 
    subscription = db.relationship("Subscription",
                             backref="stock_in_subscription")
    def __repr__(self):
        return f'<stock_in_subscription {self.subscription_id} of {self.stock_id}>'

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
    
    comment = db.relationship('Comment', backref='meetup', 
                                order_by='Comment.timestamp')

    def __repr__(self):
        return f'<Meetup {self.name} at {self.date}>'
        
class Comment(db.Model):    
    """A meetup comment."""

    __tablename__ = 'comment'

    id = db.Column(db.Integer, autoincrement=True, 
                    primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    text = db.Column(db.Text)

    writer = db.relationship('User') 

    def __repr__(self):
            return f'<Comment on Meetup {self.meetup_id} by User {self.user_id}>'

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