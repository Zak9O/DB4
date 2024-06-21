from machine import Pin, PWM

in1 = Pin(17, Pin.OUT)
in2 = Pin(21, Pin.OUT)
enA = Pin(27, Pin.OUT)

in3 = Pin(19, Pin.OUT)
in4 = Pin(16, Pin.OUT)
enB = Pin(12, Pin.OUT)

# One in-pin should be high
in1.value(0)
in2.value(1)

# One in-pin should be high
in3.value(0)
in4.value(1)

pwm1 = PWM(enA)
pwm1.freq(1000)
pwm1.duty(500)

pwm2 = PWM(enB)
pwm2.freq(1000)
pwm2.duty(500)

while True:
    print("Running motor")

import LargeDCMotor as motor

pump = motor.LargeDCMotor(16, 17, 21)
pump.start()
# while True:
#     print("IT SHOULD FUCKING RUN YOU IDIOT")
