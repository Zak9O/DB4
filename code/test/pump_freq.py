from drivers.driver_pump_dc import *
import time

under_water_pump = DcPump(12, 27, 15)
big_pump = DcPump(16, 17, 21)

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
        time.sleep(1)
        print("Waited for {} seconds".format(i+1))
        
    under_water_pump.stop()
    big_pump.stop()
