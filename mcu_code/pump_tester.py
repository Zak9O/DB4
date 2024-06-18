from dc_pump import *

under_water_pump = dc_pump(12, 27, 15)
big_pump = dc_pump(16, 17, 21)

while True:
    try:
        freq = int(input("Write freq: "))
    except: 
        print("Invalid input. Try again")
        continue
    print("Runnig pumps with freq {}".format(freq))

    under_water_pump.run_freq(freq)
    big_pump.run_freq(freq)
