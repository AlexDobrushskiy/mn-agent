import logging
from blockchain_connector import BlockChain
import requests
from models import Regticket, Chunk, Masternode
import os
import json

blockchain = BlockChain()

dns_name = "dobrushskiy.name"
port = '8020'
if os.environ.get('CUSTOM_DNS_NAME') is not None:
    if os.environ.get('CUSTOM_PORT') is not None:
        dns_name = os.environ.get('CUSTOM_DNS_NAME')
        port = os.environ.get('CUSTOM_PORT')


def send_masternode(MY_IP):
    balance = int(blockchain.getbalance())
    address = blockchain.getaccountaddress()
    try:
        pastelid = blockchain.getpastelidlist()[0]['PastelID']
    except:
        pastelid = 'pastelID does not exist'

    with open('.pastel/testnet3/masternode.conf', 'r', encoding='utf-8') as g:
        read_data = g.read()
    name = list(json.loads(read_data).keys())[0]
    # send data
    url = 'http://{}:{}/api/masternode'.format(dns_name, port)
    data = {"ip": MY_IP,
            "address": address,
            "balance": balance,
            "pastelID": pastelid,
            "name": name}
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
    try:
        masternode_pastelid = blockchain.getpastelidlist()[0]['PastelID']
    except:
        masternode_pastelid = 'pastelID does not exist'
    # send data
    url = 'http://{}:{}/api/regticket'.format(dns_name, port)
    data = {"artist_pastelid": artist_pastelid,
            "image_hash": image_hash,
            "status": status,
            "created": created,
            "masternode_pastelid": masternode_pastelid}
    r = requests.post(url, data=data)
    logging.info('regticket')
    # print(r.text)


def send_chunks(last_chunk_id):
    all_chunks = Chunk.select()
    new_chunk_id = last_chunk_id
    for db_data in all_chunks:
        if db_data.id > last_chunk_id:
            send_chunk(db_data)
            new_chunk_id = db_data.id
    return new_chunk_id


def send_chunk(db_data):
    chunk_id = db_data.chunk_id
    image_hash = db_data.image_hash
    indexed = db_data.indexed
    confirmed = db_data.confirmed
    stored = db_data.stored
    try:
        mn_pastelid = blockchain.getpastelidlist()[0]['PastelID']
    except:
        mn_pastelid = 'pastelID does not exist'
    # send data
    url = 'http://{}:{}/api/chunk'.format(dns_name, port)
    data = {"mn_pastelid": mn_pastelid,
            "chunk_id": chunk_id,
            "image_hash": image_hash,
            "indexed": indexed,
            "confirmed": confirmed,
            "stored": stored}
    r = requests.post(url, data=data)
    # print(r.text)


def mn_connections():
    connections = blockchain.getpeerinfo()
    data = []
    try:
        mn_pastelid = blockchain.getpastelidlist()[0]['PastelID']
    except:
        mn_pastelid = 'pastelID does not exist'
    for connection in connections:
        ip = connection['addr']
        clear_ip = ip.split(':')[0]
        masternodes = Masternode.select()
        for masternode in masternodes:
            if masternode.ext_address.split(':')[0] == clear_ip:
                pastelid = masternode.pastel_id
                active = masternode.active
                part = {'masternode_pastelid': mn_pastelid,
                        'ip': clear_ip,
                        'remote_pastelid': pastelid,
                        'active': active}
                data.append(part)

    # print(data)
    url = 'http://{}:{}/api/mn_connection'.format(dns_name, port)
    r = requests.post(url, json=data)
    print(r.text)
