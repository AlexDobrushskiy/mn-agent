from peewee import (Model, SqliteDatabase, BlobField, DateTimeField, DecimalField, BooleanField, IntegerField,
                    CharField)

MASTERNODE_DB = SqliteDatabase('/opt/app/agent/container_db/masternode.db')

REGTICKET_STATUS_CREATED = 0
REGTICKET_STATUS_ERROR = -1
REGTICKET_STATUS_PLACED_ON_BLOCKCHAIN = 1

REGTICKET_STATUS_CHOICES = ((REGTICKET_STATUS_CREATED, 'Created'),
                            (REGTICKET_STATUS_ERROR, 'Error'),
                            (REGTICKET_STATUS_PLACED_ON_BLOCKCHAIN, 'Placed on blockchain'),)

class Regticket(Model):
    upload_code = BlobField(unique=True, null=True)
    regticket = BlobField()
    artist_pk = BlobField()
    image_hash = BlobField()
    artists_signature_ticket = BlobField()
    created = DateTimeField()
    image_data = BlobField(null=True)
    localfee = DecimalField(null=True)
    is_valid_mn0 = BooleanField(null=True)
    mn1_pk = BlobField(null=True)
    mn1_serialized_signature = BlobField(null=True)
    is_valid_mn1 = BooleanField(null=True)
    mn2_pk = BlobField(null=True)
    mn2_serialized_signature = BlobField(null=True)
    is_valid_mn2 = BooleanField(null=True)
    status = IntegerField(choices=REGTICKET_STATUS_CHOICES, default=REGTICKET_STATUS_CREATED)
    error = CharField(null=True)
    confirmed = BooleanField(default=False)  # track if confirmation ticket for a given regticket exists

    class Meta:
        database = MASTERNODE_DB
        table_name = 'regticket'

class Chunk(Model):
    chunk_id = CharField(unique=True)
    image_hash = BlobField()
    indexed = BooleanField(default=False)  # to track fresh added chunks, and calculate XOR distances for them.
    confirmed = BooleanField(default=False)  # indicates if chunk ID is contained in one of confirmed registration tickets
    stored = BooleanField(default=False)

    class Meta:
        database = MASTERNODE_DB
        table_name = 'chunk'

class Masternode(Model):
    ext_address = CharField(unique=True)  # ip:port
    pastel_id = CharField(unique=True)
    active = BooleanField(default=True)  # optionally disable masternode

    class Meta:
        database = MASTERNODE_DB
        table_name = 'masternode'