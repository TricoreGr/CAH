from flask import Blueprint
from .services import getUsers, getUser, checkCreds, addUser

users = Blueprint('users', __name__)

@users.route('/<username>')
def returnUser(username):
    user = getUser(username)
    return user

@users.route('/allusers')
def returnUsers():
    users = getUsers()
    return users

@users.route('/<username>/auth')
def checkToken(username):
    response = checkCreds(username,'root')
    return response