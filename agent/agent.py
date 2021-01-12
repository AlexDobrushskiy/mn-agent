import time
from blockchain_connector import BlockChain
import requests
import json

blockchain = BlockChain()

if __name__ == '__main__':
    MY_IP = requests.get('http://ipinfo.io/ip').text.strip()
    while True:
        time.sleep(3)
        balance = int(blockchain.getbalance())
        address = blockchain.getaccountaddress()
        try:
            pastelid = blockchain.getpastelidlist()[0]['pastelID']
        except:
            print('pastelID does not exist')
            pastelid = 'asda'
        # print(balance)
        # print(address)
        # print(MY_IP)
        # print(blockchain.help())
        url = ' http://dobrushskiy.name:8020/api/masternode'
        data = {"ip": MY_IP,
                "address": address,
                "balance": balance,
                "pastelID": pastelid}
        # print(data)
        s = requests.put(url, data=data)
        print(s.text)

