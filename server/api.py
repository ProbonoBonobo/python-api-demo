# rpcserver.py
import json
import os
import sys
sys.path.append("../")
from authenticate import get_authkey, print_authkey,return_authkey

class RPCHandler:
    def __init__(self):
        self._functions = { }

    def register_function(self, func):
        self._functions[func.__name__] = func

    def handle_connection(self, connection):
        try:
            while True:
                # Receive a message
                func_name, args, kwargs = json.loads(connection.recv())
                # Run the RPC and send a response
                try:
                    r = self._functions[func_name](*args,**kwargs)
                    connection.send(json.dumps(r))
                except Exception as e:
                    connection.send(json.dumps(str(e)))
        except EOFError:
             pass

# Example use
from multiprocessing.connection import Listener
from threading import Thread

def rpc_server(handler, address, authkey):
    sock = Listener(address, authkey=authkey)
    while True:
        client = sock.accept()
        t = Thread(target=handler.handle_connection, args=(client,))
        t.daemon = True
        t.start()

# Some remote functions
def add(x, y):
    return x + y

def sub(x, y):
    return x - y

def ls():
    return os.listdir()

def print_creds():
    print("======== SUPER SECRET CREDENTIALS =========")
    print("Authkey is {} (type: {})".format(get_authkey(), type(get_authkey())))

# Register with a handler
handler = RPCHandler()
handler.register_function(add)
handler.register_function(sub)
handler.register_function(ls)
handler.register_function(print_creds)

# Run the server

rpc_server(handler, ('localhost', 17000), authkey=get_authkey())
