from wifi.connection import *
from wifi.wifi_list import *
from PID import PID
import read_temp
from dc_pump import *
import time

ADAFRUIT_USERNAME = 'linusjuni'
ADAFRUIT_KEY = 'aio_hEHF11FSb8mtj9G6NMuiSIGJJlvh'

def main():

    TARGET_TEMP = 17
    STEP_DELAY = 1 # in seconds

    check_all_wifis()
    connect_to_wifi('Oscar iPhone', '123456789')

    temperature_client = establish_mqtt_connection(ADAFRUIT_USERNAME, ADAFRUIT_KEY, 'temperature') #temperature
    #TODO: add optical density client

    kP = -2
    kI = -0.4
    kD = -2
    
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
        print("\n")

        if pid_value >= 50:
            big_pump.run_freq(int(pid_value))
        else:
            big_pump.stop()

        with open('exp_1.2.txt', 'a') as f:
            f.write(f"{elapsed_time:.2f},{pid_value},{current_temperature}\n")

        publish_and_request_using_adafruit_io(current_temperature, temperature_client)
        #TODO: add call to pub&sub the optical density

        time.sleep(STEP_DELAY)

if __name__ == "__main__":
    main()