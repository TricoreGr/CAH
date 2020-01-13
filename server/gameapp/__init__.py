from flask import Flask
from flask_socketio import SocketIO,emit,send
from gameapp.config import Config,Configdb

socketio = SocketIO()

@socketio.on('joined',{})
def joined(data):
    emit('playerJoined',{'user':'status',"message":data['username']+' has joined.'},broadcast=True)

# todo: set it up
@socketio.on('leave')
def leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the table.', room=room)

@socketio.on('sendMessage')
def sendMessage(data):
    username = data['username']
    message = data['message']
    emit('newMessage',{'user':username,'message':message},broadcast=True)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.from_object(Configdb)

    from gameapp.users.routes import users
    from gameapp.game.routes import game
    from gameapp.chat.routes import chat

    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(game, url_prefix='/game')
    app.register_blueprint(chat)

    socketio.init_app(app,cors_allowed_origins="*")

    return app