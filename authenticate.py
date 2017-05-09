import sys
import os
from configparser import ConfigParser
sys.path.append("/Users/kz/Projects/redux-dev/redux/examples/rnn-party/api")
os.chdir("/Users/kz/Projects/redux-dev/redux/examples/rnn-party/api")
global cfg
cfg = ConfigParser()
cfg.read('clientsecrets.ini')

def Config():
    from configparser import ConfigParser
    print("Returning the config object: {}".format(cfg))
    return cfg

def print_sections():
    ret =  cfg.sections()
    print("Sections in {}: {}".format('clientsecrets.ini', ret))
    return ret

def get_authkey():
    return cfg.get('auth','authkey').encode('ascii')

def print_authkey():
    print(get_authkey())

def return_authkey():
    auth = get_authkey()
    print("Returning {}".format(auth))
    return auth

if __name__ == '__init__':
    print_sections()