"""Demonstration backend for AJAX."""

import random
import time
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

MELONS = ["Cantaloupe", "Honeydew", "Watermelon", "Musk"]
ADJECTIVES = [
        "Juicy",
        "Delicious",
        "Aromatic",
        "Ripe",
        "Flavorful",
        "Reasonably-Priced",
        "Artisanally Hand-Crafted",
]
CITY_DELIVERY_INFO = {
    "SF": {
        "days": 1,
        "cost": 3.00,
    },
    "Oak": {
        "days": 2,
        "cost": 5.00,
    },
    "other": {
        "days": 5,
        "cost": 10.00,
    },
}


@app.route("/")
def index():
    """Homepage."""

    return render_template("test-js-jq.html", melons=MELONS)


@app.route("/adjective")
def get_random_adjective():
    """Return a simple adjective."""

    return random.choice(ADJECTIVES)


@app.route("/status")
def get_order_status():
    """Get order status."""

    order_number = request.args.get("order")

    if order_number == "123":
        return random.choice(["LATE", "SUPER-LATE"])
    else:
        return "ON-TIME"


@app.route("/new-order", methods=["POST"])
def add_order():
    """Add a melon order to our database."""

    melon_type = request.form.get("type")
    amount = request.form.get("amount")

    return "Your order has been confirmed"


@app.route("/delivery-info.json")
def get_delivery_info():
    """Get delivery info."""

    address = request.args.get("address")
    city = request.args.get("city")

    if city in CITY_DELIVERY_INFO:
        return jsonify(CITY_DELIVERY_INFO[city])
    else:
        return jsonify(CITY_DELIVERY_INFO["other"])


@app.route("/melon-info.py")
def melon_info_py():
    """This route will fail!"""

    melon_1 = {
        "id": "watermelon",
        "name": "Watermelon",
        "price": 5.00,
        "available": True,
        "countries": ["US", "CA", "MX"]
    }
    melon_2 = {
    "id": "canteloupe",
    "name": "canteloupe",
    "price": 50.00,
    "available": False,
    "countries": []
    }


    return [melon_1, melon_2]


@app.route("/melon-info.json")
def melon_info():
    """Return info about a melon as JSON."""

    # In real life, we would probably get this info
    # from our database
    melon_1 = {
        "id": "watermelon",
        "name": "Watermelon",
        "price": 5.00,
        "available": True,
        "countries": ["US", "CA", "MX"]
    }
    melon_2 = {
    "id": "canteloupe",
    "name": "canteloupe",
    "price": 50.00,
    "available": False,
    "countries": []
    }

    return jsonify([melon_1, melon2])


@app.after_request
def sleep(res):
    """Simulate a slow server."""

    time.sleep(2)
    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
