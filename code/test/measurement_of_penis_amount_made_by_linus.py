from machine import Pin
from drivers.read_temp import TemperatureSensor
from drivers.driver_pump_dc import DcPump
import time

sensor_temperature = TemperatureSensor()
pumpCooler = DcPump(19, 16, 12)
# fakePump = DcPump(17, 21, 27)

with open("penis_size_made_by_linus_test.csv", 'w') as f:
   f.write(f"Time,Temperature")

start_time = time.time()
pumpCooler.run(200)

while True:
    temperature = sensor_temperature.read_temp()
    elapsed_time = time.time() - start_time
    print(f"At time {elapsed_time} read {temperature}")
    with open("penis_size_made_by_linus_test.csv", 'a') as f:
       f.write(f"\n{elapsed_time},{temperature}")

    time.sleep(1)
