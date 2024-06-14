import mcu_code.dc_pump as dc_pump
pump = dc_pump.smallDCpump(16, 17, 21)

pump.run_freq(1000)
while True:
    print("pump should be running")
