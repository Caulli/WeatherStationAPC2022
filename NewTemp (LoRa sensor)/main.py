# GROUP 8
#please make sure that the python interpreter is disabled, otherwise the code will not compile and run

#normal micropython libraries
import time
import pycom
import machine
import socket
import ubinascii 
import array

#special libraries of the Lopy
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
from pycoproc_1 import Pycoproc
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01

pycom.heartbeat(False) #setting the led hearthbeat to false so it is not always blinking due to led being extremly bright
py = Pycoproc(Pycoproc.PYSENSE)

#everything is in a while(true) loop so it runs continously
while(True):

    dht = SI7006A20(py)
    a = int(dht.temperature()) # a - temperature
    b = int(dht.humidity()) # b - humidity

    pres = MPL3115A2(py,mode=PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters
    c = int(pres.pressure())/1000 # c - pressure, we divide the pressure by 1000 so we are interpreting it as KPa

    li = LTR329ALS01(py)
    d = li.light() # d - light

    #creating an array of 4
    myArray = [0] * 4

    #printing the sent values to the terminal to get a visual representation of what the sensors are sending
    print("The temperature is: " + str(a))
    print("The humidity is: " + str(b))
    print("The pressure is: " + str(c))
    print("The luminosity is: " + str(d))

    #if clauses to fix potetial crashes due to the limit of the size of the data we can send
    if a > 255:
        a = 255
    elif a < 0:
        a = 0
    if b > 255:
        b = 255
    elif b < 0:
        b = 0    
    if c > 255:
        c = 255
    elif c < 0:
        c = 0
    if d > 255:   
        d = 255
    elif d < 0:
        d = 0

    myArray[0] = a - 12 #temperature is too high so we subtract 12 from the original value to "calibrate" it
    myArray[1] = b
    myArray[2] = int(c)
    myArray[3] = int((d[0] + d[1]) / 2) # Strange behaviour: First time it sends data after pluging it in, it reads 0 as luminosity
    print(myArray)

    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW) # create a LoRa socket again in case the first one failed
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5) # set the LoRaWAN data rate again in case the first one failed
    s.setblocking(True)

    s.send(bytes([myArray[0], myArray[1], myArray[2], myArray[3]])) #sending the actual data

    s.setblocking(False)
    data = s.recv(128) #this number is the limit of bytes we can send 128 = 256 - 1(255) is the higest value.
    print(data)
    pycom.rgbled(0xff00) #setting  the rgb led to green to get a visual sign that the LoRa is sending data.
    time.sleep(300) #sending data every 5 minutes