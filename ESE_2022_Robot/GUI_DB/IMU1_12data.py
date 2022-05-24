from bluepy import btle
from bluepy.btle import AssignedNumbers
from logic import Counter
import struct
import binascii
import time

    

class MyDelegate(btle.DefaultDelegate):
    def __init__(self, x_acc, y_acc, z_acc, x_gyro ,y_gyro, z_gyro , x_mag, y_mag ,z_mag ,roll ,pitch ,yaw):
        self.start_t = time.time()
        btle.DefaultDelegate.__init__(self)
        self.handleXAcc = x_acc
        self.handleYAcc = y_acc
        self.handleZAcc = z_acc
        self.handleXGyro = x_gyro
        self.handleYGyro = y_gyro
        self.handleZGyro = z_gyro
        self.handleXMag = x_mag
        self.handleYMag = y_mag
        self.handleZMag = z_mag
        self.handleroll = roll
        self.handlepitch =pitch
        self.handleyaw =yaw
        self.T_before = time.time()
        self.counter = Counter()
        self.count = 0
        self.x_acc,self.y_acc,self.z_acc,self.x_gyro ,self.y_gyro, self.z_gyro ,self.x_mag, self.y_mag, self.z_mag, self.roll, self.pitch, self.yaw= 0,0,0,0,0,0,0,0,0,0,0,0
        # ... more initialise here

    def handleNotification(self, cHandle, data):
        val = binascii.b2a_hex(data)
        val = binascii.unhexlify(val) 
        val = struct.unpack('<i', val)[0]
        
        if(self.handleXAcc == cHandle):
            self.x_acc = val/100.0
        elif(self.handleYAcc == cHandle):
            self.y_acc = val/100.0
        elif(self.handleZAcc == cHandle):    
             self.z_acc = val/100.0
        elif(self.handleXGyro == cHandle):
            self.x_gyro = val/100.0
        elif(self.handleYGyro == cHandle):
            self.y_gyro = val/100.0
        elif(self.handleZGyro == cHandle):    
             self.z_gyro = val/100.0
        elif(self.handleXMag == cHandle):
            self.x_mag = val/100.0
        elif(self.handleYMag == cHandle):
            self.y_mag = val/100.0
        elif(self.handleZMag == cHandle):    
             self.z_mag = val/100.0
        elif(self.handleroll == cHandle):
            self.roll = val/100.0
        elif(self.handlepitch == cHandle):
            self.pitch = val/100.0
        elif(self.handleyaw == cHandle):    
             self.yaw = val/100.0
             
        #print(time.time() - self.T_before)
        #self.T_before = time.time()
        self.count = self.counter.counterAlgorithm(self.z_acc)
        #print(self.x_acc,self.y_acc,self.z_acc,self.x_gyro,self.y_gyro,self.z_gyro, self.x_mag, self.y_mag, self.z_mag, self.roll ,self.pitch , self.yaw )

    def countReturn(self):
        return self.count

def bleCommunication(count):

    print("Connecting...")
    dev = btle.Peripheral("56:ec:8a:8c:21:5d")

    try:
        print("Device services list:")
        for svc in dev.services:
            print (str(svc))


        HRService = dev.getServiceByUUID("6e400001-b5a3-f393-e0a9-e50e24dcca9e")
        print("HRService", HRService)

        print("HRService characteristics list: ")
        for char in HRService.getCharacteristics():
            print("HRService char[", char.getHandle(), "]: ", char)

        x_ACC = HRService.getCharacteristics("6e400002-b5a3-f393-e0a9-e50e24dcca9e")[0] #Notice! Check is characteristic found before usage in production code!
        y_ACC = HRService.getCharacteristics("6e400003-b5a3-f393-e0a9-e50e24dcca9e")[0] #Notice! Check is characteristic found before usage in production code!
        z_ACC = HRService.getCharacteristics("6e400004-b5a3-f393-e0a9-e50e24dcca9e")[0] #Notice! Check is characteristic found before usage in production code!
        x_GYRO = HRService.getCharacteristics("6e400005-b5a3-f393-e0a9-e50e24dcca9e")[0] #Notice! Check is characteristic found before usage in production code!
        y_GYRO = HRService.getCharacteristics("6e400006-b5a3-f393-e0a9-e50e24dcca9e")[0] #Notice! Check is characteristic found before usage in production code!
        z_GYRO = HRService.getCharacteristics("6e400007-b5a3-f393-e0a9-e50e24dcca9e")[0] #Notice! Check is characteristic found before usage in production code!
        x_MAG = HRService.getCharacteristics("6e400008-b5a3-f393-e0a9-e50e24dcca9e")[0] #Notice! Check is characteristic found before usage in production code!
        y_MAG = HRService.getCharacteristics("6e400009-b5a3-f393-e0a9-e50e24dcca9e")[0] #Notice! Check is characteristic found before usage in production code!
        z_MAG = HRService.getCharacteristics("6e400010-b5a3-f393-e0a9-e50e24dcca9e")[0] #Notice! Check is characteristic found before usage in production code!
        Roll = HRService.getCharacteristics("6e400011-b5a3-f393-e0a9-e50e24dcca9e")[0] #Notice! Check is characteristic found before usage in production code!
        Pitch = HRService.getCharacteristics("6e400012-b5a3-f393-e0a9-e50e24dcca9e")[0] #Notice! Check is characteristic found before usage in production code!
        Yaw = HRService.getCharacteristics("6e400013-b5a3-f393-e0a9-e50e24dcca9e")[0] #Notice! Check is characteristic found before usage in production code!

        print(x_ACC.getHandle())
        # Assign delegate to target characteristic
        object = MyDelegate(x_ACC.getHandle() , y_ACC.getHandle(), z_ACC.getHandle(),x_GYRO.getHandle(),y_GYRO.getHandle(),z_GYRO.getHandle(),x_MAG.getHandle(),y_MAG.getHandle(),z_MAG.getHandle(),Roll.getHandle(),Pitch.getHandle(),Yaw.getHandle() )
        dev.setDelegate(object)
        # dev.setDelegate(MyDelegate(y_ACC.getHandle()))
        # dev.setDelegate(MyDelegate(z_ACC.getHandle()))
        
        # We need to write into org.bluetooth.descriptor.gatt.client_characteristic_configuration descriptor to enabe notifications
        # to do so, we must get this descriptor from characteristic first
        # more details you can find in bluepy source (def getDescriptors(self, forUUID=None, hndEnd=0xFFFF))
        desc_x_acc = x_ACC.getDescriptors(AssignedNumbers.client_characteristic_configuration)
        desc_y_acc = y_ACC.getDescriptors(AssignedNumbers.client_characteristic_configuration)
        desc_z_acc = z_ACC.getDescriptors(AssignedNumbers.client_characteristic_configuration)
        desc_x_gyro = x_GYRO.getDescriptors(AssignedNumbers.client_characteristic_configuration)
        desc_y_gyro = y_GYRO.getDescriptors(AssignedNumbers.client_characteristic_configuration)
        desc_z_gyro = z_GYRO.getDescriptors(AssignedNumbers.client_characteristic_configuration)
        desc_x_mag = x_MAG.getDescriptors(AssignedNumbers.client_characteristic_configuration)
        desc_y_mag = y_MAG.getDescriptors(AssignedNumbers.client_characteristic_configuration)
        desc_z_mag = z_MAG.getDescriptors(AssignedNumbers.client_characteristic_configuration)
        desc_roll = Roll.getDescriptors(AssignedNumbers.client_characteristic_configuration)
        desc_pitch = Pitch.getDescriptors(AssignedNumbers.client_characteristic_configuration)
        desc_yaw = Yaw.getDescriptors(AssignedNumbers.client_characteristic_configuration)

        # print("Writing \"notification\" flag to descriptor with handle: ", desc[0].handle)
        dev.writeCharacteristic(desc_x_acc[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_y_acc[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_z_acc[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_x_gyro[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_y_gyro[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_z_gyro[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_x_mag[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_y_mag[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_z_mag[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_roll[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_pitch[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_yaw[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!

        print("Waiting for notifications...")

        while True:
            if dev.waitForNotifications(1):
                count = object.countReturn()
                # handleNotification() was called
                continue

    finally:
        dev.disconnect()