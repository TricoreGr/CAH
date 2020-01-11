from pymongo import MongoClient

client = MongoClient("mongodb+srv://ieeediots:asidirop@ieeediots-uctmo.mongodb.net/test?retryWrites=true&w=majority") #TODO whitlist your ip in order to connect

game = client['game'] #db name is game

cards = game['cards'] #collection name

tables = game['tables'] #collection name