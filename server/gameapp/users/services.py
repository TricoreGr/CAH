from models import User,db


def addUser(username,password,email,img):
    user = User(username=username, password=password, email=email, img=img)
    db.session.add(user)
    db.session.commit()
    print("User added")

def getUsers():
    users = User.query.all()
    return users

def getUser(uname):
    user = User.query.filter_by(username=uname).first()
    print(user)

if __name__ == '__main__':
    getUsers()
    getUser('admin')