# This is Alfred's intelctual property. Use of this code without authorization will be punished.

import time
import pycom
import machine
import socket
import ubinascii 
import array

from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
from pycoproc_1 import Pycoproc
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01

pycom.heartbeat(True)
py = Pycoproc(Pycoproc.PYSENSE)
while(True):

    dht = SI7006A20(py)
    a = int(dht.temperature())

    alt = MPL3115A2(py, mode = ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
    b = int(alt.altitude())

    pres = MPL3115A2(py,mode=PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters
    c = int(pres.pressure())/1000

    li = LTR329ALS01(py)
    d = li.light()
    
    myArray = [0] * 4

    print("The temperature is: " + str(a))
    print("The altitude is: " + str(b))
    print("The pressure is: " + str(c))
    print("The luminosity is: " + str(d))

    if a > 255:
        a = 255
    elif a < 0:
        a = 1
    if b > 255:
        b = 255
    elif b < 0:
        b = 1    
    if c > 255:
        c = 255
    elif c < 0:
        c = 1
    if d > 255:   
        d = 255
    elif d < 0:
        d = 1


    myArray[0] = a - 12
    myArray[1] = b
    myArray[2] = int(c)
    myArray[3] = int((d[0] + d[1]) / 2)
    print(myArray)

    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
    s.setblocking(True)

    s.send(bytes([myArray[0], myArray[1], myArray[2], myArray[3]]))

    s.setblocking(False)
    data = s.recv(128) #this number is the limit of bytes we can send 128 = 256 - 1(255) is the higest value.
    print(data)
    time.sleep(300)