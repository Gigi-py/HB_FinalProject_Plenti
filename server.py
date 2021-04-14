"""server file for Plenti app"""

from flask import (Flask, render_template, request, flash, session, jsonify, redirect)
from model import connect_to_db, User, Stock, Subscription, Stock_in_Subscription
from random import sample, choice
import crud
import json
import os
import math
from flask_sqlalchemy import SQLAlchemy
from jinja2 import StrictUndefined
import stripe

stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'


app = Flask(__name__)
app.secret_key = 'dev'
connect_to_db(app)

@app.route('/') 
def homepage():
    """Welcome page"""
    quote_of_the_day = choice(crud.get_quote())
    return render_template('homepage.html', quote = quote_of_the_day)

@app.route('/signin', methods=['POST'])
def login():
    """login for existing user"""
    username = request.form.get('username')
    password = request.form.get('password')

    if password == 'test' and username == 'JLo':
        session['logged_in'] = True
        return redirect('/allstocks')
    # else:
    #     flash('wrong password!')
    #     return redirect('homepage.html')


@app.route('/signup', methods=['POST'])
def register_user():
    """Create a new user account."""

    username = request.form.get('username')
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')
    about = request.form.get('about')
    image_url = None
    city = None

    # Check if user with that username already exists
    user = crud.get_user_by_username(username)
    if user:
        return jsonify({
                'status': 'error',
                'message': 'Username already exists. Please pick a different one.'
        })

    user = crud.get_user_by_email(email)
    if user:
        return jsonify({
                'status': 'error',
                'message': 'Account with that email already exists.'
        })

    user = crud.create_user(username, fname, lname, image_url, city, about, password)
    flash('Account created! Please log in.')
    
    session['user_id'] = user.user_id 
    
    return redirect('/allstocks')

@app.route('/allstocks')
def view_all_stocks():
    """view a list of all stocks to invest."""
    return render_template("/allstocks.html")

@app.route('/subscriptions')
def view_all_subscriptions():
    """view a list of all subscriptions to choose from."""
    return render_template("/subscriptions.html") 

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
                            'images': ['https://i.imgur.com/EHyR2nP.png'],
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
