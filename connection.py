import network
import time
from umqtt.robust import MQTTClient
import os
import gc
import sys

def connect_to_wifi(ssid, password):

    """
    Description:
    Connects the device to the specified WiFi network.

    Parameters:
    ssid (str): The SSID of the WiFi network.
    password (str): The password of the WiFi network.

    Returns:
    Void

    Raises:
    SystemExit: If the connection to the WiFi network fails after maximum attempts.
    """

    print("Attempting to connect to wifi")
    print("SSID: ", ssid)
    print("PASSWORD: ", password)

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

def publish_and_subscribe_to_adafruit_io(aio_username, aio_key, aio_feedname):

    """
    Description:
    Connects to the Adafruit IO MQTT broker and handles both publishing and subscribing to a specified feed.

    Parameters:
    aio_username (str): The Adafruit IO username.
    aio_key (str): The Adafruit IO key.
    aio_feedname (str): The name of the Adafruit IO feed.

    Returns:
    None

    Raises:
    SystemExit: If the connection to the MQTT server fails.
    """
    
    random_num = int.from_bytes(os.urandom(3), 'little')
    mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

    ADAFRUIT_IO_URL = b'io.adafruit.com' 

    client = MQTTClient(client_id=mqtt_client_id, 
                        server=ADAFRUIT_IO_URL, 
                        user=aio_username, 
                        password=aio_key,
                        ssl=False)
                        
    try:            
        client.connect()
    except Exception as e:
        print('Could not connect to MQTT server {}{}'.format(type(e).__name__, e))
        sys.exit()

    mqtt_feedname = bytes('{:s}/feeds/{:s}'.format(aio_username, aio_feedname), 'utf-8')
    client.set_callback(cb)      
    client.subscribe(mqtt_feedname)  
    PUBLISH_PERIOD_IN_SEC = 10 
    SUBSCRIBE_CHECK_PERIOD_IN_SEC = 0.5 
    accum_time = 0
    while True:
        try:
            # Publish
            if accum_time >= PUBLISH_PERIOD_IN_SEC:
                free_heap_in_bytes = gc.mem_free()
                print('Publish:  freeHeap = {}'.format(free_heap_in_bytes))
                client.publish(mqtt_feedname,    
                            bytes(str(free_heap_in_bytes), 'utf-8'), 
                            qos=0) 
                accum_time = 0                
            
            # Subscribe.  Non-blocking check for a new message.  
            client.check_msg()

            time.sleep(SUBSCRIBE_CHECK_PERIOD_IN_SEC)
            accum_time += SUBSCRIBE_CHECK_PERIOD_IN_SEC
        except KeyboardInterrupt:
            client.disconnect()
            sys.exit()

def cb(topic, msg):
    print('Subscribe:  Received Data:  Topic = {}, Msg = {}\n'.format(topic, msg))
    free_heap = int(str(msg,'utf-8'))