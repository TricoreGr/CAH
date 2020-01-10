from flask import Blueprint
from .services import getUsers, getUser, checkCreds, addUser, getUserByJWToken, deleteUser
from flask import jsonify,request

users = Blueprint('users', __name__)

@user.route('/users/delete',method['GET'])
def deleteUser():
    username - getUserByJWToken(request.get_json()['token'])
    response = deleteUser(username)
    return response

@user.route('/users/signup',method['POST'])
def signup():
    creds = request.get_json()
    username = creds['username']
    password = creds['password']
    email = creds['email']
    resp = addUser(username,password,email)
    return resp
    
@users.route('/users/<username>', method=['GET'])
def returnUser(username):
    user = getUser(username)
    return user

@users.route('/jwtToUsername',methods=['POST'])
def returnUserByJWT():
    user = getUserByJWToken(request.get_json()['token'])
    return user

@users.route('/users', method=['GET'])
def returnUsers():
    users = getUsers()
    return users

@users.route('/users/<username>/login', methods=['POST']) #TODO add password 
def login(username):
    creds = request.get_json()
    password = creds['password']
    response = checkCreds(username,password)
    return response