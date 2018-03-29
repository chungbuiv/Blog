from flask_login import UserMixin

from models.base import db, ModelMethods


class User(UserMixin, db.Model, ModelMethods):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(80))
    phone = db.Column(db.String(40))
    job = db.Column(db.String(40))
    role = db.Column(db.Boolean)  # True: Facebook user; False: Google user

    def __init__(self, email, role):
        self.email = email
        self.role = role

    def get_id(self):
        return self.id

    def __repr__(self):
        return "User: {} {}".format(self.email, self.role)
