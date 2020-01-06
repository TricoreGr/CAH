from flask import Blueprint
from .services import getBlackCards,getWhiteCards,getBase,getOrder

game = Blueprint('game', __name__)

@game.route('/white')
def returnWhiteCards():
    cards = getWhiteCards()
    return cards

@game.route('/black')
def returnBlackCards():
    cards = getBlackCards()
    return cards

@game.route('/base')
def returnBase():
    base = getBase()
    return base

@game.route('/order')
def returnOrder():
    order = getOrder()
    return order