from app import db
from flask_login import UserMixin


class Users(UserMixin, db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    email = db.Column(db.String, unique=True)    
    password = db.Column(db.String)
    isDriver = db.Column(db.Integer)

    def get_id(self):
        try:
            return str(self.userId)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

class Products(db.Model):

    __tablename__ = 'Products'
    productId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    imageURL = db.Column(db.String)
    store = db.Column(db.String)

