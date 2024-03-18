import secrets
from flask import render_template, request, redirect, url_for, jsonify
from . import app, db
from .models import Character, Player, EquipmentCard, ZombieCard, Deck
from flask_socketio import emit
from . import socketio
from .events import notify_card_transfer

@app.route('/')
def index():
    characters = Character.query.all()
    return render_template('index.html', characters=characters)

def generate_player_id():
    """
    Generates a unique player ID.
    """
    return secrets.token_urlsafe(8)

def generate_token():
    """
    Generates a secure, random token for the player session.
    """
    return secrets.token_urlsafe(16)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        player_name = request.form.get('player_name')
        selected_character_ids = request.form.getlist('character_ids')
        
        player_id = generate_player_id()
        token = generate_token()
        
        new_player = Player(id=player_id, name=player_name, token=token)
        db.session.add(new_player)
        
        for character_id in selected_character_ids:
            character = Character.query.get(character_id)
            character.player_id = player_id
            db.session.add(character)
        
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html')

from flask import jsonify

@app.route('/character_details/<int:character_id>', methods=['GET'])
def get_character_details(character_id):
    character = Character.query.get(character_id)
    if character:
        # Assuming each character has a relationship to Abilities defined
        abilities = [ability.description for ability in character.abilities]
        player = Player.query.get(character.player_id)
        
        character_details = {
            "player_name": player.name if player else "Unknown",
            "current_health": character.life_points,
            "current_level": character.level,
            "abilities": abilities,
            "cards": {
                "slot_1": character.card_slot_1,
                "slot_2": character.card_slot_2,
                "slot_3": character.card_slot_3,
                "slot_4": character.card_slot_4,
                "slot_5": character.card_slot_5,
            }
        }

        return jsonify(character_details), 200
    else:
        return jsonify({"error": "Character not found"}), 404


import random

@app.route('/shuffle/<deck_type>', methods=['POST'])
def shuffle_deck(deck_type):
    deck = Deck.query.filter_by(type=deck_type).first()
    if deck:
        random.shuffle(deck.cards)
        db.session.commit()
        return {"success": True, "message": f"{deck_type.capitalize()} deck shuffled."}
    return {"success": False, "message": "Deck not found."}

@app.route('/draw/<deck_type>', methods=['POST'])
def draw_card(deck_type):
    deck = Deck.query.filter_by(type=deck_type).first()
    if deck and deck.cards:
        card_id = deck.cards.pop(random.randint(0, len(deck.cards) - 1))
        deck.discard.append(card_id)
        db.session.commit()
        return {"card_id": card_id}
    elif deck and not deck.cards:  # If deck is empty, refill from discard pile
        deck.cards = deck.discard
        deck.discard = []
        db.session.commit()
        return draw_card(deck_type)  # Try drawing again after refilling
    return {"success": False, "message": "Deck not found or empty."}

@app.route('/remaining/<deck_type>', methods=['GET'])
def remaining_cards(deck_type):
    deck = Deck.query.filter_by(type=deck_type).first()
    if deck:
        return {"remaining_cards": len(deck.cards)}
    return {"success": False, "message": "Deck not found."}

@app.route('/pop_card/<deck_type>/<int:card_id>', methods=['POST'])
def pop_specific_card(deck_type, card_id):
    deck = Deck.query.filter_by(type=deck_type).first()
    if deck and card_id in deck.cards:
        deck.cards.remove(card_id)
        deck.discard.append(card_id)
        db.session.commit()
        return {"success": True, "message": f"Card {card_id} popped from {deck_type} deck."}
    return {"success": False, "message": "Card or deck not found."}

@app.route('/transfer_card', methods=['POST'])
def transfer_card():
    from_player_id = request.json.get('from_player_id')
    to_player_id = request.json.get('to_player_id')
    card_id = request.json.get('card_id')
    from_player = Player.query.get(from_player_id)
    to_player = Player.query.get(to_player_id)
    
    # Remove the card from the sender
    removed = False
    for slot in ['card_slot_1', 'card_slot_2', 'card_slot_3', 'card_slot_4', 'card_slot_5']:
        if getattr(from_player, slot) == card_id:
            setattr(from_player, slot, None)
            db.session.commit()
            removed = True
            break
    if not removed:
        return jsonify({"success": False, "message": "Card not found in sender's slots."}), 400

    # Notify the recipient of the card transfer using real-time events
    notify_card_transfer(to_player_id, card_id)
    
    return jsonify({"success": True, "message": "Card transfer initiated."}), 200

    # Temporary store the card in a "pending_transfer" to the recipient

@app.route('/assign_card_to_slot', methods=['POST'])
def assign_card_to_slot():
    player_id = request.json.get('player_id')
    card_id = request.json.get('card_id')  # This can be from drawing or transfer
    slot = request.json.get('slot')  # Expected to be one of ['card_slot_1', 'card_slot_2', ..., 'card_slot_5']
    player = Player.query.get(player_id)
    
    # Assign the card to the selected slot
    setattr(player, slot, card_id)
    if card_id in player.pending_transfer:
        player.pending_transfer.remove(card_id)
    
    db.session.commit()
    return {"success": True, "message": "Card assigned to slot."}

@app.route('/modify_experience', methods=['POST'])
def modify_experience():
    player_id = request.json.get('player_id')
    experience_change = request.json.get('experience_change')  # This can be positive or negative
    character = Character.query.filter_by(player_id=player_id).first()
    
    character.experience_points += experience_change
    db.session.commit()
    return {"success": True, "experience_points": character.experience_points}

@app.route('/select_ability', methods=['POST'])
def select_ability():
    character_id = request.json.get('character_id')
    ability_id = request.json.get('ability_id')  # ID of the chosen ability
    character = Character.query.get(character_id)
    
    # Logic to ensure the character is at the appropriate level and the ability is among the options
    # This is simplified; you'll need to implement the actual logic based on your game rules
    
    character.selected_abilities.append(ability_id)
    db.session.commit()
    return {"success": True, "message": "Ability selected."}

@app.route('/modify_life', methods=['POST'])
def modify_life():
    character_id = request.json.get('character_id')
    life_change = request.json.get('life_change')  # Can be positive or negative
    character = Character.query.get(character_id)
    
    character.life_points += life_change
    db.session.commit()
    return {"success": True, "life_points": character.life_points}

@app.route('/choose_characters')
def choose_characters():
    return render_template('choose_characters.html')

