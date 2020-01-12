from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask
from ..config import Config

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://GMfobXB7CD:1mRCSNkKIV@remotemysql.com:3306/GMfobXB7CD' #add password in order for it to run

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    username = db.Column(db.String(120) , primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    img = db.Column(db.String(60), default='default.jpg') #TODO add image
    games = db.Column(db.Integer)
    wins = db.Column(db.Integer)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'email','img','games','wins')

user_schema = UserSchema()
users_schema = UserSchema(many=True)