import time
from drivers.optical_density import *
from drivers.oled_screen import *

od_sensor = OpticalDensity()
od_measurements = []

total_measurements = 10

for i in range(total_measurements):

    measurement = od_sensor.readOD()
    od_measurements.append(measurement)

    print("{}/{}: OD value is: {}".format(i, total_measurements - 1, measurement))
    screen_on(str("{} od: ".format(i)), str(measurement))

    time.sleep(1)

average = sum(od_measurements) / len(od_measurements)
print("Average value is: {}".format(average))
screen_on(str("OD average is: "), str(average))
