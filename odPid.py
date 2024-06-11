import measureOD
import stepper1

def odPid(prevErr, intSum):
    p = 0
    i = 0
    d = 0
    desiredOD = 0
    integral = intSum

    curOD = measureOD()
    err = curOD - desiredOD
    dt = 2

    proportional = err * p
    integral = intSum + (i * err * dt)
    derivative = d * (err - prevErr)/dt

    pid = proportional + integral + derivative

    status = stepper1(pid)

    return [integral,err,status,curOD]