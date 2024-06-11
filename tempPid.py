import stepper2
import measureTemp

def tempPid(prevErr,intSum):
    p = 0
    i = 0
    d = 0
    desiredTemp = 17
    integral = intSum

    curTemp = measureTemp()
    err = curTemp - desiredTemp
    dt = 2
    
    proportional = err * p
    integral = intSum + (i * err * dt)
    derivative = d * (err - prevErr)/dt

    pid = proportional + integral + derivative

    status = stepper2(pid)

    return [integral,err,status,curTemp]




