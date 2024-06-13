from PID import PID
import read_temp
import pump

import time

# kP, kI, kD, setpoint is the desired value, scale is micro seconds

TARGET_TEMP = 23
kP = 1
kI = 1
kD = 1
STEP_DELAY = 1 # in seconds

STEP_PIN_NUM = 1
DIR_PIN_NUM = 1

# The further away from the setpoint the higher a value is produced by the PID
# sample time makes the PID change it's value once very X seconds
pid = PID(kP, kI, kD, setpoint=TARGET_TEMP, sample_time=0.1, scale="s") 

temp_sensor = read_temp.TemperatureSensor()
pump = pump.StepperMotor(STEP_PIN_NUM, DIR_PIN_NUM)

while True:
    current_temperature = temp_sensor.read_temp()
    pid_value = pid(current_temperature)

    if pid_value > 1:
        pump.increase_speed(pid_value * 1000)
    else:
        pump.stop()

    time.sleep(STEP_DELAY)
