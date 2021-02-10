from django.db import models
from datetime import datetime

REGTICKET_STATUS_CREATED = 0
REGTICKET_STATUS_ERROR = -1
REGTICKET_STATUS_PLACED_ON_BLOCKCHAIN = 1

REGTICKET_STATUS_CHOICES = ((REGTICKET_STATUS_CREATED, 'Created'),
                            (REGTICKET_STATUS_ERROR, 'Error'),
                            (REGTICKET_STATUS_PLACED_ON_BLOCKCHAIN, 'Placed on blockchain'),)


# Create your models here.
class Masternode(models.Model):
    ip = models.CharField(unique=True, max_length=15)
    address = models.CharField(max_length=35, null=True)
    balance = models.IntegerField(null=True)
    pastelID = models.CharField(max_length=86, unique=True)
    name = models.CharField(max_length=35)
    update = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return '{}'.format(self.ip)


class Regticket(models.Model):
    masternode_pastelid = models.ForeignKey(Masternode, on_delete=models.CASCADE, to_field='pastelID',)
    artist_pastelid = models.CharField(max_length=86,)
    image_hash = models.CharField(max_length=64)
    status = models.IntegerField(choices=REGTICKET_STATUS_CHOICES)
    created = models.DateTimeField()

    class Meta:
        unique_together = ('masternode_pastelid', 'image_hash',)

    def __str__(self):
        return '{}'.format(self.id)


class Chunk(models.Model):
    mn_pastelid = models.ForeignKey(Masternode, on_delete=models.CASCADE, to_field='pastelID',)
    chunk_id = models.CharField(max_length=256,)
    image_hash = models.CharField(max_length=64,)
    indexed = models.BooleanField()
    confirmed = models.BooleanField()
    stored = models.BooleanField()

    class Meta:
        unique_together = ('chunk_id', 'mn_pastelid',)

    def __str__(self):
        return '{}'.format(self.id)


class MNConnection(models.Model):
    masternode_pastelid = models.ForeignKey(Masternode, on_delete=models.CASCADE, to_field='pastelID',)
    ip = models.CharField(max_length=15)
    remote_pastelid = models.CharField(max_length=86,)
    active = models.BooleanField()

    class Meta:
        unique_together = ('masternode_pastelid', 'remote_pastelid',)

    def __str__(self):
        return '{}'.format(self.id)
