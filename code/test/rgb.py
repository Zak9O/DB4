import time
from machine import Pin, I2C
import drivers.oled_screen
import drivers.tcs34725 as rgb_driver

i2c = I2C(scl=Pin(22), sda=Pin(23), freq=100000)
sensor = rgb_driver.TCS34725(i2c)

sensor.integration_time(500) #value between 2.4 and 614.4.
sensor.gain(60) #must be a value of 1, 4, 16, 60

def color_rgb_bytes_new(color_raw):
    r, g, b, clear = color_raw
    if clear == 0:
        return "err"
    red = int(pow((int((r/clear) * 256) / 255), 2.5) * 255)
    green = int(pow((int((g/clear) * 256) / 255), 2.5) * 255)
    blue = int(pow((int((b/clear) * 256) / 255), 2.5) * 255)

    return (blue, b)

count = 0
valsred = []
valsr = []
while count < 20 :
    value = sensor.read(True)
    red, r = color_rgb_bytes_new(value)
    drivers.oled_screen.screen_on("Value", str((red, r)))
    time.sleep(0.5)
    print(red)
    print(r)
    valsred.append(red)
    valsr.append(r)
    count += 1


avgred = sum(valsred)/len(valsred)
avgr = sum(valsr)/len(valsr)
print(avgred)
print(avgr)
