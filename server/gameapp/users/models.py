from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:///user.db'

db = SQLAlchemy(app)

class User(db.Model):
    username = db.Column(db.String(120) , primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    img = db.Column(db.String, nullable=False, default='default.jpg') #TODO add image
    games = db.Column(db.Integer)
    wins = db.Column(db.Integer)
