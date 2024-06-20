import machine

class DcPump:
    
    DEFAULT_FREQ = 1000
    DEFAULT_DUTY = 500

    def __init__(self, inputC, inputD, EnableA):
        self.in_1 = machine.Pin(inputC, machine.Pin.OUT)
        self.in_2 = machine.Pin(inputD, machine.Pin.OUT)
        self.enabler = machine.Pin(EnableA, machine.Pin.OUT)

        self.in_1.value(0)
        self.in_2.value(0)
        self.pwm = machine.PWM(self.enabler)

        self.pwm.freq(self.DEFAULT_FREQ)
        self.pwm.duty(self.DEFAULT_DUTY)

    def run(self, freq=DEFAULT_FREQ):
        self.in_2.value(1)
        self.pwm.freq(freq)

    def stop(self):
        self.in_2.value(0)
