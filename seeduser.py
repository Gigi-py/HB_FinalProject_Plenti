import os
import json
from random import choice, randint, sample
from datetime import datetime
import crud, api
from model import connect_to_db, db, User
from server import app

connect_to_db(app, echo=False)
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

    db_user = crud.create_user(username, fname, lname, email, password, avatar, address)
    users_in_db.append(db_user)

db.session.commit()