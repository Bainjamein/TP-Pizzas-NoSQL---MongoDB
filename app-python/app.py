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

    def getOrdersBySize(self, size):
        return list(self.orders_collection.find({"size": size}))

    def getOrdersByCriteria(self, criteria):
        return list(self.orders_collection.find(criteria))
    
    def getTotalPriceOrders(self):
        return list(self.orders_collection.aggregate([{"$group": {"_id": None, "total": {"$sum": "$price"}}}]))[0]["total"]

    def getPizzaMostOrdered(self):
        return list(self.orders_collection.aggregate([{"$group": {"_id": "$name", "total": {"$sum": 1}}}, {"$sort": {"total": -1}}]))[0]["_id"]

    def getSizePizzaMostOrdered(self):
        return list(self.orders_collection.aggregate([{"$group": {"_id": "$size", "total": {"$sum": 1}}}, {"$sort": {"total": -1}}]))[0]["_id"]

    def getPizzaMostIncome(self):
        return list(self.orders_collection.aggregate([{"$group": {"_id": "$name", "total": {"$sum": "$price"}}}, {"$sort": {"total": -1}}]))[0]["_id"]
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

    print("Nombre de pizzas Vegan commandées:")
    print(len(order_service.getOrdersByPizza("Vegan")))

    print("Nombre de commandes de grandes tailles:")
    print(len(order_service.getOrdersBySize("large")))

    print("Pizza la plus commandée:")
    print(order_service.getPizzaMostOrdered())

    print("Format de pizza la plus commandée:")
    print(order_service.getSizePizzaMostOrdered())

    print("Recette de pizza avec le plus de revenus:")
    print(order_service.getPizzaMostIncome())