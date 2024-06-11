from machine import Pin
import time

pump_pin = Pin(26, Pin.OUT)

def make_wave():
    pump_pin.off()
    pump_pin.on()
    
while True:
    print("Making one iteration")
    make_wave()
    time.sleep(0.1)
    
