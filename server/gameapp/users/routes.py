from flask import Blueprint
from .services import getUsers, getUser, checkCreds, addUser, getUserByJWToken, deleteUser, updateUser, updateGames
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
            creds = request.get_json()
            username = creds.get('username')
            password = creds.get('password')
            email = creds.get('email')
            if username is None or password is None or email is None:
                response = {
                    'message':'Some fields are missing'
                }
                return response, 400
            response = addUser(username,password,email)
            return response
        except Exception as e:
            print(e)
            response = {
                'message' : 'Server error'
            }
            return response,500


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
            win = creds.get('win')
            game = creds.get('game')

            validUser = validateToken(creds.get('token'), username)
            if not validUser:
                return {'message': 'Unauthorized'}, 401
            
            if win is not None or game is not None:
                return updateGames(username,win,game)
            else:
                img = creds.get('image')
                if img is None:
                    return {'message': 'No user info given'}, 400 
                return updateUser(username, img)
        except Exception as e:
            print(e)
            return {'message': 'Server error'}, 500
    if request.method == 'DELETE':
        try:
            creds = request.get_json()
            validUser = validateToken(creds.get('token'), username)
            if not validUser:
                return {'message': 'Unauthorized'}, 401
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
        username = creds.get('username')
        password = creds.get('password')
        response = checkCreds(username, password)
        return response
    except Exception as e:
        print(e)
        response = {
            'message': 'Server error'
        }
        return response,500

def validateToken(token, givenUsername):
    if token is None:
        return False
    user = getUserByJWToken(token)
    if givenUsername != user.get('username'):
        return False
    return True
    