from pump import *
from ODmeasure import *
from read_temp import *
from oled_screen import *
from DCpump import *
import time

count = 0

sm = StepperMotor(17,21)
sm.setDutyCycle(512)
dcpump = DCpump(12, 27, 15)
motor.run(512)
tempsens = TemperatureSensor()
odsens = OD()

temp = tempsens.read_temp()
od = odsens.readOD()
screen_on(str(temp),str(od))

while True:
    time.sleep(0.001)
    if count == 100:
        temp = tempsens.measure_temp()
        time.sleep(0.001)
        od = OD()
        screen_on(str(temp), str(od))
        count = 0

    count += 1