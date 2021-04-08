"""server file for Plenti app"""

from flask import (Flask, render_template, request, flash, session, jsonify, redirect)
from model import connect_to_db, User, Stock
import crud
import json
import os
# import cloudinary.uploader
import math
from flask_sqlalchemy import SQLAlchemy
from jinja2 import StrictUndefined


# ALPHAVANTAGE_KEY = os.environ['ALPHAVANTAGE_KEY']

# cloudinary.config(
#   cloud_name = os.environ['CLOUDINARY_CLOUD_NAME'],  
#   api_key = os.environ['CLOUDINARY_API_KEY'],  
#   api_secret = os.environ['CLOUDINARY_API_SECRET'] 
# )

app = Flask(__name__)
app.secret_key = 'dev'

@app.route('/', defaults={'path': ''}) 
@app.route('/<path:path>') 
def show_homepage(path):
    """View the homepage."""
    
    return render_template('homepage.html')



# Replace this with routes and view functions!

""" API Routes"""
 


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
