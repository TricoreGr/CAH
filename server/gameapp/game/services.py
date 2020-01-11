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
    tablename = owner + "'s_table"
    table = {
        'id' : tablename,
        'owner' : owner,
        'gamesession' : {
            'czar' : None,
            'blackCards' : [],
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

def addUserToTable(user,id):
    query = {'id':id}
    newuser = {'$push': {
        'players':[
            {'username':user['username'],'points':0,'whitecards:[]'}
            ]}}
    tables.update_one(query,newuser)

def removeUserFromTable(user,id):
    query = {'id':id}
    user = {'$pull': {
        'players':[
            {'username':user['username']}
            ]}}
    tables.update_one(query,user)
