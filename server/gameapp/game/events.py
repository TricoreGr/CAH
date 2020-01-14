from flask_socketio import SocketIO,emit,send,join_room,leave_room
from ..socket import socketio
from ..users.services import returnImg
from .services import getCzarAsJson, getRandomPlayer, getNextCzar

@socketio.on('joined')
def joined(data):
    room = data['room']
    join_room(room)
    username = data['username']
    img = returnImg(username)
    emit('playerJoined',{'user':'status','message':username +' has joined.', 'image':img,'player':username},room=room)

@socketio.on('leave')
def left(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('playerLeft',{'user':'status','message':data['username']+' has left.'}, room=room)

@socketio.on('round_start')
def start(data):
    room = data['room']
    czar = getCzarAsJson(room)
    if czar is "" or czar is None:
        czar = getRandomPlayer(room)
    else:
        czar = getNextCzar(czar,room)
    return czar