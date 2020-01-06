import requests

def getCards():
    cards = requests.get("https://crhallberg.com/cah/output.php").json()
    print(cards)
getCards()