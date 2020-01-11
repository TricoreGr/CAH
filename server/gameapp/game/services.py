from .models import cards, tables
import json
from flask import jsonify

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

def newTable(owner):
    try:
        tablename = owner + "'s_table"
        table = {
            'id' : tablename,
            'owner' : owner,
            'gamesession' : {
                'czar' : None,
                'blackCard' : None,
                'whitecards' : []
            },
            'players': [{
                'username' : owner,
                'points' : 0,
                'whitecards' : []
                }
            ],
            'cards': {
                'bcards' : [],
                'wcards' : []
            }
        }
        tables.insert_one(table)

        message = 'New table was created'
    else:
        message = 'Could not create table'
    
    response = {
        'message' : message
    }
    return jsonify(response)

def getAllTable():
    try:
        info = []
        cursor = tables.find({})
        for table in cursor:
            id = table['id']
            players = len(table['players'])
            info.append({"id":id,"players":players})
        response = {
            'message' : 'All table',
            'tables' : info
        }
    except:
        response = {
            'message' : 'Could not return tables'
        }
    return jsonify(response)


def deleteTable(id):
    try:
        query = {'id':id}
        tables.delete_one(query)
        message = 'Table was deleted'
    else:
        message = 'Unable to delete table'
    response = {
        'message' : message
    }
    return jsonify(response)

def addUserToTable(user,id):
    try:
        query = {'id':id}
        newuser = {'$push': {
            'players':[
                {'username':user['username'],'points':0,'whitecards:[]'}
                ]}}
        tables.update_one(query,newuser)
        message = 'User added to table'
    except:
        message = 'Could not add user to table'
    response = {
        'message' : message
    }
    return jsonify(response)

def removeUserFromTable(user,id):
    try:
        query = {'id':id}
        new_vals = {'$pull': {
            'players':[
                {'username':user['username']}
                ]}}
        tables.update_one(query,new_vals)
        message = 'User removed from table'
    except:
        message = 'User was not removed from table'
    response = {
        'message' : message
    }
    return jsonify(response)

def submitWhiteCard(user,id,card):
    try:
        query = {'id':id, 'players':[{'username':user['username']}]}
        new_vals = {'$push': { 'gamesession':{
            'whitecards':[card]
        }}}
        tables.update_one(query,new_vals)
        message = 'Card was submited'
    except:
        message = 'Card was not submited'
    response = {
        'message' : message
    }
    return jsonify(response)

def getSubmitedCards(id):
    try:
        query = {'id':id}
        result = tables.find_one(query)
        session = result['gamesession']
        cards = session['whiteCards']
        response = {
            'message' : 'Cards were returned',
            'cards' : cards
        }
    except:
        response = {
            'message' : 'Could not return cards'
        }
    return jsonify(response)
