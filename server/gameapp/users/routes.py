from flask import Blueprint
from .services import getUsers, getUser, checkCreds, addUser
from flask import jsonify

users = Blueprint('users', __name__)

@users.route('/<username>')
def returnUser(username):
    user = getUser(username)
    return user

@users.route('/allusers')
def returnUsers():
    users = getUsers()
    return users

@users.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@users.route('/<username>/auth')
def checkToken(username):
    response = checkCreds('apostoles','password')
    return response