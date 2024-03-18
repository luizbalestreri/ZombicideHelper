from . import socketio, db
from flask_socketio import send, emit
from .models import Player, Character
# Import necessary models

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

def notify_card_transfer(to_player_id, card_id):
    """
    Notify the recipient player of a new card transfer.
    This function is called from routes.py during the card transfer process.
    """
    # Emit a SocketIO event to the specific recipient player
    emit('card_received', {'card_id': card_id}, room=to_player_id)