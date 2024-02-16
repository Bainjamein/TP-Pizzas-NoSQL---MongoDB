from flask import Flask, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

class PizzaMenuApi:
    def __init__(self, db_client):
        self.db_client = db_client
        self.orders_collection = self.db_client.pizzas_menu_db.menu

    def getPizzas(self):
        return list(self.orders_collection.find({}, {"_id": 0}))

    def getPizza(self, oid):
        document = self.orders_collection.find_one({"_id": ObjectId(oid)}, {"_id": 0})
        if document:
            return document
        else:
            return None

    def getPizzaDeclination(self, oid, size):
        document = self.orders_collection.find_one({"_id": ObjectId(oid)}, {"_id": 0, "declinations": 1})
        if document:
            for declination in document["declinations"]:
                if declination["size"] == size:
                    return {"name": document["name"], "size": declination["size"], "price": declination["price"]}
            return None
        

if __name__ == "__main__":
    client = MongoClient('mongodb://mongodb2:27017/')
    
    pizza_service = PizzaMenuApi(client)

    @app.route('/pizzas', methods=['GET'])
    def pizzas():
        pizzas = pizza_service.getPizzas()
        return jsonify(pizzas)
    
    @app.route('/pizzas/<oid>', methods=['GET'])
    def pizza(oid):
        pizza = pizza_service.getPizza(oid)
        if pizza:
            return jsonify(pizza)
        else:
            return jsonify({"error": "Pizza not found"}), 404
    
    @app.route('/pizzas/<oid>/declinations/<size>', methods=['GET'])
    def pizzaDeclination(oid, size):
        pizza = pizza_service.getPizzaDeclination(oid, size)
        if pizza:
            return jsonify(pizza) 
        else:
            return jsonify({"error": "Pizza not found"}), 404

    app.run(debug=True, host='0.0.0.0', port=5001)
