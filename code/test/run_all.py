from drivers.optical_density import *
from drivers.read_temp import *
from drivers.oled_screen import *
from drivers.driver_pump_dc import *
import time

under_water_pump = DcPump(12, 27, 15)
big_pump = DcPump(32, 15, 14)

temp_sens = TemperatureSensor()

while True:
    try:
        freq = int(input("Write freq: "))
        if (freq < 0):
            print("Goodbye")
            break
    except: 
        print("Invalid input. Try again")
        continue

    print("Runnig pumps with freq {}".format(freq))

    under_water_pump.run_freq(freq)
    big_pump.run_freq(freq)
    
    for i in range(10):
        #temp = temp_sens.read_temp()
        #screen_on(str(temp),"wtf")
        #print("Waited for {} seconds. Temp {}".format(i+1, temp))
        time.sleep(1)

    under_water_pump.stop()
    big_pump.stop()
    #screen_on("Waiting for", "input")
