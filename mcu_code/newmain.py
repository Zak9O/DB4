from pump import *
from ODmeasure import *
from read_temp import *
from oled_screen import *
import time
count = 0

temp = measure_temp()
od = OD()
screen_on(str(temp),str(od))

while True:
    run_with_pwm()
    time.sleep(0.001)

    if count == 100:
        temp = measure_temp()
        time.sleep(0.001)
        od = OD()
        screen_on(str(temp), str(od))
        count = 0

    time.sleep(0.01)
    count += 1
    