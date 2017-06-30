import websocket
import threading
import ssl
import time
import sys
import json
import urllib.request
import os

postMessageL = '{"botName": "코인", "botIconImage": "https://upload.wikimedia.org/wikipedia/commons/7/7c/Spaincoin-256.png", "text":"","attachments":[{"title":"실시간 가격", "titleLink": "", "text":"'

postMessageR='", "color": "darkgreen"}]}'
hook = ''

def on_message(wss, message):
    data = json.loads(message)
    if data['action'] == 'create':
        msg = data['content']['text']
        if msg == '@코인':
            gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            res = urllib.request.urlopen("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH&tsyms=KRW", context=gcontext).read()
            jsonRes = json.loads(res)
            ethKRW = jsonRes['RAW']['ETH']['KRW']['PRICE']
            btcKRW = jsonRes['RAW']['BTC']['KRW']['PRICE']
            postpost = 'curl -H "Content-Type: application/json" -X POST -d \'' + postMessageL + 'ETH : ' + str(ethKRW) + "원, BTC : " + str(btcKRW)+"원" + postMessageR+'\' ' +  hook;
            print (postpost)
            os.system(postpost)

def on_error(wss, error):
    print('error')


def on_close(wss):
    print("close")


def on_open(wss):
    def run(*args):
        while True:
            time.sleep(3)
            wss.send('{"type":"ping"}')
    th = threading.Thread(target=run)
    th.start()

if __name__ == "__main__":
    websocket.enableTrace(False)
    if len(sys.argv) < 2:
        host = "web socket host"
    else:
        host = sys.argv[1]
    gheader = {'Cookie:SESSION=', 'User-Agent:'}
    wss = websocket.WebSocketApp(host, header = gheader)
    wss.on_message = on_message
    wss.on_error = on_error
    wss.on_close = on_close
    wss.on_open = on_open
#    wss.connect(host, http_proxy_host="localhost", http_proxy_port=8888, header = gheader)
    wss.run_forever(sslopt={"cert_reqs":ssl.CERT_NONE})

