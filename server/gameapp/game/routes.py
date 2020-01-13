from flask import Blueprint
from .services import getBlackCards,getWhiteCards,getBase,getOrder

game = Blueprint('game', __name__)

@game.route('/cards/<color>', methods=['GET'])
def returnWhiteCards(color):
    if color == 'white':
        cards = getWhiteCards()
        return cards
    elif color == 'black':
        cards = getBlackCards()
        return cards

@game.route('/cards/base', methods=['GET'])
def returnBase():
    base = getBase()
    return base

@game.route('/cards/order', methods=['GET'])
def returnOrder():
    order = getOrder()
    return order