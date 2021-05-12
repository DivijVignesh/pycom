from webserver.customwebserver import *
from network import WLAN
import machine
wlan = WLAN(mode=WLAN.STA)
print(ssid+password)
nets = wlan.scan()
for net in nets:
    if net.ssid == ssid:
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, password), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break
ssid,password=webserver_main()