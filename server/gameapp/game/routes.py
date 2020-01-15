from flask import Blueprint, request
from .services import getOwner,getRooms, submitWhiteCards, insertPlayer, createRoom, getRoundWhiteCards, getCzar, getBlackCard, getPlayers,getIndividualWhiteCards, getTableStatus,checkWinner
from .events import joined,left,start

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
            whitecards = requestData.get('cards')
            return submitWhiteCards(roomId, token, whitecards)
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

@game.route('/<roomId>/players', methods=['GET','POST'])
def handlePlayersRoute(roomId):
    if request.method == 'GET':
        try:
            return getPlayers(roomId)
        except Exception as e:
            print(e)
            return {'message': 'Server error'}, 500
    if request.method == 'POST':
        try:
            requestData = request.get_json()
            token = requestData.get('token')
            return insertPlayer(roomId, token)
        except Exception as e:
            print(e)
            return {'message': 'Server error'}, 500

@game.route('/<roomId>/owner', methods=['GET'])
def handleOwnerRoute(roomId):
        try:
            return getOwner(roomId)
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

@game.route('/<roomId>', methods=['GET'])
def returnTableStatus(roomId):
    table = getTableStatus(roomId)
    del table['_id']
    return table