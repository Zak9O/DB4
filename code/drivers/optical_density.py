import machine

class OpticalDensity:
    def __init__(self,pin_num = 33):
        self.sensor = machine.ADC(machine.Pin(pin_num))

    def readOD(self):
        value = self.sensor.read() 
        return value
