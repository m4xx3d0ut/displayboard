from flask_login import UserMixin
from . import db


# Creates user account in database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    secret = db.Column(db.String(100))
    permissions = db.Column(db.String(100))