from flask_login import UserMixin

from .app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    pw_hash = db.Column(db.String(100))

    def __init__(self, email, pw_hash):
        self.email = email
        self.pw_hash = pw_hash
