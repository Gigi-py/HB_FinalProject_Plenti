"""FOCUS ON MY VISION OF WHAT I WANT TO BUILD AND GAIN THE SKILLS TO ACHIEVE IT."""


from flask import Flask, render_template, url_for, request, flash, session, jsonify, redirect
from model import connect_to_db, User, Stock, Stockprice, UserFavorite, Plan, Blog, Subscription, Stock_in_Subscription, Event, Comment
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

#AUTHENTICATION CONFIG:
login_manager = LoginManager()
login_manager.init_app(app)

# Blueprint Configuration

auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)

@main_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    """Logged-in User Dashboard."""
    return render_template(
        'dashboard.jinja2',
        title='Flask-Login Tutorial.',
        template='dashboard-template',
        current_user=current_user,
        body="You are now logged in!"
    )

# @app.route('/') 
# def index():
#     """Welcome page"""
#     return render_template('homepage.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
            return redirect(url_for('main_bp.dashboard'))

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main_bp.dashboard'))
        flash('Invalid username/password combination')
        return redirect(url_for('auth_bp.login'))

    return render_template(
        'login.html',
        form=form,
        title='Log in.',
        template='login-page',
        body="Log in with your User account."
    )

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(
                name=form.name.data,
                email=form.email.data,
                website=form.website.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user)  # Log in as newly created user
            return redirect(url_for('main_bp.dashboard'))
        flash('A user already exists with that email address.')
 
    return render_template(
        'signup.jinja2',
        title='Create an Account.',
        form=form,
        template='signup-page',
        body="Sign up for a user account."
    )

@main_bp.route("/logout")
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))


@app.route('/user/<username>')
def show_user_profile(username):
    """Show the user dashboard page for that user"""
    
    return f'Profile page for user: {username}'

# @app.route('/signup', methods=['POST'])
# def register_user():
#     """Create a new user account."""

#     username = request.form.get('username')
#     fname = request.form.get('fname')
#     lname = request.form.get('lname')
#     email = request.form.get('email')
#     password = request.form.get('password')
#     about = request.form.get('about')
#     image_url = None
#     city = None

#     user = crud.get_user_by_email(email)
#     if not user:
#         user = crud.create_user(username, fname, lname, image_url, city, about, password)
#         flash('Account created! Please log in.')
#     else:
#         flash('An account has already been used with this email, please login.')

#     return render_template('homepage.html',person=first_name )

#     # Check if user with that username already exists
    
    
#     session['user_id'] = user.user_id 
    
#     return redirect('/allstocks')

@app.route('/allstocks')
def view_all_stocks():
    """view a list of all stocks to invest."""
    return render_template("/allstocks.html")

# @app.route('/stock/<symbol>')
# def view_all_stocks():
#     """view a list of all stocks to invest."""
#     return f'Profile page for stock: {symbol}'

@app.route('/dashboard')
def view_dashboard():
    """view a list of all stocks to invest."""
    return render_template("/user_dashboard.html")

@app.route('/plans')
def view_subscriptions():
    """view a list of all subscriptions to choose from."""
    return render_template("/plans.html") 

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

# @app.route('/blog/<int:id>')
# def show_blog(id):
    
#     return render_template("blog.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    DebugToolbarExtension(app)
