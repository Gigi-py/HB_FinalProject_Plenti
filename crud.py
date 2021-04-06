from server import db, connect_to_db
from model import User, Stock, UserBasket
import requests
import csv

# user info================================================================
def get_user():
    """Return list of user objects"""

    return User.query.all()

def get_user_by_fname(user_id):
    return User.query.filter(User.id == user_id).first()

def get_user_by_id(user_id):
    """Return a user by primary with user email"""
    user_id_identification = User.query.get(user_id)

    return user_id_identification

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def create_user(email, password, first_name, last_name):
    """create a new user"""

    user = User(email=email,
                password=password,
                first_name=first_name, 
                last_name=last_name)

    db.session.add(user)
    db.session.commit()

    return user

def check_password(email, password):
    """ Check password and email for logging in"""

    user= get_user_by_email(email)
   
    if not user:
        return False
    if user.password == password:
        return True
    else:
        return False

# stock info ================================================================

# ============================favorite info ===============================================
def create_favorites(user_id, stock_id):
    """create and returns user favorites from stocks list """

    userBaskets = UserBasket(
                    user_id = user_id,
                    stock_id = stock_id)

    
    db.session.add(userBaskets)
    db.session.commit()

    return userBaskets

def delete_stock_user(user_id, stock_id):
    """delete from database when user unfavorites stock"""
    fav_obj = db.session.query(UserBasket).filter(UserBasket.user_id == user_id,UserBasket.stock_id == stock_id).first()
    # print(fav_obj)

    db.session.query(UserBasket).filter(UserBasket.user_id == user_id,UserBasket.stock_id == stock_id).first()
    db.session.delete(fav_obj)
    db.session.commit()
    

def user_favorites(user_id):
    """returns all user favorites"""
    favs = UserBasket.query.filter(user_id=user_id).all()


    db.session.add(favs)
    db.session.commit()
    return favs
def get_user_fav(user_id,stock_id):

    userfav= UserBasket.query.filter_by(user_id=user_id, stock_id=stock_id).one()

    return userfav