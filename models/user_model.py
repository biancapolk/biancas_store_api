import sqlite3
from db import db


# Create user class - MODELS - internal representation
class UserModel(db.Model):
    # Creating a model for the DB here, tells it how to read it
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    # Finds user by username in the db
    @classmethod
    def find_by_username(cls, username):  # finds username

        return cls.query.filter_by(username=username).first()

    # Finds user by username in the db
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
