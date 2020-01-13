from pymongo import MongoClient

# TODO whitlist your ip in order to connect
client = MongoClient(
    "mongodb+srv://ieeediots:asidirop@ieeediots-uctmo.mongodb.net/test?retryWrites=true&w=majority")

db = client['ieeediots_cah']  # db name is game
roomsCollection = db['rooms']  # collection name

db = client['game']
cardsCollection = db['cards']  # collection name



def roomModel(owner, blackcards, whitecards):
    return {
        'owner': owner,
        'gamesession': {
            'round': {
                'czar': None,
                'blackCard': None,
                'whitecards': []
            },
            'players': [
                {
                    'username': owner,
                    'points': 0,
                    'whitecards': []
                }
            ],
            'cards': {
                'blackCards': blackcards,
                'whiteCards': whitecards
            }
        },
    }
