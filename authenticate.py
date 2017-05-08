from configparser import ConfigParser
cfg = ConfigParser()
cfg.read('clientsecrets.ini')

def get_authkey():
    return cfg.get('auth','authkey').encode('ascii')

def print_authkey():
    print(get_authkey())

def return_authkey():
    auth = get_authkey()
    print("Returning {}".format(auth))
    return auth
