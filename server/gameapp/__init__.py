from flask import Flask
from flask_socketio import SocketIO
from gameapp.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # socketio = SocketIO(app)
    # socketio.run(app)

    from gameapp.users.routes import users
    from gameapp.game.routes import game
    from gameapp.chat.routes import chat
    app.register_blueprint(users)
    app.register_blueprint(game)
    app.register_blueprint(chat)

    return app