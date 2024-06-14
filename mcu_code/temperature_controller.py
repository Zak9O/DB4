from PID import PID
import read_temp
from dc_pump import *
import time

# kP, kI, kD, setpoint is the desired value, scale is micro seconds

TARGET_TEMP = 17
kP = -2
kI = -0.4
kD = -2
STEP_DELAY = 1 # in seconds

STEP_PIN_NUM = 17
DIR_PIN_NUM = 21

# The further away from the setpoint the higher a value is produced by the PID
# sample time makes the PID change it's value once very X seconds
pid = PID(kP, kI, kD, setpoint=TARGET_TEMP, sample_time=0.1, scale="s") 
pid.output_limits = (0, 1000)

temp_sensor = read_temp.TemperatureSensor()

under_water_pump = dc_pump(12, 27, 15)
under_water_pump.stop()

big_pump = dc_pump(16, 17, 21)

start_time = time.time()

while True:
    current_temperature = temp_sensor.read_temp()
    pid_value = pid(current_temperature)
    elapsed_time = time.time() - start_time

    print("Elapsed time: {:.2f} seconds".format(elapsed_time))
    print("Pid value: {}".format(pid_value))
    print("Temperature: {}".format(current_temperature))
    print("___________")

    if pid_value >= 50:
        big_pump.run_freq(int(pid_value))
    else:
        big_pump.stop()

    with open('exp_1.2.txt', 'a') as f:
        f.write(f"{elapsed_time:.2f},{pid_value},{current_temperature}\n")

    time.sleep(STEP_DELAY)
