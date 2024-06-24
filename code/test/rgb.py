import time
import drivers.oled_screen
import drivers.driver_od as driver_od

sensor = driver_od.od_sensor()

while True:
    od = sensor.read_od()
    drivers.oled_screen.screen_on("Od: ", str(od))
    print(f"Od: {od}")
    time.sleep(1)
