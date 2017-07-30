


#definyng my database
from flask import Flask
from app import app,db
from passlib.apps import custom_app_context as pwd_context


#the abstraction used for db
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    active = db.Column(db.Boolean)

    def __init__(self, nickname, email, pwd, active = True):
        self.password_hash = self.hash_password(pwd)
        self.nickname = nickname
        self.active = active

    def hash_password(self, password):
        return  pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

    #Login related functions below, the assumption follow`s 
    #if we get 2 here, the user are validate
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
