from flask import Blueprint
from .services import getUser, checkCreds, addUser, getUserByJWToken, deleteUser, updateUser
from flask import jsonify,request

users = Blueprint('users', __name__)


@users.route('/signup',methods=['POST'])
def signup():
    try:
        creds = request.get_json()
        username = creds['username']
        password = creds['password']
        email = creds['email']
        if username is None or password is None or email is None:
            response = {
                'message':'Some fields are missing'
            }
            return response, 400
        response = addUser(username,password,email)
        return response,200
    except Exception as e:
        print(e)
        response = {
            'message' : 'Server error'
        }
        return jsonify(response),500

@users.route('/<username>', methods=['GET','UPDATE','DELETE'])
def returnUser(username):
    if request.method == 'GET':
        try:
            user = getUser(username)
            response = jsonify(user)
            return response,200
        except:
            response = {
                'message' : 'Server error'
            }
            return jsonify(response),500
    elif request.method == 'DELETE':
        try:
            token = request.get_json()['token']
            uname = getUserByJWToken(token)
            if uname == username:
                response = deleteUser(username)
                return response,200
            else:
                response = {
                    'message' : 'Permission not allowed'
                }
                return jsonify(response),403
        except:
            response = {
                'message' : 'Server error'
            }
            return jsonify(response),500
    elif request.method == 'UPDATE':
        try:
            creds = request.get_json()
            token = creds['token']
            uname = getUserByJWToken(token)
            new_username = creds['username']
            if uname == username:
                img = creds['image']
                response = updateUser(username,new_username,img)
                return response,200
            else:
                response = {
                    'message' : 'Permission not allowed'
                }
                return jsonify(response),403
        except:
            response = {
                'message':'Server error'
            }
            return jsonify(response),500

@users.route('/jwtToUsername',methods=['POST'])
def returnUserByJWT():
        user = getUserByJWToken(request.get_json()['token'])
        return user

@users.route('/login', methods=['POST'])
def login():
    try:
        creds = request.get_json()
        username = creds['username']
        password = creds['password']
        response = checkCreds(username,password)
        return response,200
    except:
        response = {
            'message' : 'Server error'
        }
        return jsonify(response)