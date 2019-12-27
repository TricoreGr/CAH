from flask import Blueprint
from .services import getUsers, getUser, checkCreds, addUser
from flask import jsonify,request

users = Blueprint('users', __name__)

@users.route('/<username>')
def returnUser(username):
    user = getUser(username)
    return user

@users.route('/allusers')
def returnUsers():
    users = getUsers()
    return users

@users.route('/<username>/auth', methods=['GET','POST'])
def checkToken(username):
    password = 'password'
    if request.method == 'POST':
        creds = request.get_json()
        password = creds['password']
    response = checkCreds(username,password)
    return response