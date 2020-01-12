from flask_socketio import emit,join_room,leave_room
from .. import socketio

@socketio.on('joined')
def joined(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + 'has entered the table.', room=room)

@socketio.on('leave')
def leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the table.', room=room)

@socketio.on('send')
def send(data):
    username = data['username']
    message = data['message']
    room = data['room']
    send(username + ': ' + message, room=room)