import time
import machine

class StepperMotor:
        
        DEFAULT_delay = 0
        DEFAULT_frequency = 800
        DEFAULT_duty_cycle = 0 
        
        def __init__(self, step_pin_number: int, dir_pin_number : int):
                self.step_pin = machine.Pin(step_pin_number, machine.Pin.OUT)
                self.dir_pin = machine.Pin(dir_pin_number, machine.Pin.OUT)
                
                self.delay = self.DEFAULT_delay
                self.frequency = self.DEFAULT_frequency
                self.duty_cycle = self.DEFAULT_duty_cycle
                self.direction = 0 #clockwise
                
                self.pwm = machine.PWM(step_pin_number, machine.Pin.OUT)
                
        def start(self):
                self.pwm.duty(self.duty_cycle)

        def stop(self):
                self.pwm.duty(0)

        def step(self, steps: int):
                self.start()
                for _ in range(steps):
                        self.pwm.freq(self.frequency)
                        time.sleep(self.delay)
                        self.stop()

        def setDutyCycle(self, dutyCycle : int):
                self.duty_cycle = dutyCycle
                self.pwm.duty(dutyCycle)
        
        def setFreq(self, frequency : int ):
                self.frequency = frequency
                self.pwm.freq(frequency)

        def increase_speed(self, start_freq, end_freq, step, delay):
                for freq in range(start_freq, end_freq, step):
                        self.frequency = freq
                        self.pwm.freq(freq)
                        time.sleep(delay)

        def decrease_speed(self, start_freq, end_freq, step, delay):
                for freq in range(start_freq, end_freq, -step):
                        self.frequency = freq
                        self.pwm.freq(freq)
                        time.sleep(delay)

        def run_constant_speed(self, frequency):
                self.setFreq(frequency)
                self.start()
