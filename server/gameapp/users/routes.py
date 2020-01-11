from flask import Blueprint
from .services import getUser, checkCreds, addUser, getUserByJWToken, deleteUser, updateUser
from flask import jsonify,request

users = Blueprint('users', __name__)

@users.route('/delete',methods=['DELETE'])
def removeUser():
    try:
        token = request.get_json()['token']
        user = getUserByJWToken(token)
        username = user['username']
        response = deleteUser(username)
        return response
    except:
        response = {
            'message' : 'Error at delete'
        }
        return jsonify(response)

@users.route('/signup',methods=['POST'])
def signup():
    try:
        creds = request.get_json()
        username = creds['username']
        password = creds['password']
        email = creds['email']
        response = addUser(username,password,email)
        return response
    except Exception as e:
        print(e)
        response = {
            'message' : 'Error at singup'
        }
        return jsonify(response)

@users.route('/<username>', methods=['GET'])
def returnUser(username):
    try:
        user = getUser(username)
        response = jsonify(user)
        return response
    except:
        response = {
            'message' : 'Error at user'
        }
        return jsonify(response)

@users.route('/jwtToUsername',methods=['POST'])
def returnUserByJWT():
        user = getUserByJWToken(request.get_json()['token'])
        return user

@users.route('/login', methods=['POST']) #TODO add password 
def login():
    try:
        creds = request.get_json()
        username = creds['username']
        password = creds['password']
        response = checkCreds(username,password)
        return response
    except:
        response = {
            'message' : 'Error at login'
        }
        return jsonify(response)

@users.route('/update',methods=['UPDATE'])
def update():
    try:
        creds = request.get_json()
        token = creds['token']
        username = getUserByJWToken(token)
        username = username['username'] 
        new_username = creds['username']
        img = creds['image']
        response = updateUser(username,new_username,img)
        return response
    except:
        response = {
            'message':'Error at update'
        }
        return jsonify(response)