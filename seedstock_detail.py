import os
import json
from random import choice, randint, sample
from datetime import datetime
import crud, api
from model import connect_to_db, db, Stock, Stockprice, Stockdetail
from server import app, bcrypt

connect_to_db(app, echo=False)
db.session.query(Stockdetail).delete()
db.session.commit()

db.create_all()

symbol = 'PYPL'
stockdetails_in_db = []
stock_details_data = api.get_stock_details(symbol)

stock_id = Stock.query.filter(Stock.symbol == symbol).first().id

(logo, cik, country, industry, marketcap, employees, phone, ceo, url,
    description, exchange, name, symbol, hq_address, hq_state, hq_country, tags, similar)=(
        stock_details_data["logo"],
      stock_details_data["cik"],
      stock_details_data["country"], 
      stock_details_data["industry"],
      stock_details_data["marketcap"],
      stock_details_data["employees"],
      stock_details_data["phone"],
      stock_details_data["ceo"],
      stock_details_data["url"], 
      stock_details_data["description"],
      stock_details_data["exchange"],
      stock_details_data["name"],
      stock_details_data["symbol"],
      stock_details_data["hq_address"],
      stock_details_data["hq_state"],
      stock_details_data["hq_country"],
      stock_details_data["tags"],
      stock_details_data["similar"]
        )

stock_detail = Stockdetail(stock_id=stock_id, logo=logo,
cik=cik,
country=country,
industry=industry,
marketcap=marketcap,
employees=employees,
phone=phone,
ceo=ceo,
url=url,
description=description,
exchange=exchange,
name=name,
symbol=symbol,
hq_address=hq_address,
hq_state=hq_state,
hq_country=hq_country)

db_stockdetail = crud.create_stockdetail(stock_id, logo, cik, country, industry, marketcap, employees, phone, ceo, url,
                    description, exchange, name, symbol, hq_address, hq_state, hq_country)
stockdetails_in_db.append(db_stockdetail)

db.session.add(stock_detail)
db.session.commit()


