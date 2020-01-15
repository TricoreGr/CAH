from .models import cardsCollection, roomsCollection, roomModel
from flask_socketio import SocketIO,emit,send,join_room,leave_room
from ..socket import socketio
import json
import jwt
from flask import jsonify, Response
from bson.json_util import dumps
from bson import json_util, BSON
from ..config import Config
from bson.objectid import ObjectId
import random
from pprint import pprint

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
    return random.sample(allWhiteCards, k=146)

def getRoundWhiteCards(roomId):
    try:
        roomDocument = roomsCollection.find_one({'_id': ObjectId(roomId)})
        cards = roomDocument['gamesession']['round']['whitecards']
        white_cards = list()
        for card in cards:
            white_cards.append(card)
        random.shuffle(white_cards)
        print(white_cards)
        return Response(json.dumps({'whiteCards': white_cards}, default=json_util.default),
                        mimetype='application/json')
    except Exception as e:
        print(e)
        return {'message','Server error'},500

def getCzar(roomId):
    czar = getCzarAsJson(roomId)
    return Response(json.dumps({'czar': czar}, default=json_util.default),
                    mimetype='application/json')

def getCzarAsJson(roomId):
    roomDocument = roomsCollection.find_one({'_id': ObjectId(roomId)})
    czar = roomDocument['gamesession']['round']['czar']
    return czar

def getNextCzar(czar,roomId):
    roomDocument = roomsCollection.find_one({'_id':ObjectId(roomId)})
    players = roomDocument['gamesession']['players']
    dudes = list()
    for player in players:
        dudes.append(player['username'])
    index = dudes.index(czar)
    if index != len(players)-1:
        czar = players[index+1]
    else:
        czar = players[0]
    query = {
        '_id':ObjectId(roomId)
    }
    new_vals = {
        "$set" : {
            "gamesession.round.czar" :  czar['username']     
        }
    }
    roomsCollection.update_one(query,new_vals)
    return czar['username']

def getBlackCard(roomId):
    roomDocument = roomsCollection.find_one({'_id': ObjectId(roomId)})
    blackCard = roomDocument['gamesession']['round']['blackCard']
    return Response(json.dumps({'blackCard': blackCard}, default=json_util.default),
                    mimetype='application/json')


def getPlayers(roomId):
    roomDocument = roomsCollection.find_one({'_id': ObjectId(roomId)})
    playersDoc = roomDocument['gamesession']['players']
    return Response(json.dumps({'players': playersDoc}, default=json_util.default),
                    mimetype='application/json')
    

def getRandomPlayer(roomId):
    roomDocument = roomsCollection.find_one({'_id': ObjectId(roomId)})
    players = roomDocument['gamesession']['players']
    czar = random.choice(players)
    query = {
        '_id':ObjectId(roomId)
    }
    new_vals = {
        "$set" : {
            "gamesession.round.czar" : czar['username']
        }
    }
    roomsCollection.update_one(query,new_vals)
    return czar['username']

def getOwner(roomId):
    roomDocument = roomsCollection.find_one({'_id': ObjectId(roomId)})
    owner = roomDocument['owner']
    return Response(json.dumps({'owner': owner}, default=json_util.default),
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
        submittedUsername = getUsernameByJWToken(token)
        
        cardsToAppend = ""
        for card in cards:
            cardsToAppend +=  card + "   +   "
        cardsToAppend = cardsToAppend[:-7]

        submittedCards = {
            'username': submittedUsername,
            'cards': cardsToAppend
        }
        query = {
            '_id': ObjectId(roomId)
        }
        new_vals = {
            "$push" : {
                "gamesession.round.whitecards" : {
                    "username": submittedUsername,
                    "cards" : cardsToAppend
                }
            }

        }
        roomsCollection.update_one(query,new_vals)

        roomDoc = roomsCollection.find_one(query)
        players = roomDoc['gamesession']['players']

        for player in players:
            if submittedUsername == player['username']:
                Usercards = player['whitecards']
                break

        for card in Usercards:
            if card in cards:
                Usercards.remove(card)
        
        for player in players:
            if submittedUsername == player['username']:
                player['whitecards'] = Usercards
        
        
        roomsCollection.update_one(query,{'$set':{'gamesession.players':players}})
        resp = checkCzarTurn(roomId)

        socketio.emit('playerSubmission',{'username':submittedUsername},room=roomId)
        if resp is not False:
            socketio.emit('czarPickingPhase',{'status':'czar'}, room=roomId)
        return Response(json.dumps({'cards': submittedCards}, default=json_util.default),
                        mimetype='application/json')
    except Exception as e:
        print(e)
        return {"message": "Server error"}, 500

def setUserPoints(roomId, username):
    roomDocument = roomsCollection.find_one({'_id': ObjectId(roomId)})
    playersArray = roomDocument['gamesession']['players']
    print(playersArray)
    return {'message':'ok'}

def insertPlayer(roomId, username, img):
    try:
        query = {
                '_id': ObjectId(roomId)
            }
        userObject = {
            "username": username,
            "points" : 0,
            "img": img,
            "whitecards": []
        }
        new_vals = {
            "$push" : {
                "gamesession.players" : userObject
            }
        }
        roomsCollection.update_one(query,new_vals)
        return Response(json.dumps({'player': userObject}, default=json_util.default),
                        mimetype='application/json')
    except Exception as e:
        print(e)
        return {"message": "Server error"}, 500

def addUserToTable(user, id):
    try:
        query = {'_id': ObjectId(roomId)}
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

def removeUserFromTable(username, roomId):
    try:
        query = {'_id': ObjectId(roomId)}
        new_vals = {'$pull': {'gamesession.players': {'username': username}}}
        roomsCollection.update_one(query, new_vals)
    except:
        pass

def getSubmitedCards(id):
    try:
        query = {'_id': ObjectId(roomId)}
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

def splitCards(roomId):
    roomDocument = roomsCollection.find_one({'_id': ObjectId(roomId)})
    whiteCards = roomDocument['gamesession']['cards']['whiteCards']
    players = roomDocument['gamesession']['players']
    new_values = list()
    query = {
        '_id' : ObjectId(roomId),
    }

    for player in players:
        difference = 10 - len(player['whitecards'])
        player_cards = list()

        for i in range(difference):
            white_card = whiteCards.pop()
            player_cards.append(white_card)
            new_vals = {
                '$pull' : {
                    'gamesession.cards.whiteCards' : white_card
                }
            }
            roomsCollection.update_one(query,new_vals)

        new_values.append({
            'username': player['username'],
            "points" : player['points'],
            "whitecards" : player_cards
        })

    new_vals = {
        '$set' : {
            "gamesession.players": new_values
        }
    }
    roomsCollection.update_one(query,new_vals)

def checkToDeleteRoom(roomId):
    try:
        query = {
            '_id' : ObjectId(roomId)
        }
        roomDocument = roomsCollection.find_one(query)
        playas = roomDocument['gamesession']['players']
        if len(playas) == 0:
            roomsCollection.delete_one(query)
            message = {
                'message' : 'Room is deleted'
            }
    except:
        pass

def submitBlackCard(roomId):
    try:
        query = {
            '_id' : ObjectId(roomId)
        }
        roomDocument = roomsCollection.find_one(query)
        blackCards = roomDocument['gamesession']['cards']['blackCards']
        card = random.sample(blackCards, k=1)
        card = card[0]
        new_values = {
            '$pull' : {
                    'gamesession.cards.blackCards' : card
                }
        }
        update = {
            '$set' : {
                'gamesession.round.blackCard' : card
            }
        }
        roomsCollection.update_one(query,update)
        roomsCollection.update_one(query,new_values)
    except Exception as e:
        print(e)
        return jsonify({'message':'Server error'}),500

def getTableStatus(roomId):
    try:
        query = {
            '_id': ObjectId(roomId)
        }
        roomDocument = roomsCollection.find_one(query)
        return Response(json.dumps({'room': roomDocument}, default=json_util.default),
                        mimetype='application/json')
    except Exception as e:
        print(e)
        return jsonify({'message':'Server Error'}),500

def checkCzarTurn(roomId):
    try:
        print("CZAR TEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEST")
        query = {
            '_id': ObjectId(roomId)
        }
        player_counter = 0
        roomDocument = roomsCollection.find_one(query)
        players = roomDocument['gamesession']['players']
        cards = roomDocument['gamesession']['round']['whitecards']
        for player in players:
            print(len(player['whitecards']))
            if len(player['whitecards']) != 0:
                player_counter += 1
        print(player_counter)       
        if len(cards) == player_counter - 1:
            print("WORKS")
            return cards
        else:
            return False
    except:
        return False
