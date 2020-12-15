import time
from blockchain_connector import BlockChain
import requests

blockchain = BlockChain()

if __name__ == '__main__':
    MY_IP = requests.get('http://ipinfo.io/ip').text.strip()
    while True:
        time.sleep(3)
        balance = int(blockchain.getbalance())
        address = blockchain.getaccountaddress()
        print(balance)
        print(address)
        print(MY_IP)
