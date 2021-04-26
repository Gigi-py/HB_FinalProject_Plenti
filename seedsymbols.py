import os
import json
from random import choice, randint, sample
import requests, json, csv, time
from datetime import datetime
import crud, api
from model import connect_to_db, db, User, Symbol, Stock, Stockprice, Stockdetail, Stocknews, UserFavorite, Plan, Blog, Subscription, Stock_in_Subscription, Event, Comment
from server import app

os.system('dropdb stocks')
os.system('createdb stocks')

connect_to_db(app, echo=False)
db.create_all()

AA_API_KEY = os.environ['AA_API_KEY']

url = 'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey='+ AA_API_KEY
res = requests.get(url) # double check this line, might be a duplicate to line 65
decoded = res.content.decode('utf-8')

csv_read = csv.reader(decoded.splitlines(), delimiter=',')
all_symbols = list(csv_read)

for symbol in all_symbols:
    symbol = Symbol(symbol = symbol[0])
    db.session.add(symbol)
    db.session.commit()

print("Finished adding all stock symbols")
