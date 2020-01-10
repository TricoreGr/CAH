from flask import Blueprint
from .services import getUsers, getUser, checkCreds, addUser
from flask import jsonify,request

users = Blueprint('users', __name__)

@users.route('/users/<username>', method=['GET'])
def returnUser(username):
    user = getUser(username)
    return user

@users.route('/users', method=['GET'])
def returnUsers():
    users = getUsers()
    return users

@users.route('/users/<username>/auth', methods=['POST']) #TODO add password 
def checkToken(username):
    creds = request.get_json()
    password = creds['password']
    response = checkCreds(username,password)
    return response