from pyautogui import size
import os
from sys import stdout
import time
import json
from urllib.request import urlretrieve, urlopen
import re as r
from app.wkn_firebase import DatabaseFB
import requests
from random import choice


def readFile(path):
    if os.path.isfile(path) is True:
        list_out = []
        with open(path, "r", encoding="utf8") as f:
            lines = f.readlines()
            f.close()
        for i in lines:
            list_out.append(i.replace("\n", ""))
        return list_out
    return False

def writeFile(path, data):
    with open(path, 'w', encoding='utf8') as f:
        for r in data:
            f.write(r)
            f.write("\n")
        f.close()

def printDefault(strs):
    print("*" * os.get_terminal_size().columns)
    print(strs)

def loadScreen(key ,number, hidden):
    position = []
    screen_size = size()
    if key == 1:
        default_size = screen_size.width // number
    else:
        default_size = screen_size.width
    for i in range(number):
        if hidden == 'True':
            position.append((default_size * i) + screen_size.width)
        else:
            position.append(default_size * i)
    return default_size, screen_size.height, position

def wait_time(number):
    for i in range(number):
        stdout.write('\r')
        stdout.write("PLEASE WAIT AFTER: %-4s SECOND" % (number - i))
        stdout.flush()
        time.sleep(1)
    print('\n')

# # GET IP PUBLIC
# def getIP():
#     d = str(urlopen('http://checkip.dyndns.com/').read())
#     return r.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)

# def checkLicense(userid, key):
#     data = DatabaseFB().getDB(parent='users', child=userid)
#     data = json.loads(json.dumps(data))
#     license_check = ""
#     if data['license'][0]['key'] == key and data['ip'] == getIP() and data['license'][0]['expires'] >= time.time():
#         license_check = 1
#     return license_check
