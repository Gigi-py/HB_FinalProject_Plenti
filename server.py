"""server file for Plenti app"""

from flask import (Flask, render_template, request, flash, session, jsonify, redirect)
from model import connect_to_db, User, Stock, Subscription, Stock_in_Subscription
import crud
import json
import os
import math
from flask_sqlalchemy import SQLAlchemy
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'dev'

@app.route('/') 
def homepage():
    """View the homepage."""
    
    return render_template('homepage.html')


""" API Routes"""
 

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
