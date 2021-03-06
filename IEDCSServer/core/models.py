from django.db import models


keySize = 2048


### USER
class User(models.Model):
    userID = models.AutoField(primary_key=True)
    userCC = models.CharField(max_length=8, unique=True)
    userCCKey = models.CharField(max_length=keySize)
    userKey = models.CharField(max_length=keySize)
    username = models.CharField(max_length=100, unique=True)
    userIV = models.CharField(max_length=32, blank=True)
    userSalt = models.CharField(max_length=64, blank=True)
    email = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    magicKey = models.CharField(max_length=keySize, blank=True)
    createdOn = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'ID {0} - {1} - ({2}/{3}/{4})'.format( \
            self.userID, \
            self.username, \
            self.createdOn.day, \
            self.createdOn.month, \
            self.createdOn.year
        )


### PLAYER
class Player(models.Model):
    playerID = models.AutoField(primary_key=True)
    playerKey = models.CharField(max_length=keySize)
    playerIV = models.CharField(max_length=32)
    createdOn = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return u'{0} - ({1}/{2}/{3})'.format(self.playerID, \
            self.createdOn.day, \
            self.createdOn.month, \
            self.createdOn.year)


### DEVICE
class Device(models.Model):
    deviceID = models.AutoField(primary_key=True)
    deviceKey = models.CharField(max_length=keySize)
    createdOn = models.DateTimeField(auto_now_add=True)
    player = models.ForeignKey(Player)
    deviceHash = models.CharField(max_length=keySize)

    def __unicode__(self):
        return u'{0} - ({1}/{2}/{3})'.format(self.deviceID, \
            self.createdOn.day, \
            self.createdOn.month, \
            self.createdOn.year)


### CONTENT
class Content(models.Model):
    contentID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    fileName = models.CharField(max_length=150)
    filepath = models.CharField(max_length=400)
    pages = models.IntegerField(default=0)
    restriction = models.CharField(max_length=150, default="World")
    description = models.CharField(max_length=250, blank=True, default="Place description here")
    createdOn = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'{0} - {1}'.format(
                self.contentID, \
                self.name, \
            )


### PURCHASE
class Purchase(models.Model):
    purchaseID = models.AutoField(primary_key=True)
    createdOn = models.DateTimeField(auto_now_add=True)
    content = models.ForeignKey(Content)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return u'purchaseID {0} - {1} - {2}'.format(
                self.purchaseID, \
                self.user, \
                self.content
            )
