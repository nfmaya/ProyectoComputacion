from flask import render_template, request, redirect, url_for, session
from app import app, db, socketio
from app.models import Room, Game
from flask_socketio import emit
import uuid

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_room', methods=['GET', 'POST'])
def create_room():
    if request.method == 'POST':
        room_id = str(uuid.uuid4())
        room = Room(id=room_id)
        db.session.add(room)
        db.session.commit()
        session['user_id'] = str(uuid.uuid4())
        session['room_id'] = room_id
        return redirect(url_for('play', room_id=room_id))
    return render_template('create_room.html')

@app.route('/join_room', methods=['GET', 'POST'])
def join_room():
    if request.method == 'POST':
        room_id = request.form['room_id']
        room = Room.query.get(room_id)
        if room:
            session['user_id'] = str(uuid.uuid4())
            session['room_id'] = room_id
            return redirect(url_for('play', room_id=room_id))
        else:
            return 'Room not found', 404
    return render_template('join_room.html')

@app.route('/play', methods=['GET'])
def play():
    room_id = request.args.get('room_id')
    return render_template('play.html', room_id=room_id)


from .game_functions import determine_winner, insert_game

@socketio.on('play')
def handle_play(data):
    room_id = session.get('room_id')
    user_id = session.get('user_id')
    
    game = Game.query.filter_by(room_id=room_id).first()
    if not game:
        game = Game(id=str(uuid.uuid4()), room_id=room_id)
        db.session.add(game)
    
    if game.player1_id is None:
        game.player1_id = user_id
        game.player1_choice = data['choice']
    elif game.player2_id is None:
        game.player2_id = user_id
        game.player2_choice = data['choice']

    if game.player1_choice and game.player2_choice:
        winner = determine_winner(game.player1_choice, game.player2_choice)

        if winner is None:  # Tie
            winner_id = None
        elif winner:  # Player 1 wins
            winner_id = game.player1_id
        else:  # Player 2 wins
            winner_id = game.player2_id

        game.winner_id = winner_id
    
    db.session.commit()
    
    emit('play_response', {
        'player1_id': game.player1_id,
        'player2_id': game.player2_id,
        'player1_choice': game.player1_choice,
        'player2_choice': game.player2_choice,
        'room_id': game.room_id
    }, room=room_id)
