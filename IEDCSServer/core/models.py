from django.db import models


keySize = 1024


### USER
class User(models.Model):
    userID = models.AutoField(primary_key=True)
    userKey = models.CharField(max_length=keySize)
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=100)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    fileKey = models.CharField(max_length=keySize, blank=True)
    # playerID = models.ForeignKey(Player)
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
    createdOn = models.DateTimeField(auto_now_add=True)
    userId = models.ForeignKey(User)

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
    players = models.ManyToManyField(Player) # ManyToMany relation

    def __unicode__(self):
        return u'{0} - ({1}/{2}/{3})'.format(self.deviceID, \
            self.createdOn.day, \
            self.createdOn.month, \
            self.createdOn.year)


### CONTENT
class Content(models.Model):
    contentId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    createdOn = models.DateTimeField(auto_now_add=True)
    restriction = models.CharField(max_length=150)
    description = models.CharField(max_length=250)

    def __unicode__(self):
        return u'{0} - {1}'.format(
                self.contentId, \
                self.name, \
            )


### PURCHASE
class Purchase(models.Model):
    purchaseID = models.AutoField(primary_key=True)
    createdOn = models.DateTimeField(auto_now_add=True)
    content = models.ForeignKey(Content)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return u'contentID {0} - {1}'.format(
                self.purchaseID, \
                self.user, \
            )
