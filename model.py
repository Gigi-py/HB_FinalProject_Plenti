"""data models for Plenti"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()

#USER========================================
class User(db.Model):
#user table
    __tablename__ ='users'

    user_id = db.Column(db.Integer, autoincrement=True, 
                    primary_key=True)
    username = db.Column(db.String, unique=True) 
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    image_url = db.Column(db.String, default='/static/img/JLo.jpeg')
    city = db.Column(db.String)
    about = db.Column(db.Text)

    def __repr__(self):
        return f'<User {self.fname} {self.lname}>'

    def to_dict(self, include_email=True):
        data = {
            'user_id': self.user_id,
            'username': self.username,
            'fname': self.fname,
            'lname': self.lname,
            'image_url': self.image_url,
            'city': self.city,
            'about': self.about
        }
        if include_email:
            data['email'] = self.email
        return data

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)
    
    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)

#STOCKS ===================================
class Stock(db.Model):
    """Stocks Table"""

    __tablename__ = 'stocks'

    stock_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    symbol = db.Column(db.String)
    company_name = db.Column(db.String)
    description = db.Column(db.String)
    industry = db.Column(db.String)
    asset_type = db.Column(db.String)
    ipo_date = db.Column(db.DateTime)
    current_price = db.Column(db.Integer)
    

    def __repr__(self):
        return f'<Stock {self.stock_id} {self.symbol}>'

    def to_dict(self):
        data = {
            'stock_id': self.id,
            'symbol': self.symbol,
            'company_name': self.company_name,
            'description': self.description,
            'industry': self.industry,
            'asset_type': self.asset_type,
            'ipo_date': self.ipo_date,
            'current_price': self.current_price,
        }
        return data

#SUBSCRIPTION ===================================
class Subscription(db.Model):
    """Different subscription offerings for users"""

    __tablename__ = 'subscriptions'

    subscription_id = db.Column(db.Integer, autoincrement= True, primary_key=True)
    created_date = db.Column(db.DateTime)
    updated_date = db.Column(db.DateTime)
    description = db.Column(db.Text)
    monthly_investment = db.Column(db.Integer) 

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    user = db.relationship('User', backref = 'Subscription')

    def __repr__(self):
        return f'<Subscription {self.subscription_id}>'

    def to_dict(self):
        data = {
            'subscription_id': self.subscription_id,
            'created_date': self.created_date,
            'updated_date': self.updated_date,
            'description': self.description,
            'monthly_investment': self.monthly_vaue,
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