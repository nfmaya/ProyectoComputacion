from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    player1_choice = db.Column(db.String(10))
    player2_choice = db.Column(db.String(10))
    winner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.String(50), nullable=False)
