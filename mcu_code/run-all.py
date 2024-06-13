from pump import *
from ODmeasure import *
from read_temp import *
from oled_screen import *
from DCpump import *
import time

count = 0

sm = StepperMotor(17,21)
sm.run_constant_speed(400)
dcpump = DCpump(12, 27, 15)
dcpump.run(512)
tempsens = TemperatureSensor()
odsens = OD()

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
