"""
Python/Raspberry Pi BluetoothLE exercise:
using bluepy library

Work with Arduino Nano RP2040 Connect example:
ArduinoBLE > Peripheral > CallbackLED

Connect to Peripheral with matched MAC.
Check for service uuid and characteristic uuid,
if matched found: send bytes 0x01 and 0x00 for three time
to turn Nano RP2040 Connect onboard LED ON/OFF.
"""

from bluepy import btle
import time

#Have to match with Peripheral
MAC = "df:e6:f4:32:69:6d"
SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
CHARACTERISTIC_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"

nanoRP2040_Char = None

print("Hello")

print("Connect to:" + MAC)
dev = btle.Peripheral(MAC)
print("\n--- dev ----------------------------")
print(type(dev))
print(dev)

print("\n--- dev.services -------------------")
for svc in dev.services:
    print(str(svc))
    
print("\n------------------------------------")
print("Get Serice By UUID: " + SERVICE_UUID)
service_uuid = btle.UUID(SERVICE_UUID)
service = dev.getServiceByUUID(service_uuid)

print(service)
print("\n--- service.getCharacteristics() ---")
print(type(service.getCharacteristics()))
print(service.getCharacteristics())

#----------------------------------------------
characteristics = dev.getCharacteristics()
print("\n--- dev.getCharacteristics() -------")
print(type(characteristics))
print(characteristics)
    
for char in characteristics:
    print("----------")
    print(type(char))
    print(char)
    print(char.uuid)
    if(char.uuid == CHARACTERISTIC_UUID ):
        print("=== !CHARACTERISTIC_UUID matched! ==")
        nanoRP2040_Char = char
        print(char)
        print(dir(char))
        #print(char.getDescriptors)
        #print(char.propNames)
        #print(char.properties)
        #print(type(char.read()))
        print(char.read())
        
bytes_ON = b'\x01'
bytes_OFF = b'\x00'

if nanoRP2040_Char != None:
    print("\nnanoRP2040_Char found")
    print(nanoRP2040_Char)
    while True:
        print(nanoRP2040_Char.read())
        time.sleep(0.1)

else:
    print("\nnanoRP2040_Char NOT found!")
#=============================================
dev.disconnect()
print("\n--- bye ---\n")