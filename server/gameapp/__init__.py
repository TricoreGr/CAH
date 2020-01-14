from flask import Flask
from  .socket import socketio
from gameapp.config import Config,Configdb

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.from_object(Configdb)

    from gameapp.users.routes import users
    from gameapp.game.routes import game
    from gameapp.chat.routes import chat

    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(game, url_prefix='/rooms')
    app.register_blueprint(chat)

    socketio.init_app(app,cors_allowed_origins="*")

    return app