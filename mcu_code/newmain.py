from pump import *
from mcu_code.optical_density import *
from read_temp import *
from oled_screen import *
import time
count = 0
tempsens = TemperatureSensor()

sm = StepperMotor(17,21)
sm.setDutyCycle(512)
sm.run_constant_speed(500)

temp = tempsens.measure_temp()
od = optical_density()
screen_on(str(temp),str(od))


while True:
    time.sleep(0.001)

    if count == 100:
        temp = tempsens.measure_temp()
        time.sleep(0.001)
        od = optical_density()
        screen_on(str(temp), str(od))
        count = 0

    time.sleep(0.01)
    count += 1
    