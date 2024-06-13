import pump
pump = pump.StepperMotor(17, 21)

pump.run_constant_speed(500)
while True:
    print("pump should be running")
