from datetime import datetime
#add datatime library
from flask_sqlalchemy import SQLAlchemy
#add SQLAlchemy functionality

db = SQLAlchemy()

class User(db.Model):
    
    """User Table"""

__tablename__ ='users'

    user_id = db.Column(db.Integer, autoincrement= True, primary_key= True)
    email = db.Column(db.String, unique = True)
    password= db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'


class Stock(db.Model):
    """All Stocks"""
    """needs to dig into the API"""

    __tablename__ = 'stocks'


    stock_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    symbol = db.Column(db.String, nullable = False)
    company_name = db.Column(db.String, nullable = False)
    # exchange = db.Column(db.String, nullable = False)
    asset_type = db.Column(db.String, nullable = False)
    status = db.Column(db.String, nullable = False)
    current_price = db.Column(db.Integer, nullable = False)
    ipo_price = db.Column(db.Integer, nullable = False)
    # ipo_date = db.Column(db.String, nullable = False)
    # delisting_date = db.Column(db.String, nullable = False)
    women_lead = db.Column(db.Boolean, default = False )

    def __repr__(self):
        return f'<Stock stock_id={self.stock_id} symbol={self.symbol}>'


class UserBasket(db.Model):
    """users items in subscription box """

    __tablename__ = 'userBasket'

    basket_id = db.Column(db.Integer, autoincrement= True, primary_key=True)
    is_favorite = db.Column(db.Boolean, default = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.stock_id'))
   
    stock = db.relationship('Stock', backref = 'userBasket')
    user = db.relationship('User', backref = 'userBasket')

    def __repr__(self):
        return f'<userBasket favorite_id={self.basket_id} is_favorite={self.is_favorite}>'


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)