from pump import *
from mcu_code.optical_density import *
from read_temp import *
from oled_screen import *
from dc_pump import *
import time

count = 0

dcpump = dc_pump(12, 27, 15)
dcpump.run(256)
tempsens = TemperatureSensor()
odsens = optical_density()

temp = tempsens.read_temp()
od = odsens.readOD()
screen_on(str(temp), str(od))

while True:
    print("Loop run at count {}".format(count))
    time.sleep(0.001)
    
    if count == 100:
        temp = tempsens.read_temp()
        time.sleep(0.001)
        od = odsens.readOD()
        screen_on(str(temp), str(od))
        count = 0

    count += 1
