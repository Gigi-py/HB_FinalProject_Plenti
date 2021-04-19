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
import stripe

stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

#INITIALIZING APP
app = Flask(__name__)
app.secret_key = 'dev'
connect_to_db(app)
bcrypt = Bcrypt(app)

@app.route('/') 
def show_homepage():
    """Homepage"""
    return render_template('index.html')

@app.route('/login', methods=['GET']) 
def show_login_form():
    """Homepage"""
    return render_template('login.html')

@app.route('/login', methods=['POST']) 
def login():
    """Sign in user"""
    #to do: check validity of the user
    session['username'] = request.form.get('username')
    return redirect('/dashboard')

@app.route('/dashboard')
def view_dashboard():
    username = session['username'].upper()

    return render_template('/dashboard.html', username=username)

@app.route('/myprofile')
def user_profile():
    username = session['username']
    user = crud.get_user_by_username(username)
    print(user)
    return render_template('myprofile.html', user=user)
    
@app.route('/mysubscription')
def user_subscription():
    username = session['username']
    user = crud.get_user_by_username(username)
    user_id = user.id
    subscription = Subscription.query.filter(user_id == user_id).first()
    
    return render_template('mysubscription.html', subscription=subscription, user=user)
    
@app.route('/mystocks')
def user_stocks():
    username = session['username']
    user = crud.get_user_by_username(username)
    user_id = user.id
    subscription = Subscription.query.filter(user_id == user_id).first()
    
    return render_template('mystocks.html')
    
@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/login')

@app.route('/user/<username>')
def show_user_profile(username):
    """Show the user dashboard page for that user"""
    
    return f'Profile page for user: {username}'

@app.route('/allstocks')
def view_all_stocks():
    """view a list of all stocks to invest."""
    username = session.get('username')
    print(session)
    all_stocks = crud.get_all_stocks()
    
    return render_template("/allstocks.html", all_stocks=all_stocks)

@app.route('/plans')
def view_plans():
    """view a list of all subscriptions to choose from."""
    return render_template("/plans.html") 

@app.route('/checkplan')
def check_plan():
    subscription = True
    username = session['username']
    user = crud.get_user_by_username(username)
    return render_template("/checkplan.html", subscription=subscription) 


@app.route('/checkout')
def checkout():
    """view a list of all subscriptions to choose from."""
    return render_template("/checkout.html") 

@app.route('/create-checkout-session', methods=['POST']) 
def create_checkout_session():
    """checkout subscription payments"""
    # This is a sample test API key. Sign in to see examples pre-filled with your key.
    YOUR_DOMAIN = 'http://localhost:5000'
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': 2000,
                        'product_data': {
                            'name': 'Bronze Membership',
                            'images': ['static/img/Plenti_logo.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route('/blog')
def all_blogs():
    """show all blogs"""
    return render_template("blog.html")

@app.route('/blog/<int:id>')
def show_blog(id):
    
    return render_template("blog.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    DebugToolbarExtension(app)
