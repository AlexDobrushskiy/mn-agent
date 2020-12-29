from django.contrib import admin
from main.models import Masternode, MNConnection, Regticket, Chunk

# Register your models here.
admin.site.register(Masternode)
admin.site.register(MNConnection)
admin.site.register(Regticket)
admin.site.register(Chunk)
