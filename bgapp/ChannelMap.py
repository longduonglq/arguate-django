from bgapp.bgModels.User import User

def checkUserIdInMap(user_db):
    return user_db.channelID is not None

def getChannelID(user_db):
    return user_db.channelID
