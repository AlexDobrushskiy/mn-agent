import time
from http.client import CannotSendRequest, RemoteDisconnected

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


class BlockChain:
    def __init__(self, user='rt', password='rt', ip='127.0.0.1', rpcport=19932):
        self.url = "http://%s:%s@%s:%s" % (user, password, ip, rpcport)
        self.__reconnect()

    def __reconnect(self):
        while True:
            try:
                newjsonrpc = AuthServiceProxy(self.url)

                # we need this so that we know the blockchain has started
                newjsonrpc.getwalletinfo()
            except ConnectionRefusedError:
                time.sleep(0.1)
            except JSONRPCException as exc:
                if exc.code == -28:
                    time.sleep(0.1)
                else:
                    raise
            else:
                self.__jsonrpc = newjsonrpc
                break

    def __call_jsonrpc(self, name, *params):
        while True:
            f = getattr(self.__jsonrpc, name)
            try:
                if len(params) == 0:
                    ret = f()
                else:
                    ret = f(*params)
            except (BrokenPipeError, CannotSendRequest, RemoteDisconnected) as exc:
                print("RECONNECTING %s" % exc)
                self.__reconnect()
            else:
                break
        return ret

    def help(self):
        return self.__call_jsonrpc("help")

    def addnode(self, node, mode):
        return self.__call_jsonrpc("addnode", node, mode)

    def getlocalfee(self):
        return self.__call_jsonrpc("storagefee", "getlocalfee")

    def getnetworkfee(self):
        return self.__call_jsonrpc("storagefee", "getnetworkfee")

    def getbalance(self):
        return self.__call_jsonrpc("getbalance")

    def getaccountaddress(self):
        return self.__call_jsonrpc("getaccountaddress", "")

    def getpastelidlist(self):
        return self.__call_jsonrpc("pastelid", "list")
