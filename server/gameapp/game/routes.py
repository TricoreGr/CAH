from flask import Blueprint
from .services import getBlackCards,getWhiteCards,getBase,getOrder

game = Blueprint('game', __name__)

@game.route('/cards/white', methods=['GET'])
def returnWhiteCards():
    cards = getWhiteCards()
    return cards

@game.route('/cards/black', methods=['GET'])
def returnBlackCards():
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