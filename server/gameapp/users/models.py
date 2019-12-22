from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql:///users' #create a user table in username@localhost

db = SQLAlchemy(app)

class User(db.Model):
    username = db.Column(db.String(120) , primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    img = db.Column(db.String(60), nullable=False, default='default.jpg') #TODO add image
    games = db.Column(db.Integer)
    wins = db.Column(db.Integer)

    def __repr__(self):
        user = {"username":self.username, "password":self.password, 
        "email":self.email,"img":self.img, "games":self.games, "wins":self.wins}
        return str(user)

    def __json__(self):
        return ['username','password','email','img','games','wins']