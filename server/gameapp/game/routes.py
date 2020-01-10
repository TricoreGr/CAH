from flask import Blueprint
from .services import getBlackCards,getWhiteCards,getBase,getOrder

game = Blueprint('game', __name__)

@game.route('/cards/white', method=['GET'])
def returnWhiteCards():
    cards = getWhiteCards()
    return cards

@game.route('/cards/black', method=['GET'])
def returnBlackCards():
    cards = getBlackCards()
    return cards

@game.route('/cards/base', method=['GET'])
def returnBase():
    base = getBase()
    return base

@game.route('/cards/order', method=['GET'])
def returnOrder():
    order = getOrder()
    return order