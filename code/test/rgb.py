import time
import drivers.driver_rgb as rgb_driver
import drivers.oled_screen

sensor = rgb_driver.RGBSensor()

while True:
    value = sensor.rgb.read(True)
    drivers.oled_screen.screen_on("Value", str(value))
    time.sleep(1)
