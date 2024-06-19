import machine

class dc_pump:
    
    DEFAULT_FREQ = 1000
    DEFAULT_DUTY = 500

    def __init__(self, inputC, inputD, EnableA):
        self.InC = machine.Pin(inputC, machine.Pin.OUT)
        self.InD = machine.Pin(inputD, machine.Pin.OUT)
        self.EnA = machine.Pin(EnableA, machine.Pin.OUT)

        self.InC.value(1)
        self.InD.value(0)
        self.pwmA = machine.PWM(self.EnA)
        self.pwmA.freq(self.DEFAULT_FREQ)
        self.pwmA.duty(self.DEFAULT_DUTY)

    def setDutyCycle(self, duty):
        self.pwmA.duty(duty)

    def run(self, duty):
        self.setDutyCycle(duty)
        self.InC.value(1)
        self.InD.value(0)

    def run_freq(self,freq_val):
        self.pwmA.freq(freq_val)
        self.run(self.DEFAULT_DUTY)

    def stop(self):
        self.pwmA.duty(0)
