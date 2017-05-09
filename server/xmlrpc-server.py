from xmlrpc.server import SimpleXMLRPCServer


class KeyValueServer:
    _rpc_methods_ = ['get', 'set', 'delete', 'exists', 'keys', 'add']
    def __init__(self, address):
        self._data = {}
        self._serv = SimpleXMLRPCServer(address, allow_none=True)
        for name in self._rpc_methods_:
            self._serv.register_function(getattr(self, name))
    def get(self, name):
        return self._data[name]
    def set(self, name, value):
        self._data[name] = value
    def delete(self, name):
        del self._data[name]
    def exists(self, name):
        return name in self._data
    def keys(self):
        return list(self._data)
    def serve_forever(self):
        self._serv.serve_forever()

class RPCServer(KeyValueServer):
  def add(self, x, y):
    return x + y

# Example
if __name__ == '__main__':
    kvserv = RPCServer(('', 15000))

    kvserv.serve_forever()
