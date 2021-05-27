from db import db


# Internal representation that contain the properties of an item
class StoreModel(db.Model):
    # Creating a model for the DB here, tells it how to read it
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')  # Allows Store to access the items that have its id, but the lazy variable prevents it from creating a new object for all items
    def __init__(self, name):
        self.name = name

    # Return JSON representation of the model
    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}  # until we call the json method we are not looking into the stores, .all() retireve all items

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  # This translates to some SQL code: SELECT * FROM items WHERE name=name LIMIT 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

