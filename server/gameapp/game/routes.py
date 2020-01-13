from flask import Blueprint, request
from .services import getRooms, createRoom, deleteRoom, getRoundWhiteCards, getCzar, getBlackCard, getPlayers,getIndividualWhiteCards

game = Blueprint('game', __name__)

@game.route('/', methods=['GET','POST','DELETE'])
def handleRoomsRoute():
    if request.method == 'GET':
        try:
            return getRooms()
        except Exception as e:
            print(e)
            return {'message': 'Server error'}, 500
    if request.method == 'POST':
        try:
            requestPayload = request.get_json()
            token = requestPayload.get('token')
            return createRoom(token)
        except Exception as e:
            print(e)
            return {'message': 'Server error'}, 500  
    if request.method == 'DELETE':
        try:
            requestPayload = request.get_json()
            token = requestPayload.get('token')
            return deleteRoom(token)
        except Exception as e:
            print(e)
            return {'message': 'Server error'}, 500 


@game.route('/<roomId>/round/whitecards', methods=['GET', 'POST'])
def handleRoundWhitecardsRoute(roomId):
    if request.method == 'GET':
        try:
            return getRoundWhiteCards(roomId)
        except Exception as e:
            print(e)
            return {'message': 'Server error'}, 500
    if request.method == 'POST':
        try:
            requestData = request.get_json()
            token = requestData.get('token')
            whitecard = requestData.get('card')
            submitWhitecards(roomId, token, card)
        except Exception as e:
            print(e)
            return {'message': 'Server error'}, 500   

@game.route('/<roomId>/round/czar', methods=['GET'])
def handleCzarRoute(roomId):
    try:
        return getCzar(roomId)
    except Exception as e:
        print(e)
        return {'message': 'Server error'}, 500


@game.route('/<roomId>/round/blackcard', methods=['GET'])
def handleBlackcardRoute(roomId):
    try:
        return getBlackCard(roomId)
    except Exception as e:
        print(e)
        return {'message': 'Server error'}, 500

@game.route('/<roomId>/players', methods=['GET'])
def handlePlayersRoute(roomId):
    try:
        return getPlayers(roomId)
    except Exception as e:
        print(e)
        return {'message': 'Server error'}, 500

@game.route('/<roomId>/players/<username>/whitecards', methods=['GET'])
def handlePlayerCardsRoute(roomId, username):
    try:
        return getIndividualWhiteCards(roomId, username)
    except Exception as e:
        print(e)
        return {'message': 'Server error'}, 500