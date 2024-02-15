from pymongo import MongoClient
from bson.objectid import ObjectId

class OrderService:
    def __init__(self, db_client):
        self.db_client = db_client
        self.orders_collection = self.db_client.pizzas_orders_db.orders

    def getOrders(self):
        return list(self.orders_collection.find())

    def getOrdersByPizza(self, name):
        return list(self.orders_collection.find({"name": name}))
    
    def getTotalPizzasOrdered(self):
        return sum([order["quantity"] for order in self.getOrders()])
    
    def getOrdersCountByPizza(self, name):
        return sum(item["quantity"] for item in self.getOrdersByPizza(name))
    
    def getOrdersBySize(self, size):
        return sum([order["quantity"] for order in self.getOrders() if order["size"] == size])

    def getOrdersByCriteria(self, criteria):
        return list(self.orders_collection.find(criteria))
    
    def getTotalPriceOrders(self):
        return sum([order["price"] * order["quantity"] for order in self.getOrders()])

    def getPizzaMostOrdered(self):
        return list(self.orders_collection.aggregate([{"$group": {"_id": "$name", "total": {"$sum": "$quantity"}}}, {"$sort": {"total": -1}}]))[0]["_id"]

    def getSizePizzaMostOrdered(self):
        return list(self.orders_collection.aggregate([{"$group": {"_id": "$size", "total": {"$sum": 1}}}, {"$sort": {"total": -1}}]))[0]["_id"]

    def getPizzaMostIncome(self):
        return list(self.orders_collection.aggregate([{"$group": {"_id": "$name", "total": {"$sum": {"$multiply": ["$price", "$quantity"]}}}}, {"$sort": {"total": -1}}]))[0]["_id"]
if __name__ == "__main__":

    client = MongoClient('mongodb://mongodb:27017/')
    
    order_service = OrderService(client)

    print("Liste des commandes:")
    print(order_service.getOrders())

    print("Commandes pour la pizza Pepperoni:")
    print(order_service.getOrdersByPizza("Pepperoni"))

    print("Commandes de grande taille:")
    print(order_service.getOrdersBySize("large"))

    print("Commandes de pizza Margherita de grande taille:")
    criteria = {"name": "Pepperoni", "size": "large"}
    print(order_service.getOrdersByCriteria(criteria))

    print("Prix total des commandes:")
    print(order_service.getTotalPriceOrders())

    print("Nombre total de pizzas commandées:")
    print(order_service.getTotalPizzasOrdered())

    print("Nombre de pizzas Vegan commandées:")
    print(order_service.getOrdersCountByPizza("Vegan"))

    print("Nombre de commandes de grandes tailles:")
    print(order_service.getOrdersBySize("large"))

    print("Pizza la plus commandée:")
    print(order_service.getPizzaMostOrdered())

    print("Format de pizza la plus commandée:")
    print(order_service.getSizePizzaMostOrdered())

    print("Recette de pizza avec le plus de revenus:")
    print(order_service.getPizzaMostIncome())