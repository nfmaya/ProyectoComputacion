
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_session import Session

app = Flask(__name__, template_folder='../templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:manuel@localhost/pptbd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

db = SQLAlchemy(app)
Session(app)
socketio = SocketIO(app)  # Initialize SocketIO here

from app import routes

with app.app_context():
   db.create_all()