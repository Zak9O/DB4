from math import exp
from machine import Pin
from drivers.PID import PID
from drivers.read_temp import TemperatureSensor
from drivers.driver_pump_dc import DcPump
import drivers.driver_od as driver_od
import drivers.server as server_module
import time
import os

TARGET_TEMP = 17
STEP_DELAY = 1 # in seconds
COOLER_KP = -1.5
COOLER_KI = -0.4
COOLER_KD = -1.5

class Main:

    def run(self):
        print("Starting Program")

        self.initialize_variables()

        self.connect_server()
        print("Connected server successfully")

        count_sync = 0
        count_food = 60*60

        self.start_time = time.time()

        while True:
            self.cooling_actions()

            if count_food == 60 * 60:
                self.food_actions()
                count_food = 0

            self.server.client.check_msg()

            # This is runs every x seconds
            if count_sync == 10:
                print("Syncing and saving data")

                od = self.sensor_od.read_od()
                self.sync_data_to_server(self.current_temperature, od)
                self.save_data_locally(self.current_temperature, od)
                
                count_sync = 0

            print("Tunings: {}".format(self.coolerPID.tunings))
            time.sleep(STEP_DELAY)
            count_sync += 1
            count_food += 1

    def initialize_variables(self):
        self.coolerPID = PID(COOLER_KP, COOLER_KI, COOLER_KD, setpoint=TARGET_TEMP, sample_time=STEP_DELAY, scale="s") 
        self.coolerPID.output_limits = (0, 200)
        
        self.sensor_temperature = TemperatureSensor()
        self.sensor_od = driver_od.od_sensor()

        self.pumpCooler = DcPump(19, 16, 12)
        self.food_pump = DcPump(17, 21, 27)
        
        self.server = server_module.Server(self.coolerPID, self.pumpCooler)

        self.initialize_data_file()

    def initialize_data_file(self):
        self.try_make_data_dir()
        self.file_name = self.make_file_name()

        with open(self.file_name, 'w') as f:
           f.write(f"Time,Temperature,Optical Density")

        print(f"Created: {self.file_name}")

    def try_make_data_dir(self):
        try:
            os.mkdir("data")
        except OSError as e:
            if e.errno == 17:
                pass
            else:
                raise

    def make_file_name(self):
        amount = len(os.listdir("data")) + 1
        return f"data/data_{amount}.csv";

    def connect_server(self):
        server = self.server
        server.connect_wifi()
        server.connect_server()
        server.subscribe()
        
        # Sync the server with values
        # Minus added because values are positive on the server
        server.publish("cooler_kP", - COOLER_KP)
        server.publish("cooler_kI", - COOLER_KI)
        server.publish("cooler_kD", - COOLER_KD)

    def cooling_actions(self):
            self.current_temperature = self.sensor_temperature.read_temp()

            if self.server.remote_controlled:
                print("Remote controlled")
                return
            
            pid_value = self.coolerPID(self.current_temperature)
            print("Temperature:", str(self.current_temperature))
            print("Running pump with frequency: {}".format(pid_value))
            self.pumpCooler.run(int(pid_value))

            if pid_value <= 0:
                self.turn_off_cooler()
            else:
                self.turn_on_cooler()

    def food_actions(self):
        pump_run_time = 2 # self.calculate_food_pump_run_time()

        start_time = time.time()

        self.food_pump.run(1)
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time >= pump_run_time:
                break
            time.sleep(1)

        self.food_pump.stop()

    def calculate_food_pump_run_time(self):
        volume = 4000  # mL
        clearance_rate = 3 * 7.47E-4 # cells / mL / s
        time_between = 2 * 60 * 60 # s
        flow_rate = 12 # mL / s
        od = 8250 # self.sensor_od.read_od()
        cell_concentration = 5.74E+06*exp(-3.42E-4 * od) + -3.13E+5 # cells / mL
        initial_concentration = 6000 # cells / mL

        pump_run_time = - volume * clearance_rate * time_between / (flow_rate * (-clearance_rate * time_between - cell_concentration + initial_concentration))

        return abs(pump_run_time)

    def sync_data_to_server(self, temperature, od):
        server = self.server
        server.publish("temperature", temperature)
        server.publish("optical-density", od)
        server.publish("cooler_pump_rate", self.pumpCooler.get_flow_rate())

    def save_data_locally(self, temperature, od):
        elapsed_time = time.time() - self.start_time
        with open(self.file_name, 'a') as f:
           f.write(f"\n{elapsed_time},{temperature},{od}")

    def turn_on_cooler(self):
        fan = Pin(5, Pin.OUT)
        peltier = Pin(18, Pin.OUT)
        fan.on()
        peltier.on()
       
    def turn_off_cooler(self):
        fan = Pin(5, Pin.OUT)
        peltier = Pin(18, Pin.OUT)

        fan.off()
        peltier.off()


Main().run()
