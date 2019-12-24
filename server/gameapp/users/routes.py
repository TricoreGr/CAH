from flask import Blueprint
from .services import getUsers, getUser

users = Blueprint('users', __name__)

@users.route('/<username>')
def returnUser(username):
    user = getUser(username)
    return user

@users.route('/allusers')
def returnUsers():
    users = getUsers()
    return users