from flask import Flask, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import requests

app = Flask(__name__)

class PizzaShopApi:
    def __init__(self, db_client):
        self.db_client = db_client
        self.orders_collection = self.db_client.pizzas_menu_db.cart



if __name__ == "__main__":
    client = MongoClient('mongodb://mongodb4:27020/')
    
    pizza_service = PizzaShopApi(client)