import datetime

from flask_login import UserMixin

from .database import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    pw_hash = db.Column(db.String(100))
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    search_infos = db.relationship('SearchInfo')

    def __init__(self, email, pw_hash):
        self.email = email
        self.pw_hash = pw_hash


class SearchInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    phrase = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, phrase, date, user_id):
        self.phrase = phrase
        self.date = date
        self.user_id = user_id

