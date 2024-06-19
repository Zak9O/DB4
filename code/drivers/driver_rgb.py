from machine import Pin, I2C
import tcs34725 as rgb_driver

"""
Access the rgb method by accessing the rgb field of the class
"""
class RGBSensor:

    def __init__(self) -> None:
        i2c = I2C(scl=Pin(22), sda=Pin(23), freq=100000)
        self.rgb =  rgb_driver.TCS34725(i2c)
