from wifi.connection import *
from wifi.wifi_list import *
from drivers.PID import PID
from drivers.read_temp import *
from drivers.driver_pump_dc import *
import time
from drivers.optical_density import *


ADAFRUIT_USERNAME = 'linusjuni'
ADAFRUIT_KEY = 'aio_VxPe46XaH0DLnHZzzj2Qi60tXTKA'

# Creating objects
under_water_pump = DcPump(12, 27, 15)
under_water_pump.stop()

big_pump = DcPump(16, 17, 21)

optical_density_sensor = OpticalDensity()

def main():

    TARGET_TEMP = 17
    STEP_DELAY = 1 # in seconds

    check_all_wifis()
    connect_to_wifi('DB4GROUP2', '12345678')

    temperature_client = establish_mqtt_connection(ADAFRUIT_USERNAME, ADAFRUIT_KEY, 'temperature')
    optical_density_client = establish_mqtt_connection(ADAFRUIT_USERNAME, ADAFRUIT_KEY, 'optical-density')
    remote_controlled_status_client = establish_mqtt_connection(ADAFRUIT_USERNAME, ADAFRUIT_KEY, 'remote-controlled-status')
    cooling_pump_client = establish_mqtt_connection(ADAFRUIT_USERNAME, ADAFRUIT_KEY, 'cooling-pump')

    kP = -2
    kI = -0.4
    kD = -2

    start_time = time.time()
    
    pid = PID(kP, kI, kD, setpoint=TARGET_TEMP, sample_time=0.1, scale="s") 
    pid.output_limits = (0, 1000)

    temp_sensor = TemperatureSensor()

    while True:
        remote_controlled_status = request_using_adafruit_io(remote_controlled_status_client)
        remote_status_mode = get_message()

        print("The remote status is:", remote_status_mode)
        time.sleep(2)

        if remote_status_mode == 0 or remote_controlled_status == None:
            temperature_from_sensor = temp_sensor.read_temp()
            optical_density_from_sensor = optical_density_sensor.readOD()

            elapsed_time = time.time() - start_time

            temperature = publish_and_request_using_adafruit_io(temperature_from_sensor, temperature_client)
            optical_density = publish_and_request_using_adafruit_io(optical_density_from_sensor, optical_density_client)

            pid_value = pid(temperature)

            print("Elapsed time: {:.2f} seconds".format(elapsed_time))
            print("Pid value: {}".format(pid_value))
            print("Temperature: {}".format(temperature))
            print("Optical Density: {}".format(optical_density))
            print("\n")

            if pid_value >= 50:
                big_pump.run_freq(int(pid_value))
            else:
                big_pump.stop()

            # TODO: When we want to log data in a file:
            # with open('exp_1.2.txt', 'a') as f:
            #    f.write(f"{elapsed_time:.2f},{pid_value},{temperature}\n")

            time.sleep(STEP_DELAY)

        elif remote_status_mode == 1:
            request_using_adafruit_io(cooling_pump_client)
            pid_value = get_message()
            print("The PID value is", pid_value)
            big_pump.run_freq(int(pid_value))

if __name__ == "__main__":
    main()