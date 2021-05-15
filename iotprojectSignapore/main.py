from iotprojectSignapore.ctsensor import CtCurrent
from network import WLAN 
from mqtt.mqtt import MQTTClient 
import machine 
import time 
def sub_cb(topic, msg): 
   print(msg) 
print("Connecting to wifi") 
wlan = WLAN(mode=WLAN.STA) 
wlan.connect("Dilip Divij", auth=(WLAN.WPA2, "dilipdivij123"), timeout=5000) 

while not wlan.isconnected():  
    machine.idle() 
print("Connected to Wif in") 


while True:
    current=CtCurrent()
    #write for accelerometer sensors

    client = MQTTClient("device_id", "io.adafruit.com",user="Divijvignesh", password="aio_WTIp99fn1T6H3akqkZhCZcK2CAoK", port=1883) 
    client.set_callback(sub_cb) 
    client.connect()
    # client.subscribe(topic="Divijvignesh/feeds/CurrentValues") 
    client.publish(topic="Divijvignesh/feeds/CurrentValues", msg=str(current))
    print("Published data ="+str(current))
    client.disconnect()

    time.sleep(10)

