from gameapp.users.services import check
from flask import Blueprint

users = Blueprint('users', __name__)

@users.route('/')
def health_check():
    return check()