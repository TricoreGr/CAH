from flask_socketio import SocketIO,emit,send,join_room,leave_room
from ..socket import socketio

@socketio.on('sendMessage')
def sendMessage(data):
    username = data['username']
    message = data['message']
    room = data['room']
    emit('newMessage',{'user':username,'message':message},room=room)