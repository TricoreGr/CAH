from flask import Blueprint,jsonify
from services import getUsers

users = Blueprint('users', __name__)

@users.route('/')
def hello():
    users = getUsers()
    return jsonify(users)