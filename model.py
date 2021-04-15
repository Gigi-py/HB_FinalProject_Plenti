"""data models for Plenti"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_imageattach.entity import Image, image_attachment
import json

db = SQLAlchemy()

#USER================================================
class User(db.Model):
#user table
    __tablename__ ='user'

    id = db.Column(db.Integer, autoincrement=True, 
                    primary_key=True)
    username = db.Column(db.String, unique=True) 
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    avatar = image_attachement('UserPicture')
    address = db.Column(db.String)

    def __repr__(self):
        return f'<User {self.fname} {self.lname}>'

    def to_dict(self, include_email=True):
        data = {
            'user_id': self.id,
            'username': self.username,
            'fname': self.fname,
            'lname': self.lname,
            'email': self.email,
            'avatar': self.avatar,
            'address': self.address,
        }
    
        return data

class UserPicture(self, Image):
    """User picture model."""

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user = relationship('User')
    __tablename__ = 'user_picture'

#STOCKS ===================================
class Stock(db.Model):
    """Stocks Table"""

    __tablename__ = 'stock'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    symbol = db.Column(db.String)
    company_name = db.Column(db.String)
    description = db.Column(db.String)
    industry = db.Column(db.String)
    asset_type = db.Column(db.String)
    currency = db.Column(db.String)
    company_url = db.Column(db.String)
    stockprice = relationship("stockprice", backref=backref("stock", uselist=False)) #one to one relationship
    
    def __repr__(self):
        return f'<Stock {self.id} {self.symbol}>'

    def to_dict(self):
        data = {
            'stock_id': self.id,
            'symbol': self.symbol,
            'company_name': self.company_name,
            'description': self.description,
            'industry': self.industry,
            'asset_type': self.asset_type,
            'currency': self.currency,
            'current_price': self.current_price,
            'company_url': self.company_url
        }
        return data


class StockPrice():
    __tablename__ = 'stockprice'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey(stock.id))
    date = db.Colummn(db.DateTime)
    open = db.Column(db.Float)
    high = sdb.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
    volumn = db.Column(db.Integer)

    def __repr__(self):
        return f'<Stock Price for {self.symbol} on {self.date}>'

    def to_dict(self):
        data = {
            'symbol': self.symbol,
            'date': self.date,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'volumn': self.volumn,
        }

        return data

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

    def to_dict(self):
        data = {
            'plan_name': self.name,
            'stocks_per_month': self.stocks_per_month,
            'investment_per_month': self.investment_per_month,
            'user_id': self.user_id
        }
        return data

class Subscription(db.Model):
    id = db.Column(db.Integer, autoincrement= True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'))
    Subscription_start_timestamp = db.Column(db.DateTime)
    Subscription_end_timestamp = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Plan {self.name}>'

    def to_dict(self):
        data = {
            'plan_name': self.name,
            'stocks_per_month': self.stocks_per_month,
            'investment_per_month': self.investment_per_month,
            'user_id': self.user_id
        }
        return data


class Stock_in_Subscription(db.Model):
    """Add stock to a subcription box"""
    """which stock is in the subcription box"""

    __tablename__ = 'stock_in_subscription'

    stock_in_subscription_id = db.Column(db.Integer, autoincrement= True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id')) 
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.stock_id'))
    added_time = db.Column(db.DateTime)
    stock_price = db.Column(db.Integer) 
    user = db.relationship('User', backref = 'stock_in_subscription')
    stock = db.relationship('Stock', backref = 'stock_in_subscription')

    def __repr__(self):
        return f'<stock_in_subscription {self.subscription_id} of {self.stock_id}>'

    def to_dict(self):
        data = {
            'stock_in_subscription_id': self.stock_in_subscription_id,
            'user_id': self.user_id,
            'stock_id': self.stock_id,
            'added_time': self.added_time,
            'stock_price': self.stock_price
        }
        return data

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