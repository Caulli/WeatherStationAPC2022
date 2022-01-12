# GROUP 8
#please make sure that the python interpreter is disabled, otherwise the code will not compile and run

from network import LoRa
import socket
import time
import ubinascii
import pycom

# Initialise LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)

# create an OTAA authentication parameters, change them to the provided credentials
app_eui = ubinascii.unhexlify('70B3D5496612657F')
app_key = ubinascii.unhexlify('263E241ABF2087C603B72741DA312495')
dev_eui = ubinascii.unhexlify('70B3D5499D2EC797')

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

# wait until the module has joined the network 
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

print('Joined')
# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)


s.setblocking(True)
s.setblocking(False)

# get any data received (if any...)
data = s.recv(64)
print(data)