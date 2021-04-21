import os
import json
from random import choice, randint, sample
from datetime import datetime
import crud, api
from model import connect_to_db, db, User, Stock, Stockprice, Stockdetail, Stocknews, UserFavorite, Plan, Blog, Subscription, Stock_in_Subscription, Event, Comment
from server import app


connect_to_db(app, echo=False)
db.create_all()
db.session.query(Stockdetail).delete()
db.session.query(Stocknews).delete()
db.session.query(User).delete()
db.session.query(Plan).delete()
db.session.query(Subscription).delete()

db.session.commit()

# #STOCK DETAIL TABLE==========
# stockdetails_in_db = []
# stock_details_data = api.get_stock_details()

# for stock_detail in stock_details_data:
#     logo, cik, country, industry, marketcap, employees, phone, ceo, url, description, exchange, name, symbol, hq_address, hq_state, hq_country, tags, similar=(
#             stock_details_data["logo"],
#         stock_details_data["cik"],
#         stock_details_data["country"], 
#         stock_details_data["industry"],
#         stock_details_data["marketcap"],
#         stock_details_data["employees"],
#         stock_details_data["phone"],
#         stock_details_data["ceo"],
#         stock_details_data["url"], 
#         stock_details_data["description"],
#         stock_details_data["exchange"],
#         stock_details_data["name"],
#         stock_details_data["symbol"],
#         stock_details_data["hq_address"],
#         stock_details_data["hq_state"],
#         stock_details_data["hq_country"],
#         stock_details_data["tags"],
#         stock_details_data["similar"]
#             )

# db_stockdetail = crud.create_stockdetail(logo, cik, country, industry, marketcap, employees, phone, ceo, url, description, exchange, name, symbol, hq_address, hq_state, hq_country)
# stockdetails_in_db.append(db_stockdetail)

#STOCK NEWS TABLE================
stocknews_in_db = []
stock_news_data = api.get_news_details()

for stock_news in stock_news_data:
    symbol, timestamp, title, url, source, summary, image = (
        stock_news_data["symbols"],
        stock_news_data["timestamp"],
        stock_news_data["title"],
        stock_news_data["url"],
        stock_news_data["source"],
        stock_news_data["summary"],
        stock_news_data["image"])
     
    db_stocknews = crud.create_stocknews(symbol, timestamp, title, url, source, summary, image)
    stocknews_in_db.append(db_stocknews)
