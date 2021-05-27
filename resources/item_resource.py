from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item_model import ItemModel



class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id!"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)     # (name, data['price'])

        try:
            item.save_to_db() #Not sure I understand why this isnt Item.insert(), also is there a better way to save to the db
        except Exception as e:
            print(e)
            return {"message": "An error occurred inserting the item."}, 500 # Internal server error

        return item.json(), 201


    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': "Item deleted"}
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            try:
                item = ItemModel(name, **data)
            except:
                return {"message": "An error occurred inserting the item."}
        else:
            try:
                item.price = data['price']  # should I add store id?
            except:
                return {"message": "An error occurred updating the item."}

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
       # return {'items': [item.json() for item in ItemModel.query.all()]}
       return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}

