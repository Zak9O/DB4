import drivers.ssd1306
from machine import I2C, Pin

def screen_on(temp, od):
    i2c = I2C(scl=Pin(22), sda=Pin(23), freq=100000)
    oled = drivers.ssd1306.SSD1306_I2C(128, 32, i2c)
    oled.fill(0)
    oled.text(f"Temp: {temp}", 0, 8)
    oled.text(f"OD: {od}", 8, 16)
    oled.show()
