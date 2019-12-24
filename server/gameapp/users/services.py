from .models import User,db,users_schema,user_schema
from flask import jsonify
import json

def addUser(username,password,email,img):
    user = User(username=username, password=password, email=email, img=img)
    db.session.add(user)
    db.session.commit()
    print("User added")

def getUsers():
    users = User.query.all()
    if users is None:
        response = {
            'message' : 'No users in database'
        }
        return jsonify(response), 404
    results = users_schema.dumps(users)
    results = results.replace('[','').replace(']','')
    data = json.loads(results)
    return jsonify(data)

def getUser(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        response = {
                'message' : 'No user in database with this username'
        }
        return jsonify(response), 404
    results = user_schema.dumps(user)
    results = results.replace('[','').replace(']','')
    data = json.loads(results)
    return jsonify(data)
