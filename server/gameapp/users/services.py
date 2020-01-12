from .models import User,db,users_schema,user_schema
from flask import jsonify
import json
import hashlib
import jwt
from ..config import Config

def addUser(username,password,email):
    exists = User.query.filter_by(username=username).first()
    mailex = User.query.filter_by(email=email).first()
    if exists is None and mailex is None:
        hashedPassword = hashPassword(password)
        user = User(username=username, password=hashedPassword, email=email)

        db.session.add(user)
        db.session.commit()

        response = {
            'message' : 'User added to db'
        }
        return jsonify(response),200
    elif mailex is not None:
        response = {
            'message': 'Email belongs to another user'
        }
    else:
        response={
            'message':'Username already exists'
        }
    return jsonify(response),409

def getUser(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        response = {
                'message' : 'No user in database with this username'
        }
        return response,404

    results = user_schema.dumps(user)
    results = results.replace('[','').replace(']','')
    data = json.loads(results)
    return data

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
        return jsonify(response),401
    else:
        key = Config.SECRET_KEY #get the secrete key
        token = jwt.encode({'user':username},key) #generate token
        return jsonify({'token': token.decode('utf-8')}),200 #python encodes it in bytes

def deleteUser(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        response = {
            'message' : 'User is deleted'
        }
        return jsonify(response),200
    else:
        response = {
            'message' : 'User does not exist'
        }
        return jsonify(response),404

def updateUser(username,new_username,img):
    user = User.query.filter_by(username=username).first()
    exist = User.query.filter_by(username=new_username).first()
    change = False
    if username != new_username and exists is None:
        user.username = new_username
        change = True
    elif exists is not None:
        response = {
            'message' : 'Invalid username'
        }
        return jsonify(response),500
    if user.img != img:
        user.img = img
        change = True  
    if change == True: 
        db.session.commit()
        response = {
            'message' : 'Update was successful'
        }
    else:
        response = {
            'message' : 'Nothing was updated'
        }
    return jsonify(response),200

def hashPassword(password):
    hashpass = hashlib.md5() # create md5 hash
    hashpass.update(password.encode()) #update it with the password
    return hashpass.hexdigest() #return the hex
