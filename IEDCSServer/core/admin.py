from django.contrib import admin
from .models import User, Player, Device, Content, Purchase

# Register your models here.
admin.site.register(User)
admin.site.register(Player)
admin.site.register(Device)
admin.site.register(Content)
admin.site.register(Purchase)
