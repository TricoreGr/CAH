from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://ieeediots:asidirop@ieeediots-uctmo.mongodb.net/test?retryWrites=true&w=majority")

db = client['ieeediots_cah']  # db name is game
usersCollection = db['users']  # collection name

def userModel(username,password,email):
    return {
       'username' : username,
       'password' : password,
       'email' : email,
       'img' : 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTv4sdBGW3mOGK5e9h4KrbgA2UqdgPY6hstXXYnqhabBmtNSDwL&s',
       'games' : 0,
       'wins' : 0 
    }