from ODmeasure import *
import machine
from oled_screen import *
import time

odsens = OD()
od = odsens.readOD()
count = 0

screen_on(str("temp"), str(od))
start_time = time.time()

while True:
    elapsed_time = time.time() - start_time
    
    if count == 3:
        time.sleep(0.001)
        od = odsens.readOD()
        screen_on(str("temp"), str(od))

        with open('od_test.txt', 'a') as f:
            f.write(f"{elapsed_time:.2f},{od}\n")

        count = 0

    count += 1
    time.sleep(1)