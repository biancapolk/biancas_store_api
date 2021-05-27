import os

from db import db
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user_resource import UserRegister
from resources.item_resource import Item, ItemList
from resources.store_resource import Store, StoreList

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config[
    'SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Turning off Flask SQL Alchemy Tracker because SQL Alchemy, the main library, has its own tracking
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':  # Q: This allows us to import app without running app.run()
    db.init_app(app)
    app.run(debug=True)  # important to mention debug=True
