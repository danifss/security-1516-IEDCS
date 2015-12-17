
class UserInfo(object):
    userID = ''
    username = ''
    password = ''
    email = ''
    firstName = ''
    lastName = ''
    createdOn = ''

    def __init__(self, user=None, hashPass=None):  # userID=None, username=None, email=None, firstName=None, ):
        self.userID = user.userID
        self.username = user.username
        self.password = hashPass
        self.email = user.email
        self.firstName = user.firstName
        self.lastName = user.lastName
        self.createdOn = user.createdOn
