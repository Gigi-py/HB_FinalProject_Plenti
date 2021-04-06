
from datetime import datetime
#add datatime library
from flask_sqlalchemy import SQLAlchemy
#add SQLAlchemy functionality
import json

db = SQLAlchemy()

class User(db.Model):
    
    """User Table"""

__tablename__ ='users'

    user_id = db.Column(db.Integer, autoincrement= True, primary_key= True)
    username = db.Column(db.String)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)
    fname = db.Column(db.String)
    lname = db.Column(db.String)

    def __repr__(self):
        return f'<User {self.user_id} {self.email}>'


class Stock(db.Model):
    """All Stocks"""
    """needs to dig into the API"""

    __tablename__ = 'stocks'


    stock_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    symbol = db.Column(db.String, nullable = False)
    company_name = db.Column(db.String, nullable = False)
    # exchange = db.Column(db.String, nullable = False)
    asset_type = db.Column(db.String, nullable = False)
    ipo_date = db.Column(db.datetime, nullable = False)
    current_price = db.Column(db.Integer, nullable = False)
    ipo_price = db.Column(db.Integer, nullable = False)
    # ipo_date = db.Column(db.String, nullable = False)
    # delisting_date = db.Column(db.String, nullable = False)

    def __repr__(self):
        return f'<Stock {self.stock_id} {self.symbol}>'


class Subscription(db.Model):
    """users items in subscription box """

    __tablename__ = 'subscription'

    subscription_id = db.Column(db.Integer, autoincrement= True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
   
    stock = db.relationship('Stock', backref = 'subscription')
    user = db.relationship('User', backref = 'subscription')

    def __repr__(self):
        return f'<Subscription {self.subscription_id} by {self.is_favorite}>'


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)