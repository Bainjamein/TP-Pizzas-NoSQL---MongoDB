from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_bcrypt import Bcrypt
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'

class PizzaCustomerApi:
    def __init__(self, db_client):
        self.db_client = db_client
        self.customers_collection = self.db_client.pizzas_customers_db.customers
        self.bcrypt = Bcrypt()

    def createCustomer(self, login, password):
        hashed_password = self.bcrypt.generate_password_hash(password).decode('utf-8')
        new_customer = {
            "login": login,
            "password": hashed_password
        }
        result = self.customers_collection.insert_one(new_customer)
        return str(result.inserted_id)

    def verifyCustomer(self, login, password):
        customer = self.customers_collection.find_one({"login": login})
        if customer and self.bcrypt.check_password_hash(customer['password'], password):
            return str(customer['_id'])
        return None

    def verifyToken(self, token):
        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            customer_id = decoded_token['customer_id']
            return customer_id
        except jwt.ExpiredSignatureError:
            return 'Token expiré. Veuillez vous reconnecter.'
        except jwt.InvalidTokenError:
            return 'Token invalide. Veuillez vous reconnecter.'

    def getCustomer(self, oid):
        document = self.customers_collection.find_one({"_id": ObjectId(oid)}, {"_id": 0})
        if document:
            return document
        else:
            return None

if __name__ == "__main__":

    client = MongoClient('mongodb://mongodb3:27017/')
    
    customer_service = PizzaCustomerApi(client)

    @app.route('/auth/signup', methods=['POST'])
    def signup():
        data = request.json
        login = data.get('login')
        password = data.get('password')

        if not login or not password:
            return jsonify({'message': 'Veuillez fournir un email et un mot de passe'}), 400

        existing_customer = customer_service.customers_collection.find_one({"login": login})
        if existing_customer:
            return jsonify({'message': 'Cet email est déjà utilisé'}), 400

        # Création d'un nouveau client
        customer_id = customer_service.createCustomer(login, password)

        return jsonify({'message': 'Compte client créé avec succès', 'customer_id': customer_id}), 201


    @app.route('/auth/signin', methods=['POST'])
    def signin():
        data = request.json
        login = data.get('login')
        password = data.get('password')

        if not login or not password:
            return jsonify({'message': 'Veuillez fournir un email et un mot de passe'}), 400

        customer_id = customer_service.verifyCustomer(login, password)

        if customer_id:
            token = jwt.encode({'customer_id': str(customer_id), 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])
            return jsonify({'token': token})
        else:
            return jsonify({'message': 'Connexion échouée. Veuillez vérifier vos identifiants'}), 401


    @app.route('/auth/verify', methods=['POST'])
    def verify():
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token manquant'}), 401

        token_parts = token.split()
        if len(token_parts) != 2 or token_parts[0].lower() != 'bearer':
            return jsonify({'message': 'Format de token invalide'}), 401

        customer_id = customer_service.verifyToken(token_parts[1])

        customer = customer_service.getCustomer(customer_id)
        if customer:
            return jsonify('Vous etes un utilisateur valide')
        else:
            return jsonify({"error": "Vous n'etes pas un utilisateur valide"}), 404
    
    @app.route('/customers/me', methods=['GET'])
    def get_customer_data():
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token manquant'}), 401
        
        token_parts = token.split()
        if len(token_parts) != 2 or token_parts[0].lower() != 'bearer':
            return jsonify({'message': 'Format de token invalide'}), 401

        customer_id = customer_service.verifyToken(token_parts[1])

        customer = customer_service.getCustomer(customer_id)
        if customer:
            return jsonify(customer)
        else:
            return jsonify({"error": "Customer not found"}), 404

        return null

    app.run(debug=True, host='0.0.0.0', port=5002)
