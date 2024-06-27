from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Room(db.Model):
    id = db.Column(db.String, primary_key=True)

class Game(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    player1_id = db.Column(db.String(36), nullable=True)
    player2_id = db.Column(db.String(36), nullable=True)
    player1_choice = db.Column(db.String(10), nullable=True)
    player2_choice = db.Column(db.String(10), nullable=True)
    winner_id = db.Column(db.String(36), nullable=True)
    room_id = db.Column(db.String(36), db.ForeignKey('room.id'), nullable=False)


    room = db.relationship('Room', backref=db.backref('games', lazy=True))