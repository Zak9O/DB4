import network
import socket
import time

def connect_to_wifi(ssid, password):
    print("Attempting to connect to wifi")

    # Turn off the WiFi Access Point
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    
    # Connect the device to the WiFi network
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(ssid, password)
    
    # Wait until the connection is established
    while not wifi.isconnected():
        time.sleep(1)
    
    print("Connected to WiFi", wifi.ifconfig())

def make_request():
    request = b"GET / HTTP/1.1\r\nHost: www.dtu.dk\r\n\r\n"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("www.dtu.dk", 80))
    s.settimeout(2)
    s.send(request)
    result = s.recv(10000)
    print(result)
    s.close()