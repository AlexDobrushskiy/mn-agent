import time
from blockchain_connector import BlockChain
from jobs import send_masternode, send_regtickets, send_chunks, mn_connections
import requests
import logging

blockchain = BlockChain()

if __name__ == '__main__':
    logging.basicConfig(filename='agent.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
    logging.info('Started')

    MY_IP = requests.get('http://ipinfo.io/ip').text.strip()
    last_regticket_id = 0
    last_chunk_id = 0
    while True:
        time.sleep(3)
        # masternode
        send_masternode(MY_IP)
        # regticket
        last_regticket_id = send_regtickets(last_regticket_id)
        # chunck
        last_chunk_id = send_chunks(last_chunk_id)
        # connections
        mn_connections()
