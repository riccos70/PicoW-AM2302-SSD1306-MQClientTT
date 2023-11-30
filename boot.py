# boot.py -- run on boot-up
import network, utime, machine, ujson

with open('config.json', 'r') as f:
    config = ujson.load(f)

# Replace the following with your WIFI Credentials
SSID = config['WIFI']['SSID']
SSID_PASSWORD = config['WIFI']['PASSWORD']

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSID_PASSWORD)
        while not sta_if.isconnected():
            print("Attempting to connect....")
            utime.sleep(1)
    print('Connected! Network config:', sta_if.ifconfig())
    
print("Connecting to your wifi...")
do_connect()