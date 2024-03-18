from . import db

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    life_points = db.Column(db.Integer, default=3)
    abilities = db.relationship('Ability', backref='character', lazy=True)
    photo_id = db.Column(db.String(100))
    experience_points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=0)
    player_id = db.Column(db.String(100))
    card_slot_1 = db.Column(db.Integer)
    card_slot_2 = db.Column(db.Integer)
    card_slot_3 = db.Column(db.Integer)
    card_slot_4 = db.Column(db.Integer)
    card_slot_5 = db.Column(db.Integer)

class Ability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    level = db.Column(db.Integer)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    token = db.Column(db.String(100))

from . import db


class EquipmentCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    image_url = db.Column(db.String(200))

class ZombieCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    image_url = db.Column(db.String(200))

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))  # "equipment" or "zombie"
    cards = db.Column(db.PickleType)  # Stores list of card IDs
    discard = db.Column(db.PickleType)  # Stores list of discarded card IDs