from flask_socketio import SocketIO,emit,send,join_room,leave_room
from ..socket import socketio

@socketio.on('joined')
def joined(data):
    room = data['room']
    join_room(room)
    emit('playerJoined',{'user':'status',"message":data['username']+' has joined.'},room=room)

@socketio.on('leave')
def left(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('playerLeft',{'user':'status',"message":data['username']+' has left.'}, room=room)