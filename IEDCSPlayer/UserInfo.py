
class UserInfo(object):
    def __init__(self, x, user=None):  # userID=None, username=None, email=None, firstName=None, ):
        self.x = x
        self.userID = user.userID
        self.username = user.username
        self.password = user.password
        self.email = user.email
        self.firstName = user.firstName
        self.lastName = user.lastName
        self.createdOn = user.createdOn
