from .models import cardsCollection, roomsCollection, roomModel
import json
import jwt
from flask import jsonify, Response
from bson.json_util import dumps
from bson import json_util, BSON
from ..config import Config
from bson.objectid import ObjectId
import random
from .events import join_room,leave_room


# def migrateCards():
#     with open('cards.json','r') as file:
#         crds = json.load(file)
#     cards.insert(crds)


def getRooms():
    try:
        rooms = []
        cursor = roomsCollection.find({})
        for document in cursor:
            rooms.append(document)
        return Response(json.dumps({'rooms': rooms}, default=json_util.default),
                        mimetype='application/json')
    except Exception as e:
        print(e)
        response = {
            'message': 'Could not return tables'
        }
        return response, 500


def createRoom(token):
    owner = getUsernameByJWToken(token)
    try:
        whiteCards = getRandomWhiteCards()
        blackCards = getRandomBlackCards()
        room = roomModel(owner, blackCards, whiteCards)
        print(room)
        roomsCollection.insert_one(room)
        createdRoom = roomsCollection.find_one({"owner": owner})
        return Response(json.dumps({'room': createdRoom}, default=json_util.default),
                        mimetype='application/json')
    except Exception as e:
        print(e)
        return {"message": "Server error"}, 500


def getRandomBlackCards():
    allBlackCards = []
    cursor = cardsCollection.find({})
    for document in cursor:
        allBlackCards = document["blackCards"]
    return random.sample(allBlackCards, k=33)


def getRandomWhiteCards():
    allWhiteCards = []
    cursor = cardsCollection.find({})
    for document in cursor:
        allWhiteCards = document["whiteCards"]
    print(len(allWhiteCards))
    return random.sample(allWhiteCards, k=146)


def deleteRoom():
    return okok


def getRoundWhiteCards(roomId):
    roomDocument = roomsCollection.find_one({'_id': ObjectId(roomId)})
    session = roomDocument['gamesession']['round']['whitecards']
    return {"message": "ok"}


def getCzar(roomId):
    roomDocument = roomsCollection.find_one({'_id': ObjectId(roomId)})
    czar = roomDocument['gamesession']['round']['czar']
    return Response(json.dumps({'czar': czar}, default=json_util.default),
                    mimetype='application/json')


def getBlackCard(roomId):
    roomDocument = roomsCollection.find_one({'_id': ObjectId(roomId)})
    blackCard = roomDocument['gamesession']['round']['blackCard']
    return Response(json.dumps({'blackCard': blackCard}, default=json_util.default),
                    mimetype='application/json')


def getPlayers(roomId):
    roomDocument = roomsCollection.find_one({'_id': ObjectId(roomId)})
    players = roomDocument['gamesession']['players']
    return Response(json.dumps({'players': players}, default=json_util.default),
                    mimetype='application/json')


def getIndividualWhiteCards(roomId, username):
    try:
        roomDocument = roomsCollection.find_one({'_id': ObjectId(roomId)})
        players = roomDocument['gamesession']['players']
        for player in players:
            if player['username'] == username:
                return Response(json.dumps({'whitecards': player['whitecards']}, default=json_util.default),
                        mimetype='application/json')
    except Exception as e:
        print(e)
        return {"message": "Server error"}, 500


def submitWhiteCards(roomId, token, cards):
    try:
        roomDocument = roomsCollection.find_one({'_id': ObjectId(roomId)})
        submittedUsername = getUsernameByJWToken(token)
        cardsToAppend = []
        for card in cards:
            if card is not None:
                cardsToAppend.append(card)
        submittedCards = {
            'username': submittedUsername,
            'cards': cardsToAppend
        }
        print(submittedCards)



        return {"message": "Server ok"}, 200 
    except Exception as e:
        print(e)
        return {"message": "Server error"}, 500


        return {"message": "Server ok"}, 200 
    except Exception as e:
        print(e)
        return {"message": "Server error"}, 500

def getAllTable():
    try:
        rooms = []
        cursor = tables.find({})
        for table in cursor:
            id = table['id']
            players = len(table['players'])
            rooms.append({"id": id, "players": players})
        response = {
            'message': 'All table',
            'tables': rooms
        }
    except:
        response = {
            'message': 'Could not return tables'
        }
    return jsonify(response)


def deleteTable(id):
    try:
        query = {'id': id}
        tables.delete_one(query)
        message = 'Table was deleted'
    except:
        message = 'Unable to delete table'
    response = {
        'message': message
    }
    return jsonify(response)


def addUserToTable(user, id):
    try:
        query = {'id': id}
        newuser = {'$push': {
            'players': [
                {'username': user['username'], 'points':0, 'whitecards':[]}
            ]}}
        tables.update_one(query, newuser)
        message = 'User added to table'
    except:
        message = 'Could not add user to table'
    response = {
        'message': message
    }
    return jsonify(response)


def removeUserFromTable(user, id):
    try:
        query = {'id': id}
        new_vals = {'$pull': {
            'players': [
                {'username': user['username']}
            ]}}
        tables.update_one(query, new_vals)
        message = 'User removed from table'
    except:
        message = 'User was not removed from table'
    response = {
        'message': message
    }
    return jsonify(response)
def getSubmitedCards(id):
    try:
        query = {'id': id}
        result = tables.find_one(query)
        session = result['gamesession']
        cards = session['whiteCards']
        response = {
            'message': 'Cards were returned',
            'cards': cards
        }
    except:
        response = {
            'message': 'Could not return cards'
        }
    return jsonify(response)


def getUsernameByJWToken(token):
    username = jwt.decode(token, Config.SECRET_KEY)['user']
    return username
