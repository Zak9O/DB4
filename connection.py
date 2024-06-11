import network
import socket
import time
import sys

def connect_to_wifi(ssid, password):
    print("Attempting to connect to wifi")
    print("Using SSID: ", ssid)
    print("Using PASSWORD: ", password)

    # Turn off the WiFi Access Point
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    
    # Connect the device to the WiFi network
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(ssid, password)
    
    # Wait until the connection is established
    MAX_ATTEMPTS = 20
    attempt_count = 0
    while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
        print("Attempt number: ", attempt_count)
        attempt_count += 1
        time.sleep(1)
    
    if attempt_count == MAX_ATTEMPTS:
        print('Could not connect to the WiFi network')
        sys.exit()
    
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