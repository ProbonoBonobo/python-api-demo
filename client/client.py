import json
import sys
sys.path.append("../")
from authenticate import get_authkey, print_authkey,return_authkey

class RPCProxy:
    def __init__(self, connection):
        self._connection = connection
    def __getattr__(self, name):
        def do_rpc(*args, **kwargs):
            self._connection.send(json.dumps((name, args, kwargs)))
            result = json.loads(self._connection.recv())
            return result
        return do_rpc

# Example use
from multiprocessing.connection import Client
c = Client(('localhost', 17000), authkey=get_authkey())
proxy = RPCProxy(c)
print(proxy.add(2, 3))
print(proxy.sub(2, 3))
try:
    print(proxy.sub([1, 2], 4))
except Exception as e:
    print(e)
try:
    print(proxy.ls())
except Exception as e:
    print(e)
