from pymongo import MongoClient

client = MongoClient('localhost',27017) #

mdb = client['tables']

collection = mdb['game1']

