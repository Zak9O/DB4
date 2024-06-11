import tempPid
import odPid
from server import *

def controller():
    stepper1 = ""
    stepper2 = ""

    intTemp = 0
    errTemp = 0
    intOD = 0
    errOD = 0
    time = 0

    while True:
        array1 = tempPid(errTemp,intTemp)
        array2 = odPid(errOD,intOD)

        intTemp = array1[0]
        errTemp = array1[1]
        stepper1 = array1[2]
        temp = array1[3]

        intOD = array2[0]
        errOD = array2[1]
        stepper2 = array2[2]
        OD = array2[3]

        serverUpload(temp,stepper1,OD,stepper2,time)

        wait(2)
        time += 2
