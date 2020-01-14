import json
from bson import json_util
from ..config import Config
from bson.objectid import ObjectId
import random
from .models import roomModel 
import jwt
from .models import cardsCollection,roomsCollection
from flask import Response
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
        allBlackCards=document["blackCards"]
    return random.sample(allBlackCards, k=33)

def getRandomWhiteCards():
    allWhiteCards = []
    cursor = cardsCollection.find({})
    for document in cursor:
        allWhiteCards=document["whiteCards"]
    print(len(allWhiteCards))
    return random.sample(allWhiteCards, k=146)


def deleteRoom(id):
    try:
        query = {
            '_id':ObjectId(id)
        }
        deletedRoom = roomsCollection.delete_one(query)
        return id
    except:
        return {"message":"Server error"},500


def getRoundWhiteCards(roomId):
    roomDocument = roomsCollection.find_one({'_id': ObjectId(roomId)})
    session = roomDocument['gamesession']['round']['whitecards']
    print(session)
    return {"message": "ok"}


def getCzar():
    print(ok)


def getBlackCard():
    blackCards = cards.find({}).distinct('blackCards')
    return jsonify(blackCards)


def getPlayers():
    return ok


def getIndividualWhiteCards():
    return big 


    


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


def submitWhiteCard(user, id, card):
    try:
        query = {'id': id, 'players': [{'username': user['username']}]}
        new_vals = {'$push': {'gamesession': {
            'whitecards': [card]
        }}}
        tables.update_one(query, new_vals)
        message = 'Card was submited'
    except:
        message = 'Card was not submited'
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
    username = jwt.decode(token,Config.SECRET_KEY)['user']
    return username
