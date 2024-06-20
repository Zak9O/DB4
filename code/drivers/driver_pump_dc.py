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

        self.freq = self.DEFAULT_FREQ
        self.pwm.freq(self.DEFAULT_FREQ)
        self.pwm.duty(self.DEFAULT_DUTY)

    def run(self, freq=DEFAULT_FREQ):
        self.freq = freq
        self.in_2.value(1)
        self.pwm.freq(freq)

    def stop(self):
        self.in_2.value(0)

    def get_flow_rate(self, small_pump=True):
        if small_pump:
            return 6.55 + 0.214*self.freq + -6.22E-04*pow(self.freq, 2) + 7.25E-07*pow(self.freq, 3) + -2.94E-10*pow(self.freq, 4)
        else:
            return 4.63 + 0.0358*self.freq + -1.04E-04*pow(self.freq, 2) + 1.24E-07*pow(self.freq, 3) + -5.44E-11*pow(self.freq, 4)

