from flask import render_template, request, redirect, url_for, session
from flask_socketio import emit, send
from . import app, db, socketio
from .models import User, Game
from random import choice
import uuid

options = ['rock', 'paper', 'scissors']

def determine_winner(player1, player2):
    if player1 == player2:
        return None
    elif (player1 == 'rock' and player2 == 'scissors') or \
         (player1 == 'paper' and player2 == 'rock') or \
         (player1 == 'scissors' and player2 == 'paper'):
        return True
    else:
        return False


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return 'Usuario ya existe! Por favor, inicie sesión.'
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        session['user_id'] = new_user.id  # Guardar el ID del usuario en la sesión
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if not user:
            return 'Usuario no existe. Por favor, registrese.'
        session['username'] = username
        session['user_id'] = user.id  # Guardar el ID del usuario en la sesión
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/create_room')
def create_room():
    if 'username' not in session:
        return redirect(url_for('login'))
    room_id = str(uuid.uuid4())
    session['room_id'] = room_id
    return render_template('room.html', room_id=room_id)

@app.route('/join_room', methods=['GET', 'POST'])
def join_room():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        room_id = request.form['room_id']
        session['room_id'] = room_id
        return redirect(url_for('play', room_id=room_id))
    return render_template('join_room.html')

@app.route('/play/<room_id>')
def play(room_id):
    return render_template('play.html', room_id=room_id)


from flask_socketio import join_room, leave_room

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('message', {'msg': session['username'] + ' has joined the room.'}, room=room)

@socketio.on('create_room')
def handle_create_room():
    user_id = session.get('user_id')
    if not user_id:
        emit('error', {'error': 'User not logged in'})
        return

    room_id = str(uuid.uuid4())
    session['room_id'] = room_id
    join_room(room_id)
    emit('room_created', {'room_id': room_id, 'player': 'player1'})

@socketio.on('join_room')
def handle_join_room(data):
    room_id = data['room_id']
    user_id = session.get('user_id')

    if not user_id:
        emit('error', {'error': 'User not logged in'})
        return

    session['room_id'] = room_id
    join_room(room_id)
    emit('room_joined', {'room_id': room_id, 'player': 'player2'}, room=room_id)

@socketio.on('play')
def handle_play(data):
    room = data['room']
    player_choice = data['choice']
    user_id = session.get('user_id')

    if not user_id:
        emit('error', {'error': 'User not logged in'}, room=room)
        return

    game = Game.query.filter_by(room_id=room).first()

    if game:
        if game.player1_id == user_id:
            game.player1_choice = player_choice
        elif game.player2_id == user_id:
            game.player2_choice = player_choice

        if game.player1_choice and game.player2_choice:
            game.winner_id = determine_winner(game.player1_choice, game.player2_choice)
            db.session.commit()
            emit('game_result', {
                'player1_choice': game.player1_choice,
                'player2_choice': game.player2_choice,
                'result': get_result(game)
            }, room=room)
        else:
            db.session.commit()
            emit('waiting', {'message': 'Waiting for the other player to make a choice.'}, room=room)
    else:
        # Primer jugador creando el juego
        new_game = Game(player1_id=user_id, player1_choice=player_choice, room_id=room)
        db.session.add(new_game)
        db.session.commit()
        emit('waiting', {'message': 'Waiting for second player.'}, room=room)



def get_result(game):
    if game.winner_id is None:
        return 'tie'
    elif game.winner_id == game.player1_id:
        return 'win'
    else:
        return 'lose'





