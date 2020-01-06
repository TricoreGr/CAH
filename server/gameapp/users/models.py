from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://apostoles:password@localhost/users' #create a user table in username@localhost

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    username = db.Column(db.String(120) , primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    img = db.Column(db.String(60), nullable=False, default='default.jpg') #TODO add image
    games = db.Column(db.Integer)
    wins = db.Column(db.Integer)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'email','img','games','wins')

user_schema = UserSchema()
users_schema = UserSchema(many=True)