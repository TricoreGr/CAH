from gameapp import create_app,create_socket
from flask_cors import CORS

app = create_app()
socketio = create_socket(app)

CORS(app, resources={r'/*': {'origins': '*'}})

if __name__ == '__main__':
    app.run(debug=True,port=5000)
    socketio.run(app,port=5005)