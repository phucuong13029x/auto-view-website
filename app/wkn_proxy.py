import socket
import requests
from sys import stdout


def loadProxy(_protocol, _timeout='10000', _country='all', _ssl='all', _anonymity='all'):
    proxy = []
    try:
        for i in _protocol:
            url = 'https://api.proxyscrape.com/v2/'
            params = {'request': 'displayproxies', 'protocol': i, 'timeout': _timeout, 'country': _country, 'ssl': _ssl, 'anonymity': _anonymity}
            response = requests.get(url, params=params)
            if response.status_code == 200 and response.text:
                aList = response.text.replace("\r", "").split("\n")
                bList = []
                for a in aList:
                    if a is not None and a != '':
                        a = a + ':' + i
                        bList.append(a)
                proxy = proxy + bList
        return proxy
    except:
        return proxy

def liveProxySocks5(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    st = str(ip) + ':' + str(port)
    stdout.write('\r')
    try:
        sock.connect((ip, port))
        stdout.write("Check proxy: %-25s => True " % st)
        return True
    except Exception as e:
        stdout.write("Check proxy: %-25s => False" % st)
        return False
    finally:
        sock.close()

def liveProxyHTTP(ip, port):
    proxy = f"{ip}:{port}"
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    stdout.write('\r')
    try:
        requests.get("https://google.com/", proxies=proxies, timeout=1)
        stdout.write("Check proxy: %-25s => True " % proxy)
        return True
    except:
        stdout.write("Check proxy: %-25s => False" % proxy)
        return False