import network
import time
from umqtt.robust import MQTTClient
import sys
import os

class Server:
    def __init__(self, coolerPID, cooler_pump) -> None:
        self.ADAFRUIT_IO_URL = b'io.adafruit.com'
        self.ADAFRUIT_USERNAME = b'linusjuni'
        self.ADAFRUIT_IO_KEY = b'aio_gMaH51MWxKfsep8hNOaXpejSNYnt'

        self.PID_SWITCH = 0
        self.coolerPID = coolerPID
        self.remote_controlled = False
        self.cooler_pump = cooler_pump
    
    def connect_wifi(self):
        WIFI_SSID = 'Casper'
        WIFI_PASSWORD = 'heko12345'

        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)

        wifi = network.WLAN(network.STA_IF)
        wifi.active(True)
        wifi.connect(WIFI_SSID, WIFI_PASSWORD)

        MAX_ATTEMPTS = 20
        attempt_count = 0
        while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
            attempt_count += 1
            print("Attempting to connect wifi: {}/{}".format(attempt_count, MAX_ATTEMPTS))
            time.sleep(1)

        if attempt_count == MAX_ATTEMPTS:
            print('could not connect to the WiFi network')
            sys.exit()

    def connect_server(self):
        random_num = int.from_bytes(os.urandom(3), 'little')
        mqtt_client_id = bytes('client_' + str(random_num), 'utf-8')

        self.client = MQTTClient(client_id=mqtt_client_id,
                                 server=self.ADAFRUIT_IO_URL,
                                 user=self.ADAFRUIT_USERNAME,
                                 password=self.ADAFRUIT_IO_KEY,
                                 ssl=False)

        try:
            self.client.connect()
        except Exception as e:
            print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
            sys.exit()
        self.publish("remote_controlled", self.remote_controlled)

    def get_feedname(self, name):
        return bytes('{:s}/feeds/{:s}'.format(b'linusjuni', name), 'utf-8')

    def publish(self, name, value):
        mqtt_feedname = self.get_feedname(name)
        self.client.publish(mqtt_feedname,
                            bytes(str(value), 'utf-8'),
                            qos=0)

    def subscribe(self):
        self.client.set_callback(self.server_update)
        self.client.subscribe(self.get_feedname(b'remote_controlled'))
        self.client.subscribe(self.get_feedname(b'cooler_pump_frequency'))
        self.client.subscribe(self.get_feedname(b'cooler_kP'))
        self.client.subscribe(self.get_feedname(b'cooler_kI'))
        self.client.subscribe(self.get_feedname(b'cooler_kD'))

    def decode_k_msg(self, msg):
        return - float(msg.decode('utf-8'))

    def server_update(self, topic, msg):
        feedname = topic.split(b'/')[-1]
        print("Message received from server")
        print("Message: {}, feedname: {}".format(msg, feedname))
    
        if feedname == b'cooler_kP':
            self.coolerPID.Kp = self.decode_k_msg(msg)
        elif feedname == b'cooler_kI':
            self.coolerPID.Ki = self.decode_k_msg(msg)
        elif feedname == b'cooler_kD':
            self.coolerPID.Kd = self.decode_k_msg(msg)
        elif feedname == b'remote_controlled':
            if msg == b'ON':
                self.remote_controlled = True
            else:
                self.remote_controlled = False
        elif feedname == b'cooler_pump_frequency':
            if self.remote_controlled:
                freq = int(msg.decode('utf-8'))
                if freq == 0:
                    self.cooler_pump.stop()
                else:
                    self.cooler_pump.run(freq)
