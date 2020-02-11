from .models import usersCollection,userModel
from flask import jsonify, Response
import json
import jwt
from flask import jsonify, Response
from bson.json_util import dumps
from bson import json_util, BSON
from ..config import Config
from bson.objectid import ObjectId
import hashlib

def getUsers():
    try:
        users = []
        cursor = usersCollection.find({})
        for document in cursor:
            users.append(document)
        return Response(json.dumps({'output': users}, default=json_util.default),
                        mimetype='application/json')
    except Exception as e:
        print(e)
        response = {
            'message': 'Could not return tables'
        }
        return response, 500


def addUser(username,password,email):
    try:
        userExists = usersCollection.find_one({"username": username})
        if userExists is not None:
            return {'message': 'User already exists'}, 409

        mailExists = usersCollection.find_one({"email": email})
        if mailExists is not None:
            return {'message': 'A user with this email already exists'}, 409

        hashedPassword = hashPassword(str(password))
        user = userModel(username, hashedPassword, email)
        usersCollection.insert_one(user)
        
        key = Config.SECRET_KEY #get the secret key
        token = jwt.encode({'user':username},key).decode('utf-8') #generate token

        return Response(json.dumps({'user': user, 'token':token}, default=json_util.default),
                        mimetype='application/json')   
    except Exception as e:
        print(e)
        return {"message": "Server error"}, 500

def hashPassword(password):
    password = str(password)
    h = hashlib.md5(password.encode('utf-8'))
    return h.hexdigest()

def getUser(uname):
    try:
        user = usersCollection.find_one({'username':uname})
        if user is None:
            return {'message':'User was not found'}, 404
        return Response(json.dumps({'user': user}, default=json_util.default),
                        mimetype='application/json')
    except Exception as e:
        print(e)
        return {"message": "Server error"}, 500

def getUserByJWToken(token):
    username = jwt.decode(token,Config.SECRET_KEY)['user']
    return getUser(username)

def checkCreds(username,password):
    try:
        hashedPassword = hashPassword(password)
        user = usersCollection.find_one({'username':username})
        if user is None:
            return {'message':'The is no user with this username'}, 404
        userWithPassword = usersCollection.find_one({'password':hashedPassword})
        if userWithPassword is None:
            return {'message':'Invalid credentials'}, 401
        key = Config.SECRET_KEY
        token = jwt.encode({'user':username},key).decode('utf-8')   
        return Response(json.dumps({'user': userWithPassword, 'token':token}, default=json_util.default),
                            mimetype='application/json')
    except Exception as e:
        print(e)
        return {"message": "Server error"}, 500

def deleteUser(username):
    try:
        query = {
            'username' : username
        }
        user = usersCollection.find_one(query)
        usersCollection.delete_one(query)
        return Response(json.dumps({'user': user}, default=json_util.default),
                        mimetype='application/json')
    except Exception as e:
        print(e)
        pass

def updateUser(username, img):
    try:
        user = usersCollection.find_one({'username':username})
        if user is None:
            return {'message':'There is no user with this username'}, 404 
        return updateUserImg(username, img)
    except Exception as e:
        print(e)
        return {"message": "Server error"}, 500


def updateUserImg(username, img):
    try:
        user_image = usersCollection.find_one({'username':username})['img']
        if user_image == img:
            return {'message':'The new image is the same as the old one'}, 400
        new_vals = {
            "$set" : {"img": img}
        }
        usersCollection.update_one({'username':username},new_vals)
        user = usersCollection.find_one({'username':username})
        
        return Response(json.dumps({'user': user}, default=json_util.default),
                            mimetype='application/json')
    except Exception as e:
        print(e)
        return {"message": "Server error"}, 500
                        
def returnImg(username):
    try:
        img = usersCollection.find_one({'username':username})
        if img is None:
            img = 'https://celebs.infoseemedia.com/wp-content/uploads/2019/08/Chris-Brown-and-Lisa-Ann-dated.jpg'
        return img
    except Exception as e:
        print(e)
        return {"message": "Server error"}, 500

def updateWins(username):
    try:
        user = usersCollection.find_one({"username": username})
        wins = user['wins']
        if wins is None:
            wins = 1
        else:
            wins = wins + 1
        usersCollection.update_one({'username': username},{'$set':{'wins': wins}})
        user = usersCollection.find_one({"username": username})
        return Response(json.dumps({'user': user}, default=json_util.default),
                            mimetype='application/json')
    except Exception as e:
        print(e)
        return {"message": "Server error"}, 500


def updateGames(username):
    try:
        user = usersCollection.find_one({"username": username})
        games = user['games']
        if games is None:
            games = 1
        else:
            games = games + 1
        usersCollection.update_one({'username': username},{'$set':{'games': games}})
        user = usersCollection.find_one({"username": username})
        return Response(json.dumps({'user': user}, default=json_util.default),
                            mimetype='application/json')
    except Exception as e:
        print(e)
        return {"message": "Server error"}, 500
