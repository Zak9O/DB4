import machine
import time

def OD():
    sensor = machine.ADC(machine.Pin(33))
    value = sensor.read() 
    print(value)
    time.sleep(0.001)
    print("measureing")
    return value
 