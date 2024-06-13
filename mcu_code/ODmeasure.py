import machine
import time


class OD:
    def __init__(self,pin):
        sensor = machine.ADC(machine.Pin(33))

    def readOD(self):
        value = self.sensor.read() 
        print("reading")
        return value

 