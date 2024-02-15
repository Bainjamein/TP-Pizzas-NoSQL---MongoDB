from pymongo import MongoClient
from bson.objectid import ObjectId

class OrderService:
    def __init__(self, db_client):
        self.db_client = db_client
        self.orders_collection = self.db_client.pizzas_orders_db.orders

    def getOrders(self):
        return list(self.orders_collection.find())

    def getOrdersByPizza(self, pizza_name):
        return list(self.orders_collection.find({"name": pizza_name}))

    def getOrdersBySize(self, size):
        return list(self.orders_collection.find({"size": size}))

    def getOrdersByCriteria(self, criteria):
        return list(self.orders_collection.find(criteria))


# Exemple d'utilisation
if __name__ == "__main__":
    # Connexion à la base de données MongoDB
    client = MongoClient('mongodb://mongodb:27017/')
    
    # Instanciation du service de commande avec le client MongoDB
    order_service = OrderService(client)

    # Exemples de requêtes
    print("Liste des commandes:")
    print(order_service.getOrders())

    print("Commandes pour la pizza Pepperoni:")
    print(order_service.getOrdersByPizza("Pepperoni"))

    print("Commandes de grande taille:")
    print(order_service.getOrdersBySize("large"))

    # Exemple d'utilisation de la méthode unique avec un critère de filtre
    print("Commandes de pizza Margherita de grande taille:")
    criteria = {"name": "Pepperoni", "size": "large"}
    print(order_service.getOrdersByCriteria(criteria))
