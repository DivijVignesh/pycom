import usocket
import _thread
import time
from network import WLAN
import pycom
availablecolor = 0x001100
connectioncolor = 0x110000
ssid=''
password=''
c=0

# Thread for handling a client
def client_thread(clientsocket,n):
    # Receive maxium of 12 bytes from the client
    r = clientsocket.recv(4096)
    urlfind(str(r))
    # If recv() returns with 0 the other end closed the connection
    if len(r) == 0:
        clientsocket.close()
        return
    else:
        # Do something wth the received data...
        print("Received: {}".format(str(r))) #uncomment this line to view the HTTP request

    http = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:close \r\n\r\n" #HTTP response
    if "GET /wifidata?data" in str(r):
        clientsocket.send(http + "<html><body><h1> Entered Ssid and password </h1><br> <a href='/'> go back </a></body></html>")
        
    if "GET / " in str(r):
        #this is a get response for the page   
        # Sends back some data
        c=1
        clientsocket.send(http + "<html><body><h1> You are connection "+ str(n) + "</h1><br> Enter the wifi and password <br>  <label for=\"fname\">First name:</label><input type=\"text\" id=\"ssid\" name=\"ssid\"><br><br><label for=\"password\">Password:</label><input type=\"text\" id=\"password\" name=\"password\"><br><br> <button type=\"button\" onClick=\"submitfunction()\" >Enter</button><script>function submitfunction() {var ssid=document.getElementById(\"ssid\").value ;var password=document.getElementById(\"password\").value ;fetch(\"http://192.168.4.1/wifidata?data=\"+ssid+\"&pass=\"+password);}</script></body></html>")

    elif "GET /color" in str(r):
        pycom.rgbled(0xFFFFFF)
        clientsocket.send(http + "<html><body><h1> You are connection "+ str(n) + "</h1><br> Your browser will send multiple requests <br> <a href='/hello'> hello!</a><br><a href='/color'>change led color!</a></body></html>")
    # Close the socket and terminate the thread
    

    clientsocket.close()
    pycom.rgbled(connectioncolor)
    time.sleep_ms(500)
    pycom.rgbled(availablecolor)  

def urlfind(r):
    position=20
    position=r.find('H')
    start= r.find('?')
    query=r[start:int(position)]
    end=0
    print(query)
    for letter in query:
        if letter=='=':
            start=query.find(letter)
        if letter=='&':
            end=query.find(letter)    
            ssid=query[start+1:end]
            print("ssid:"+ssid)
    passquery=query[end:]
    for l in passquery:
        if l=='=':
            start=passquery.find(l) 
    password=passquery[start+1:]
    print(password)

def webserver_main():
    time.sleep(1)
    wifi = WLAN()
    wifi.init(mode=WLAN.AP, ssid="hello", auth=None, channel=11)
    print("WiFi is up!")
    time.sleep(1)
    pycom.heartbeat(False)
    pycom.rgbled(availablecolor)

    # Set up server socket
    serversocket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    serversocket.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
    serversocket.bind(("192.168.4.1",80 ))

    # Accept maximum of 5 connections at the same time
    serversocket.listen(5)

    # Unique data to send back
    
    while c==0:
        # Accept the connection of the clients
        (clientsocket, address) = serversocket.accept()
        # Start a new thread to handle the client
        _thread.start_new_thread(client_thread, (clientsocket, c))
        
        
    serversocket.close()
    return ssid,password