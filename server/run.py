from gameapp import create_app,socketio
from flask_cors import CORS

app = create_app()
socketio = socketio

from gameapp.chat import * 

CORS(app, resources={r'/*': {'origins': '*'}})

if __name__ == '__main__':
    app.run(debug=True,port=5000)
