from machine import Pin, I2C
import drivers.tcs34725 as tcs34725

def create(integration_time=500, gain=60) -> tcs34725.TCS34725: 
    i2c = I2C(scl=Pin(22), sda=Pin(23), freq=100000)

    sensor = tcs34725.TCS34725(i2c)
    sensor.integration_time(integration_time)
    sensor.gain(gain)

    return sensor
