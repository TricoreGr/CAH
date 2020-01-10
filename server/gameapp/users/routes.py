from flask import Blueprint
from .services import getUsers, getUser, checkCreds, addUser, getUserByJWToken, deleteUser
from flask import jsonify,request

users = Blueprint('users', __name__)

@users.route('/delete',methods=['DELETE'])
def removeUser():
    token = request.get_json()['token']
    user = getUserByJWToken(token)
    username = user['username']
    response = deleteUser(username)
    return response

@users.route('/signup',methods=['POST'])
def signup():
    creds = request.get_json()
    username = creds['username']
    password = creds['password']
    email = creds['email']
    resp = addUser(username,password,email)
    return resp

@users.route('/<username>', methods=['GET'])
def returnUser(username):
    user = getUser(username)
    resp = jsonify(user)
    return resp

@users.route('/jwtToUsername',methods=['POST'])
def returnUserByJWT():
    user = getUserByJWToken(request.get_json()['token'])
    return user

@users.route('/users', methods=['GET'])
def returnUsers():
    users = getUsers()
    return users

@users.route('/login', methods=['POST']) #TODO add password 
def login():
    creds = request.get_json()
    username = creds['username']
    password = creds['password']
    response = checkCreds(username,password)
    return response