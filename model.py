"""data models for Plenti"""

from datetime import datetime
#add datatime library
from flask_sqlalchemy import SQLAlchemy
#add SQLAlchemy functionality
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()

class User(db.Model):
#user table
    __tablename__ ='users'

    user_id = db.Column(db.Integer, autoincrement=True, 
                    primary_key=True)
    username = db.Column(db.String) #unique=True
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)
    image_url = db.Column(db.String, default='')
    about = db.Column(db.Text)

    # favorites = db.relationship('Stock', secondary=favorites,
    #                 backref='fans')

    def __repr__(self):
        return f'<User {self.fname} {self.lname}>'

    def to_dict(self, include_email=False):
        data = {
            'user_id': self.user_id,
            'username': self.username,
            'fname': self.fname,
            'lname': self.lname,
            'image_url': self.image_url,
            'about': self.about
        }
        if include_email:
            data['email'] = self.email
        return data

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Stock(db.Model):
    """Stocks Table"""
    #todo: check API to see what data I am able to get back

    __tablename__ = 'stocks'

    stock_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    symbol = db.Column(db.String, nullable = False)
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    sector = db.Column(db.String, nullable = False)
    asset_type = db.Column(db.String, nullable = False)
    ipo_date = db.Column(db.DateTime, nullable = False)
    current_price = db.Column(db.Integer, nullable = False)
    ipo_price = db.Column(db.Integer, nullable = False)
    # ipo_date = db.Column(db.String, nullable = False)

    def __repr__(self):
        return f'<Stock {self.stock_id} {self.symbol}>'

    def to_dict(self):
        data = {
            'stock_id': self.id,
            'symbol': self.symbol,
            'name': self.name,
            'company_overview': self.company_overview,
            'sector': self.sector,
            'asset_type': self.asset_type,
            'ipo_date': self.ipo_date,
            'current_price': self.current_price,
            'ipo_price': SELF.ipo_price
        }
        return data


class Subscription(db.Model):
    """Different subscription offerings for users"""

    __tablename__ = 'subscriptions'

    subscription_id = db.Column(db.Integer, autoincrement= True, primary_key=True)
    description = db.Column(db.Text)
    subscription_value = db.Column(db.Integer) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    user = db.relationship('User', backref = 'Subscription')

    def __repr__(self):
        return f'<Subscription {self.subscription_id}>'

    def to_dict(self):
        data = {
            'subscription_id': self.subscription_id,
            'description': self.description,
            'subscription_value': self.subscription_value,
            'user_id': self.user_id
        }
        return data


class Stock_in_Subscription(db.Model):
    """Add stock to a subcription box"""
    """which stock is in the subcription box"""

    __tablename__ = 'stock_in_subscription'

    subscription_id = db.Column(db.Integer, autoincrement= True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id')) 
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.stock_id'))
    added_time = db.Column(db.DateTime)
    stock_price = db.Column(db.Integer, db.ForeignKey('stocks.current_price'), nullable = False) 
    user = db.relationship('User', backref = 'stock_in_subscription')
    stock = db.relationship('Stock', backref = 'stock_in_subscription')

    def __repr__(self):
        return f'<stock_in_subscription {self.subscription_id} of {self.stock_id}>'

    def to_dict(self):
        data = {
            'subscription_id': self.event_id,
            'user_id': self.user_id,
            'stock_id': self.stock_id,
            'added_time': self.created_time,
            'stock_price': self.stock_price
        }
        return data

class Favorites(db.Model):
    """favourite stocks by user"""

    __tablename__ = 'favorites'

    favorite_id = db.Column(db.Integer, autoincrement= True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id')) 
    status = db.Column(db.String(10), default='LIKED')
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.stock_id')) 

    user = db.relationship('User', backref = 'favorites')
    stock = db.relationship('Stock', backref = 'favorites')

    def __repr__(self):
        return f'<Loved {self.event_id} by {self.user}>'

    def to_dict(self):
        data = {
            'favorite_id': self.favorite_id,
            'user_id': self.user_id,
            'status': self.status,
            'stock_id': self.stock_id
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

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)