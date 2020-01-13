from flask import Blueprint
from .events import sendMessage
# from flask_socketio import join_room,emit,send
# from server.gameapp import 

chat = Blueprint('chat', __name__)

# ROOMS = {}
 
