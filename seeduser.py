import os
import json
from random import choice, randint, sample
from datetime import datetime
import crud, api
from model import connect_to_db, db, User, Plan, Subscription
from server import app

connect_to_db(app, echo=False)

#USER ==========
db.session.query(User).delete()
db.session.commit()

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

#SEED PLAN
db.session.query(Plan).delete()
db.session.commit()

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
db.session.query(Subscription).delete()
db.session.commit()

subscriptions_in_db = []
user_id = users_in_db[0].id
plan_id = plans_in_db[0].id
subscription_start_timestamp = datetime.utcnow()
subscription_end_timestamp = datetime.utcnow()
db_subscription = crud.create_subscription(user_id, plan_id, subscription_start_timestamp, subscription_end_timestamp)
subscriptions_in_db.append(db_subscription)

db.session.commit()
