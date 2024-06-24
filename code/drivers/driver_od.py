from machine import Pin, I2C
import drivers.tcs34725 as tcs34725
import time

class od_sensor:
    def __init__(self, integration_time=500, gain=60):
        i2c = I2C(scl=Pin(22), sda=Pin(23), freq=100000)

        self.sensor = tcs34725.TCS34725(i2c)
        self.sensor.integration_time(integration_time)
        self.sensor.gain(gain)
    
    def read_od(self):
        values = []
        for _ in range(20):
            (_, blue, _, _) = self.sensor.read(True)
            values.append(blue)
            time.sleep(0.01)

        average = sum(values) / len(values)
        return average
