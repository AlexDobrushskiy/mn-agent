from django.db import models


# Create your models here.
class Masternode(models.Model):
    ip = models.CharField(unique=True, max_length=15)
    address = models.CharField(max_length=35, null=True)
    balance = models.IntegerField(null=True)

    def __str__(self):
        return '{}'.format(self.ip)
