import logging
from blockchain_connector import BlockChain
import requests
from models import Regticket, Chunk

blockchain = BlockChain()

def send_masternode(MY_IP):
    balance = int(blockchain.getbalance())
    address = blockchain.getaccountaddress()
    try:
        pastelid = blockchain.getpastelidlist()[0]['PastelID']
    except:
        pastelid = 'pastelID does not exist'
    # send data
    url = 'http://dobrushskiy.name:8020/api/masternode'
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
    masternode_pastelid = blockchain.getpastelidlist()[0]['PastelID']
    # send data
    url = 'http://dobrushskiy.name:8020/api/regticket'
    data = {"artist_pastelid": artist_pastelid,
            "image_hash": image_hash,
            "status": status,
            "created": created,
            "masternode_pastelid": masternode_pastelid}
    r = requests.post(url, data=data)
    logging.info('regticket')
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
    mn_pastelid = blockchain.getpastelidlist()[0]['PastelID']
    chunk_id = db_data.chunk_id
    image_hash = db_data.image_hash
    indexed = db_data.indexed
    confirmed = db_data.confirmed
    stored = db_data.stored
    # send data
    url = 'http://dobrushskiy.name:8020/api/chunk'
    data = {"mn_pastelid": mn_pastelid,
            "chunk_id": chunk_id,
            "image_hash": image_hash,
            "indexed": indexed,
            "confirmed": confirmed,
            "stored": stored}
    r = requests.post(url, data=data)
    print(r.text)
