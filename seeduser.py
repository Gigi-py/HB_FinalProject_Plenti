import os
import json
from random import choice, randint, sample
from datetime import datetime
import crud, api
from model import connect_to_db, db, User, Stock, Stockprice, Stockdetail, UserFavorite, Plan, Blog, Subscription, Stock_in_Subscription, Event, Comment
from server import app

db.session.query(User).delete()
db.session.query(Plan).delete()
db.session.query(Subscription).delete()
db.session.query(Blog).delete()

connect_to_db(app, echo=False)
db.create_all()

#SEED USER TABLE=================
with open('data/users.json') as f:
    user_data = json.loads(f.read())

users_in_db = []

for user in user_data:

    username, fname, lname, avatar, address = (
        user['username'],
        user['fname'],
        user['lname'],
        user['avatar'],
        user['address']
    )

    email = f'{username}@gmail.com'
    password = 'test'

    db_user = crud.create_user(app, username, fname, lname, email, password, avatar, address)
    users_in_db.append(db_user)

db.session.commit()

#SEED PLAN==========
plans = [{
    "name": "starter",
    "stocks_per_month": 10,
    "investment_per_month": 20
    },
    {
    "name": "pro",
    "stocks_per_month": 10,
    "investment_per_month": 50
    },
    {
    "name": "premium",
    "stocks_per_month": 10,
    "investment_per_month": 100
    }]

plans_in_db = []
for plan in plans:
    name, stocks_per_month, investment_per_month = (plan['name'], plan['stocks_per_month'], plan['investment_per_month'])
    db_plan = crud.create_plan(name, stocks_per_month, investment_per_month)
    plans_in_db.append(db_plan)

db.session.commit()

#SEED SUBSCRIPTION===========
subscriptions_in_db = []
user_name = users_in_db[0].username
plan_id = plans_in_db[0].id
subscription_start_timestamp = datetime.utcnow()
subscription_end_timestamp = datetime.utcnow()
db_subscription = crud.create_subscription(user_name, plan_id)
subscriptions_in_db.append(db_subscription)

db.session.commit()

#BLOGS===========

sample_articles = [{"title": "What is a Stock", "url": "https://learn.robinhood.com/articles/6FKal8yK9kk22uk65x3Jno/what-is-a-stock/"},
{"title": "What is a portfolio", "url":"https://learn.robinhood.com/articles/4vaR9PkTzes8u3ibLAWrD1/what-is-a-portfolio/"},
{"title": "What is an Initial Public Offering", "url": "https://learn.robinhood.com/articles/6UsdUrlnUvxiDpDT4D2bup/what-is-an-initial-public-offering-ipo/"},
{"title": "What is Venture Capital", "url": "https://learn.robinhood.com/articles/4XRFKEfckD73crXUgLBsoK/what-is-venture-capital/"},
{"title": "What is an Investment Company", "url": "https://learn.robinhood.com/articles/2FxgvV1Nt0LoTq59xJzj3/what-is-an-investment-company/"},
{"title": "What is a Stock Option", "url": "https://learn.robinhood.com/articles/YtqceruIQSiHncrlcecPL/what-is-a-stock-option/"}
]

articles_in_db = []
for article in sample_articles:
    title = article['title']
    url = article['url']

    article = Blog(title=title, url=url)
    articles_in_db.append(article)
    db.session.add(article)
    db.session.commit()
    
print(articles_in_db)

