#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

# Restaurants routes
@app.route('/restaurants')
def get_restaurants():
    # return [r.to_dict() for r in Restaurant.query.all()], 200
    restaurants = []
    for r in Restaurant.query.all():
        restaurants.append({
            "id": r.id,
            "name": r.name,
            "address": r.address
        })
    return restaurants, 200

@app.route('/restaurants/<int:id>')
def get_restaurant(id:int):
    restaurant = Restaurant.query.where(Restaurant.id == id).first()
    if restaurant:
        return restaurant.to_dict(), 200
    return {'error': 'Restaurant not found'}, 404

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id:int):
    restaurant = Restaurant.query.where(Restaurant.id == id).first()
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return {}, 204
    return {'error': 'No restaurant found with the provided id'}, 404

# Pizzas routes
@app.route('/pizzas')
def get_pizzas():
    # return [ p.to_dict() for p in Pizza.query.all() ], 200
    pizzas = []
    for p in Pizza.query.all():
        pizzas.append({
            "id": p.id,
            "name": p.name,
            "ingredients": p.ingredients
        })
    return pizzas, 200

# restaurant_pizzas routes
@app.route('/restaurant_pizzas', methods=['POST'])
def post_pizza():
    try:
        restaurant_pizza = RestaurantPizza(price=request.json['price'], restaurant_id=request.json['restaurant_id'], pizza_id=request.json['pizza_id'])
        db.session.add(restaurant_pizza)
        db.session.commit()
        return restaurant_pizza.to_dict(), 201
    except ValueError:
        return {'errors': ['validation errors']}, 400

if __name__ == "__main__":
    app.run(port=5555, debug=True)
