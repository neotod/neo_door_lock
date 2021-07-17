import time
import argparse
from requests import get, post

resp = get('http://192.168.4.1')
if resp.status_code != 200:
    raise RuntimeError("Can't connect to ESP webserver! Maybe you're not connected to the ESP Access point.")

parser = argparse.ArgumentParser()
parser.add_argument('ssid', help='ssid of the wifi')
parser.add_argument('password', help='password of the wifi')

args = parser.parse_args()

try:
    post('http://192.168.4.1/wifi', data={'ssid': args.ssid, 'password': args.password}, timeout=2)
except:
    pass

time.sleep(2)
print('Done! After connecting to your specified WIFI access point, query http://192.168.1.20/ in your browser to see if ESP is responding.')