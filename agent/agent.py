import time
from blockchain_connector import BlockChain
import requests
from peewee import (Model, SqliteDatabase, BlobField, DateTimeField, DecimalField, BooleanField, IntegerField,
                    CharField,
                    ForeignKeyField)

MASTERNODE_DB = SqliteDatabase('./.pastel/masternode.db')

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


blockchain = BlockChain()

if __name__ == '__main__':
    MY_IP = requests.get('http://ipinfo.io/ip').text.strip()
    def send_masternode():
        balance = int(blockchain.getbalance())
        address = blockchain.getaccountaddress()
        try:
            pastelid = blockchain.getpastelidlist()[0]['pastelID']
        except:
            pastelid = 'pastelID does not exist'
        # send data
        url = ' http://dobrushskiy.name:8020/api/masternode'
        data = {"ip": MY_IP,
                "address": address,
                "balance": balance,
                "pastelID": pastelid}
        r = requests.put(url, data=data)


    def send_regtickets(last_regticket_id):
        all_regtickets = Regticket.select()
        new_regticket_id = last_regticket_id
        for db_data in all_regtickets:
            if db_data.id > last_regticket_id:
                send_regticket(db_data)
                new_regticket_id = db_data.id
        return new_regticket_id

    def send_regticket(db_data):
        artist_pastelid = db_data.artist_pk
        image_hash = db_data.image_hash
        status = db_data.status
        created = db_data.created
        masternode_pastelid = blockchain.getaccountaddress()
        # send data
        url = ' http://dobrushskiy.name:8020/api/regticket'
        data = {"artist_pastelid": artist_pastelid,
                "image_hash": image_hash,
                "status": status,
                "created": created,
                "masternode_pastelid": masternode_pastelid}
        r = requests.post(url, data=data)
        print(r.text)

    def send_chunks(last_chunk_id):
        all_chunks = Chunk.select()
        new_chunk_id = last_chunk_id
        for db_data in all_chunks:
            if db_data.id > last_chunk_id:
                send_chunk(db_data)
                new_chunk_id = db_data.id
        return new_chunk_id

    def send_chunk(db_data):
        mn_pastelid = blockchain.getaccountaddress()
        chunk_id = db_data.chunk_id
        image_hash = db_data.image_hash
        indexed = db_data.indexed
        confirmed = db_data.confirmed
        stored = db_data.stored
        # send data
        url = ' http://dobrushskiy.name:8020/api/chunk'
        data = {"mn_pastelid": mn_pastelid,
                "chunk_id": chunk_id,
                "image_hash": image_hash,
                "indexed": indexed,
                "confirmed": confirmed,
                "stored": stored}
        r = requests.post(url, data=data)
        print(r.text)

    last_regticket_id = 0
    last_chunk_id = 0
    while True:
        time.sleep(3)
        # masternode
        send_masternode()
        # regticket
        last_regticket_id = send_regtickets(last_regticket_id)
        # chunck
        last_chunk_id = send_chunks(last_chunk_id)
