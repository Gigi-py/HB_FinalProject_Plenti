"""FOCUS ON MY VISION OF WHAT I WANT TO BUILD AND GAIN THE SKILLS TO ACHIEVE IT."""

from flask import Flask, render_template, make_response, url_for, request, flash, session, jsonify, redirect
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from model import connect_to_db, db, User, Stock, Stockprice, UserFavorite, Plan, Blog, Subscription, Stock_in_Subscription, Event, Comment
from random import sample, choice
import crud
import json
import os
import math
from jinja2 import StrictUndefined
from datetime import datetime, timedelta


#INITIALIZING APP=========
app = Flask(__name__)
app.secret_key = 'dev'
connect_to_db(app)
bcrypt = Bcrypt(app)

#LOGIN FLOW===================
@app.route('/') 
def show_homepage():
    """Homepage"""
    return render_template('index.html')

@app.route('/login', methods=['GET']) 
def show_login_form():
    """Show homepage"""
    return render_template('login.html')

@app.route('/login', methods=['POST']) 
def login():
    """Sign in user"""
    #to do: check validity of the user
    session['username'] = request.form.get('username')
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/login')

#USER DASHBOARD============
@app.route('/dashboard')
def view_dashboard():
    username = session['username'].upper()  
    all_stocks = Stock.query.all()
    favorites=UserFavorite.query.filter(username==username)
    
    return render_template('/dashboard.html', username=username, all_stocks=all_stocks, favorites=favorites)

@app.route('/chartupdate')
def chart_update():
    today = datetime.today() 
    symbol = request.args.get('symbol')
    date_range = request.args.get('date_range')
    if date_range == 'week':
        td = timedelta(7)
    elif date_range == 'month':
        td = timedelta(30)
    elif date_range == 'quarter':
        td = timedelta(120)
    else:
        td = timedelta(5)

    edate = today - timedelta(2)  
    sdate = edate - td 
    date=sdate 
    list_of_dates=[]
    while date<edate:
        date+=timedelta(days=1) 
        list_of_dates.append(date.strftime('%Y-%m-%d'))

    price_data = []
    for d in list_of_dates:
        print("="*50, f"in server, symbol = {symbol}")
        data = crud.get_price_data(symbol, d)
        price_data.append((d, data.get('close')))
        price_data_json=json.dumps(price_data)
        # import pdb; pdb.set_trace()

    return price_data_json

@app.route('/user/<username>')
def show_user_profile(username):
    """Show the user profile page for that user"""
    username = session['username']
    user = crud.get_user_by_username(username)
    favorite = request.form.get("save")
    return render_template('user-profile.html', user=user, username=username)

@app.route('/subscription/<username>')
def subscription(username):
    username = session['username']
    user = crud.get_user_by_username(username)
    symbols_in_subscription = []
    subscription = Subscription.query.filter(username == username).first()
    plan = crud.get_plan_by_id(subscription.plan_id)
    stock_in_subscription = crud.get_stock_in_subscription(subscription.id)
    for stock in stock_in_subscription:
        symbols_in_subscription.append(stock.stock_symbol)
    
    favorites=UserFavorite.query.filter(username==username)

    return render_template('subscription.html', subscription=subscription, user=user, plan=plan, stock_in_subscription=stock_in_subscription, symbols_in_subscription=symbols_in_subscription, favorites=favorites)
    
@app.route('/stocks/<username>')
def user_stocks():
    username = session['username']
    user = crud.get_user_by_username(username)
    user_id = user.id
    subscription = Subscription.query.filter(user_id == user_id).first()
    
    return render_template('mystocks.html')

#STOCKS===================
@app.route('/searchstocks')
def searchstocks():
    
    return render_template('/searchstocks.html')

@app.route('/allstocks')
def view_all_stocks():
    """view a list of all stocks to invest."""
    stock_symbols = ['HLT', 'TWLO', 'UPS', 'AMZN', 'ADBE', 'DIS', 'FB',
    'NFLX', 'TSLA', 'LULU', 'F', 'WBA']
    
    all_stocks = []
    all_stock_details = []
    for symbol in stock_symbols:
       stock = crud.get_stock_by_symbol(symbol)
       stock_detail = crud.get_stockdetails(symbol) 
       all_stocks.append((stock, stock_detail))
    username = session.get('username')
    
    return render_template("/allstocks.html", all_stocks=all_stocks)

@app.route('/stockdetails/<symbol>')
def view_stock_details(symbol):
    """view a list of all stocks to invest."""
    username = session.get('username')
    stock = crud.get_stock_by_symbol(symbol)
    stock_detail = crud.get_stockdetails(symbol)
    stock_news_data = crud.get_stock_news(symbol)
    userFav = crud.get_fav_obj(username, symbol)
    if userFav:
        fav_status = True
    else: 
        fav_status = False
    return render_template("/stock_details.html", username=username, stock=stock, stock_detail=stock_detail, stock_news_data=stock_news_data, fav_status=fav_status)

@app.route('/favorites/<symbol>', methods=['GET','POST'])
def add_fav_stock(symbol):
    username = session['username']
    fav_status = request.form.get("fav-action")
    if fav_status == 'add':
        new_userFav = crud.create_favorites(username, symbol)
    if fav_status == 'remove':
        deleted_stock = crud.delete_favorites(username, symbol)
    return redirect('/subscription/'+ username)

@app.route('/addsubscription', methods=['POST'])
def add_subscription():
    """getting the value selections of stocks and plans and adding it to the database"""
    stocks_selected = request.form.getlist("stocknames")
    plan_selected = request.form.get("plans")

    plan = crud.get_plan_by_name(plan_selected)
    plan_id = plan.id

    user_name = session.get('username')
    new_subscription = crud.create_subscription(user_name, plan_id)
    subscription_id = new_subscription.id
    for stock in stocks_selected:
        new_stock_in_subscription = crud.create_stock_in_subscription(stock, subscription_id)
    return redirect('/subscription/'+ user_name)

@app.route('/plans')
def view_plans():
    """view a list of all subscriptions to choose from."""
    return render_template("/plans.html") 

@app.route('/plans', methods=["POST"])
def add_stocks_to_plan():
    """view a list of all subscriptions to choose from."""

    return render_template("/plans.html") 

@app.route('/checkplan')
def check_plan():
    subscription = True
    username = session['username']
    return render_template("/checkplan.html", subscription=subscription) 


@app.route('/checkout')
def checkout():
    """view a list of all subscriptions to choose from."""
    return render_template("/checkout.html") 

@app.route('/blog')
def all_blogs():
    """render blogs from database"""
    blogs = crud.get_all_blogs()

    return render_template("blog.html", blogs=blogs)

@app.route('/price-chart/<symbol>')
def show_price_chart(symbol):
    """Get price chart"""
    today = datetime.today() 
    td = timedelta(30)
    edate = today - timedelta(2)  
    sdate = today - td 
    date=sdate 
    list_of_dates=[]
    while date<edate:
        date+=timedelta(days=1) 
        list_of_dates.append(date.strftime('%Y-%m-%d'))

    price_data = []
    for d in list_of_dates:
        print("="*50, f"in server, symbol = {symbol}")
        data = crud.get_price_data(symbol, d)
        price_data.append((d, data.get('close')))
        # import pdb; pdb.set_trace()

    return render_template('chart.html', price_data=price_data)

@app.route('/searchstock', methods=["GET"])
def search_stock():
    """Show search bar for stock symbols""" 
    return render_template('search.html')

@app.route('/searchstock', methods=["POST"])
def view_search_result():
    """Show stock details for searched symbol""" 
    username = session.get('username')
    symbol = request.form.get('symbol')
    stock = crud.get_stock_by_symbol(symbol)
    stock_detail = crud.get_stockdetails(symbol)
    stock_news_data = crud.get_stock_news(symbol)
    userFav = crud.get_fav_obj(username, symbol)
    if userFav:
        fav_status = True
    else: 
        fav_status = False
    return render_template("/stock_details.html", username=username, stock=stock, stock_detail=stock_detail, stock_news_data=stock_news_data, fav_status=fav_status)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/signup', methods=['GET']) 
def show_signup_form():
    """Show homepage"""
    return render_template('signup.html')

@app.route('/signup', methods=['POST']) 
def register_user():
    """Register user"""
    #to do: add user to database
    session['username'] = request.form.get('username')
    return redirect('/dashboard')

@app.route('/contact')
def contact():
    return render_template('contact.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    DebugToolbarExtension(app)
