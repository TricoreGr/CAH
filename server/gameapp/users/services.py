from .models import User,db,users_schema,user_schema
from flask import jsonify, Response
import json
import hashlib
import jwt
from ..config import Config


def getUsers():
    users = User.query.all()
    output = users_schema.dump(users)
    return {"users": output}


def addUser(username,password,email):
    userExists = User.query.filter_by(username=username).first()
    mailExists = User.query.filter_by(email=email).first()

    if userExists is not None:
        return {'message': 'User already exists'}, 409
    if mailExists is not None:
        return {'message': 'A user with this email already exists'}, 409
    hashedPassword = hashPassword(str(password))
    user = User(username=username, password=hashedPassword, email=email)
    db.session.add(user)
    db.session.commit()

    newUser = user.query.filter_by(username = username).first()
    output = user_schema.dump(newUser)
    key = Config.SECRET_KEY #get the secrete key
    token = jwt.encode({'user':username},key) #generate token

    return {"user": output, "token": token.decode('utf-8')}    


def hashPassword(password):
    h = hashlib.md5(password.encode('utf-8'))
    return h.hexdigest()


def getUser(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        return {'message': 'User was not found'}, 404
    output = user_schema.dump(user)
    return output


def getUserByJWToken(token):
    username = jwt.decode(token,Config.SECRET_KEY)['user']
    return getUser(username)


def checkCreds(username,password):
    hashedPassword = hashPassword(password)
    user = User.query.filter_by(username=username)
    if user is None:
        return {'message': 'There is no user with this username'}, 404
    userWithPassword = user.filter_by(password=hashedPassword).first()
    if userWithPassword is None:
        return {'message': 'Invalid credentials'}, 401
    key = Config.SECRET_KEY #get the secrete key
    token = jwt.encode({'user':username},key) #generate token
    output = user_schema.dump(userWithPassword)
    return {"user": output, "token": token.decode('utf-8')}


def deleteUser(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return {'message': 'User was not found'}, 404
    output = user_schema.dump(user)
    db.session.delete(user)
    db.session.commit()
    return output
    

def updateUser(username, img):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return {'message':'There is no user with this username'}, 404 
    return updateUserImg(user, img)


def updateUserImg(user, img):
    if (user.img == img):
        return {'message':'The new image is the same as the old one'}, 400
    user.img = img
    db.session.commit()
    print(user.username)
    newUser = user.query.filter_by(username = user.username).first()
    output = user_schema.dump(user)
    return output

def returnImg(username):
    user = User.query.filter_by(username=username).first()
    img = user.img
    if img is None:
        img = 'https://celebs.infoseemedia.com/wp-content/uploads/2019/08/Chris-Brown-and-Lisa-Ann-dated.jpg'
    return img