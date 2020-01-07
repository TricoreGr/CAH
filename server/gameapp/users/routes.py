from flask import Blueprint
from .services import getUsers, getUser, checkCreds, addUser,getUserByJWToken
from flask import jsonify,request

users = Blueprint('users', __name__)

@users.route('/<username>')
def returnUser(username):
    user = getUser(username)
    return user

@users.route('/jwtToUsername',methods=['POST'])
def returnUserByJWT():
    user = getUserByJWToken(request.get_json()['token'])
    return user

@users.route('/allusers')
def returnUsers():
    users = getUsers()
    return users

@users.route('/<username>/auth', methods=['GET','POST']) #TODO add password 
def checkToken(username):
    password = 'admin'
    if request.method == 'POST':
        creds = request.get_json()
        password = creds['password']
    response = checkCreds(username,password)
    return response