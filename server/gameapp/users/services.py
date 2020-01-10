from .models import User,db,users_schema,user_schema
from flask import jsonify
import json
import hashlib
import jwt
from ..config import Config

def addUser(username,password,email,img):
    exists = User.query.filter_by(username).first()
    if exists is None:
        hashedPassword = hashPassword(password)
        user = User(username=username, password=hashedPassword, email=email, img=img)

        db.session.add(user)
        db.session.commit()

        response = {
            'message' : 'User added to db'
        }
        return jsonify(response)
    else:
        response = {
            'message': 'User already exists'
        }
        return jsonify(response)

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

def getUserByJWToken(token):
    username = jwt.decode(token,Config.SECRET_KEY)['user']
    return getUser(username)

def checkCreds(username,password):
    hashedPassword = hashPassword(password)
    result = User.query.filter_by(username=username).filter_by(password=hashedPassword).first()
    if result is None:
        response = {
            'message' : 'Invalid credentials'
        }
        return jsonify(response)
    else:
        key = Config.SECRET_KEY #get the secrete key
        token = jwt.encode({'user':username},key) #generate token
        return jsonify({'token': token.decode('utf-8')}) #python encodes it in bytes

def deleteUser(token):
    username = getUserByJWToken(token)
    user = User.query.filter_by(username).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        response = {
            'message' : 'User is deleted'
        }
        return jsonify(response)
    else:
        response = {
            'message' : 'Cannot delete user'
        }

def hashPassword(password):
    hashpass = hashlib.md5() # create md5 hash
    hashpass.update(password.encode()) #update it with the password
    return hashpass.hexdigest() #return the hex
