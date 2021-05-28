import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user_resource import UserRegister
from resources.item_resource import Item, ItemList
from resources.store_resource import Store, StoreList

app = Flask(__name__)

#
uri = os.environ.get("DATABASE_URL", "sqlite:///data.db")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Turning off Flask SQL Alchemy Tracker because SQL Alchemy, the main library, has its own tracking
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')  # When we execute a post request to /register it will call the UserRegister class
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':  # Q: This allows us to import app without running app.run()
    from db import db
    db.init_app(app)
    app.run(debug=True)  # important to mention debug=True
