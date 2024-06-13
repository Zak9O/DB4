import time
import machine

class DCpump:
    
    DEFAULT_FREQ = 1000
    DEFAULT_DUTY = 450

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
        while True:
            print("Running pump at duty cycle: ", duty)
            time.sleep(1)  # Just keep running

motor = DCpump(12, 27, 15)
motor.run(512)

#motor.run(450)  # Run the pump continuously at a duty cycle of 450
