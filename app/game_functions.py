from .models import db, Game

def insert_game(player1_id, player2_id, player1_choice, player2_choice, winner_id):
    new_game = Game(
        player1_id=player1_id,
        player2_id=player2_id,
        player1_choice=player1_choice,
        player2_choice=player2_choice,
        winner_id=winner_id
    )
    db.session.add(new_game)
    db.session.commit()

def determine_winner(player1_choice, player2_choice):
    if player1_choice == player2_choice:
        return None  # Tie
    winning_combos = {
        'rock': 'scissors',
        'scissors': 'paper',
        'paper': 'rock'
    }
    if winning_combos[player1_choice] == player2_choice:
        return True
    return False
