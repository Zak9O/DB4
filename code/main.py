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

        count = 0

        self.start_time = time.time()

        while True:
            self.cooling_actions()
            self.underwaterPump.run(200)

            # TODO add control for food pump

            self.server.client.check_msg()

            # This is runs every x seconds
            if count == 10:
                print("Syncing and saving data")
                # TODO Change 300 to the value of the od sensor
                self.sync_data_to_server(self.current_temperature, 300)
                self.save_data_locally(self.current_temperature, 300)
                
                count = 0

            print("Tunings: {}".format(self.coolerPID.tunings))
            time.sleep(STEP_DELAY)
            count += 1

    def initialize_variables(self):
        self.coolerPID = PID(COOLER_KP, COOLER_KI, COOLER_KD, setpoint=TARGET_TEMP, sample_time=STEP_DELAY, scale="s") 
        self.coolerPID.output_limits = (0, 200)
        
        self.sensor_temperature = TemperatureSensor()
        #self.sensor_od = driver_od.create() 

        self.pumpCooler = DcPump(17, 21, 27)
        self.underwaterPump = DcPump(19,16,12)
        
        self.server = server_module.Server(self.coolerPID)

        self.initialize_data_file()

    def initialize_data_file(self):
        self.try_make_data_dir()
        self.file_name = self.make_file_name()

        with open(self.file_name, 'w') as f:
           f.write(f"Time,Temperature,Optical Density\n")

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
            pid_value = self.coolerPID(self.current_temperature)
            print("Temperature:", str(self.current_temperature))
            print("Running pump with frequency: {}".format(pid_value))
            self.pumpCooler.run(int(pid_value))

    def sync_data_to_server(self, temperature, od):
        server = self.server
        server.publish("temperature", temperature)
        server.publish("optical-density", od)
        server.publish("cooler_pump_rate", self.pumpCooler.get_flow_rate())

    def save_data_locally(self, temperature, od):
        elapsed_time = time.time() - self.start_time
        with open(self.file_name, 'a') as f:
           f.write(f"{elapsed_time},{temperature},{od}\n")
        pass

Main().run()
