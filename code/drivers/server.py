import network
import time
from umqtt.robust import MQTTClient
import sys
import os

class Server:
    def __init__(self, coolerPID) -> None:
        self.ADAFRUIT_IO_URL = b'io.adafruit.com'
        self.ADAFRUIT_USERNAME = b'linusjuni'
        self.ADAFRUIT_IO_KEY = b'aio_kjiU52DYYJ0vhH07cyi8QrshCPLh'

        self.PID_SWITCH = 0
        self.coolerPID = coolerPID
        # self.feederPID = feeder
    
    def connect_wifi(self):
        WIFI_SSID = 'DB4GROUP2'
        WIFI_PASSWORD = '12345678'

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

    def get_feedname(self, name):
        return bytes('{:s}/feeds/{:s}'.format(b'linusjuni', name), 'utf-8')

    def publish(self, name, value):
        mqtt_feedname = self.get_feedname(name)
        self.client.publish(mqtt_feedname,
                            bytes(str(value), 'utf-8'),
                            qos=0)

    def subscribe(self):
        self.client.set_callback(self.server_update)
        self.client.subscribe(self.get_feedname(b'remote-controlled-status'))
        self.client.subscribe(self.get_feedname(b'cooler_kP'))
        self.client.subscribe(self.get_feedname(b'cooler_kI'))
        self.client.subscribe(self.get_feedname(b'cooler_kD'))

    def decode_k_msg(self, msg):
        return - float(msg.decode('utf-8'))

    def server_update(self, topic, msg):
        feedname = topic.split(b'/')[-1]
        print("Message received from server")
        print("Message: {}, feedname: {}".format(msg, feedname))
        
        # if(msg == b'Cool'):
        #     self.PID_SWITCH = 1
        # elif(msg == b'Food'):
        #     self.PID_SWITCH = 0
        # else:
        #     msg = int(msg.decode('utf-8'))
    
        if feedname == b'cooler_kP':
            self.coolerPID.Kp = self.decode_k_msg(msg)
        elif feedname == b'cooler_kI':
            self.coolerPID.Ki = self.decode_k_msg(msg)
        elif feedname == b'cooler_kD':
            self.coolerPID.Kd = self.decode_k_msg(msg)
        
        # elif feedname == b'db4.i-value':
        #     if self.PID_SWITCH:
        #         # self.coolerPID.setI(msg)
        #         pass
        #     else:
        #         # self.feederPID.setI(msg)
        #         pass
        #
        # elif feedname == b'db4.d-value':
        #     if self.PID_SWITCH:
        #         # self.coolerPID.setD(msg)
        #         pass
        #     else:
        #         # self.feederPID.setD(msg)
        #         pass
        #
        # else:
        #     self.PID_SWITCH = msg
        #     if self.PID_SWITCH:
        #         # self.publish(b'db4.p-value', self.coolerPID.P)
        #         # self.publish(b'db4.i-value', self.coolerPID.I)
        #         # self.publish(b'db4.d-value', self.coolerPID.D)
        #         pass
        #     else:
        #         # self.publish(b'db4.p-value', self.feederPID.P)
        #         # self.publish(b'db4.i-value', self.feederPID.I)
        #         # self.publish(b'db4.d-value', self.feederPID.D)
        #         pass
