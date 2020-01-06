from .models import client
import json
from flask import jsonify

game = client['game']
cards = game['cards']

#blackCards
#whiteCards
#Base
#order

def migrateCards():
    with open('cards.json','r') as file:
        crds = json.load(file) 
    cards.insert(crds)

def getBlackCards():
    blackCards = cards.find({}).distinct('blackCards')
    return jsonify(blackCards)

def getWhiteCards():
    whiteCards = cards.find({}).distinct('whiteCards')
    return jsonify(whiteCards)

def getBase():
    base = cards.find({}).distinct('Base')
    return jsonify(base)

def getOrder():
    order = cards.find({}).distinct('order')