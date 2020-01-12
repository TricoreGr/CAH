from flask import Blueprint
from .services import getUsers, getUser, checkCreds, addUser, getUserByJWToken, deleteUser, updateUser
from flask import jsonify, request, Response

users = Blueprint('users', __name__)

@users.route('/', methods=['GET','POST'])
def handleUsersRoute():
    if request.method == 'GET':
        try:
            return getUsers()
        except Exception as e:
            print(e)
            return {'message': 'Server error'}, 500
    if request.method == 'POST':
        try: 
            requestPayload = request.get_json()
            username = requestPayload['username']
            password = requestPayload['password']
            email = requestPayload['email']
            if (username is None) or (password is None) or (email is None):
                return {'message': 'Some fields are missing'}, 400
            return addUser(username,password,email)
        except Exception as e:
            print(e)   
            return {'message': 'Server error'}, 500 


@users.route('/<username>', methods=['GET','PUT','DELETE'])
def handleUserRoute(username):
    if request.method == 'GET':
        try:
            return getUser(username)
        except:
            return {'message': 'Server error'}, 500
    if request.method == 'PUT':
        try:
            creds = request.get_json()
            print(creds)
            new_username = creds.get('username')
            img = creds.get('image')
            if (new_username is None) and (img is None):
                return {'message': 'No user info given'}, 400 
            return updateUser(username, new_username, img)
        except Exception as e:
            print(e)
            return {'message': 'Server error'}, 500
    if request.method == 'DELETE':
        try:
            return deleteUser(username)
        except Exception as e:
            print(e)
            return {'message': 'Server error'}, 500

@users.route('/jwtToUsername', methods=['POST'])
def returnUserByJWT():
    user = getUserByJWToken(request.get_json()['token'])
    return user

@users.route('/login', methods=['POST'])  # TODO add password
def login():
    try:
        creds = request.get_json()
        username = creds['username']
        password = creds['password']
        response = checkCreds(username, password)
        return response
    except:
        response = {
            'message': 'Error at login'
        }
        return jsonify(response)

