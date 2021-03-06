from bluepy import btle
from bluepy.btle import AssignedNumbers
#from logic import Counter
from logicTest import Counter
import struct
import binascii
import time

    

class MyDelegate(btle.DefaultDelegate):
    def __init__(self, IMU1ACC,IMU1GYRO,IMU1POSE,IMU2ACC,IMU2GYRO,IMU2POSE, FSR):
        self.start_t = time.time()
        btle.DefaultDelegate.__init__(self)
        
        self.IMU1acc = IMU1ACC
        self.IMU1gyro = IMU1GYRO
        self.IMU1pose = IMU1POSE
        self.IMU2acc = IMU2ACC
        self.IMU2gyro = IMU2GYRO
        self.IMU2pose = IMU2POSE

        self.FSR = FSR

        self.T_before = time.time()
        self.counter = Counter()
        self.shoulderCount = 0
        self.dumbelCount = 0
        self.x_acc1,self.y_acc1,self.z_acc1,self.x_gyro1 ,self.y_gyro1, self.z_gyro1 , self.roll1, self.pitch1, self.yaw1= 0,0,0,0,0,0,0,0,0
        self.x_acc2,self.y_acc2,self.z_acc2,self.x_gyro2 ,self.y_gyro2, self.z_gyro2 , self.roll2, self.pitch2, self.yaw2= 0,0,0,0,0,0,0,0,0
        self.FSR_data = 0
        getcount1 = 0
        getcount2 = 0
        getcount3 = 0
        # ... more initialise here

    def handleNotification(self, cHandle, data):
        # val = binascii.b2a_hex(data)
        # val = binascii.unhexlify(val) 
        # val = struct.unpack('<s', val)
        # print(len(data))
        val  = str(data)

        if(self.IMU1acc == cHandle):
            val = val.split()
            self.x_acc1 = float(val[0])
            self.y_acc1 = float(val[1])
            self.z_acc1 = float(val[2])
            
        elif(self.IMU1gyro == cHandle):
            val = val.split()
            self.x_gyro1 = float(val[0])
            self.y_gyro1 = float(val[1])
            self.z_gyro1 = float(val[2])

        elif(self.IMU1pose == cHandle):
            val = val.split()
            self.roll1 = float(val[0])
            self.pitch1 = float(val[1])
            self.yaw1 = float(val[2])
        
        elif(self.IMU2acc == cHandle):
            val = val.split()
            self.x_acc2 = float(val[0])
            self.y_acc2 = float(val[1])
            self.z_acc2 = float(val[2])
            
        elif(self.IMU2gyro == cHandle):
            val = val.split()
            self.x_gyro2 = float(val[0])
            self.y_gyro2 = float(val[1])
            self.z_gyro2 = float(val[2])

        elif(self.IMU2pose == cHandle):
            val = val.split()
            self.roll2 = float(val[0])
            self.pitch2 = float(val[1])
            self.yaw2 = float(val[2])

        elif(self.FSR == cHandle):    
             self.FSR_data = float(val)
        
            
        # print(time.time() - self.T_before)
        # self.T_before = time.time()
        # self.shoulderCount = self.counter.shoulderPress(self.z_acc1)
        # self.KcCount = self.counter.KcCurl(self.x_gyro1)
        # self.dumbelCount = self.counter.dumbelCurl(self.roll1)
        # print("IMU1",self.x_acc1,self.y_acc1,self.z_acc1,self.x_gyro1 ,self.y_gyro1, self.z_gyro1 , self.roll1, self.pitch1, self.yaw1)
        #print("IMU2",self.x_acc2,self.y_acc2,self.z_acc2,self.x_gyro2 ,self.y_gyro2, self.z_gyro2 , self.roll2, self.pitch2, self.yaw2)
        # print(self.roll1 , self.pitch1, self.yaw1 ,self.roll2, self.pitch2, self.yaw2)

    def count1Return(self):
        return self.KcCount

    def count2Return(self):
        return self.dumbelCount

    def count3Return(self):
        return self.shoulderCount
    
    def absolute_data(self):
        return [[self.x_acc1,self.y_acc1,self.z_acc1,self.x_gyro1 ,self.y_gyro1, self.z_gyro1 , self.roll1, self.pitch1, self.yaw1],[self.x_acc2,self.y_acc2,self.z_acc2,self.x_gyro2 ,self.y_gyro2, self.z_gyro2 , self.roll2, self.pitch2, self.yaw2],[self.FSR_data]]    # def count4Return(self):
    #     # if (health == 'dumbel'):
    #     return self.KcCount        

    def relativePose(self):
        return [round((self.roll1 - self.roll2),2),round((self.pitch1 - self.pitch2),2),round((self.yaw1 - self.yaw2),2)]

    def ArduinoPose(self):
        return [round((self.roll1),2),round((self.pitch1),2),round((self.yaw1),2)]



 

def bleCommunication():

    print("Connecting...")
    #56:ec:8a:8c:21:5d
    dev = btle.Peripheral("df:e6:f4:32:69:6d")

    try:
        print("Device services list:")
        for svc in dev.services:
            print (str(svc))


        HRService = dev.getServiceByUUID("6e400001-b5a3-f393-e0a9-e50e24dcca9e")
        print("HRService", HRService)

        print("HRService characteristics list: ")
        for char in HRService.getCharacteristics():
            print("HRService char[", char.getHandle(), "]: ", char)

        IMU1ACC = HRService.getCharacteristics("6e400002-b5a3-f393-e0a9-e50e24dcca9e")[0] #Notice! Check is characteristic found before usage in production code!
        IMU1Gyro = HRService.getCharacteristics("6e400003-b5a3-f393-e0a9-e50e24dcca9e")[0] #Notice! Check is characteristic found before usage in production code!
        IMU1Pose = HRService.getCharacteristics("6e400004-b5a3-f393-e0a9-e50e24dcca9e")[0] #Notice! Check is characteristic found before usage in production code!

        IMU2ACC = HRService.getCharacteristics("6e400005-b5a3-f393-e0a9-e50e24dcca9e")[0] #Notice! Check is characteristic found before usage in production code!
        IMU2Gyro = HRService.getCharacteristics("6e400006-b5a3-f393-e0a9-e50e24dcca9e")[0] #Notice! Check is characteristic found before usage in production code!
        IMU2Pose = HRService.getCharacteristics("6e400007-b5a3-f393-e0a9-e50e24dcca9e")[0] #Notice! Check is characteristic found before usage in production code!

        #FSR = HRService.getCharacteristics("6e400008-b5a3-f393-e0a9-e50e24dcca9e")[0] #Notice! Check is characteristic found before usage in production code!

        # Assign delegate to target characteristic
        object = MyDelegate(IMU1ACC.getHandle() , IMU1Gyro.getHandle(),IMU1Pose.getHandle(),IMU2ACC.getHandle(),IMU2Gyro.getHandle(),IMU2Pose.getHandle(),0 )
        dev.setDelegate(object)
        # dev.setDelegate(MyDelegate(y_ACC.getHandle()))
        # dev.setDelegate(MyDelegate(z_ACC.getHandle()))
        
        # We need to write into org.bluetooth.descriptor.gatt.client_characteristic_configuration descriptor to enabe notifications
        # to do so, we must get this descriptor from characteristic first
        # more details you can find in bluepy source (def getDescriptors(self, forUUID=None, hndEnd=0xFFFF))
        desc_IMU1ACC = IMU1ACC.getDescriptors(AssignedNumbers.client_characteristic_configuration)
        desc_IMU1Gyro = IMU1Gyro.getDescriptors(AssignedNumbers.client_characteristic_configuration)
        desc_IMU1Pose = IMU1Pose.getDescriptors(AssignedNumbers.client_characteristic_configuration)

        desc_IMU2ACC = IMU2ACC.getDescriptors(AssignedNumbers.client_characteristic_configuration)
        desc_IMU2Gyro = IMU2Gyro.getDescriptors(AssignedNumbers.client_characteristic_configuration)
        desc_IMU2Pose = IMU2Pose.getDescriptors(AssignedNumbers.client_characteristic_configuration)

        
        #desc_z_acc = z_ACC.getDescriptors(AssignedNumbers.client_characteristic_configuration)
       
        # print("Writing \"notification\" flag to descriptor with handle: ", desc[0].handle)
        dev.writeCharacteristic(desc_IMU1ACC[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_IMU1Gyro[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_IMU1Pose[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!

        dev.writeCharacteristic(desc_IMU2ACC[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_IMU2Gyro[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_IMU2Pose[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!


        #dev.writeCharacteristic(desc_z_acc[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
       
        print("Waiting for notifications...")

        while True:
            if dev.waitForNotifications(1):
                count = object.countReturn()
                # handleNotification() was called
                continue

    finally:
        dev.disconnect()



if __name__ == "__main__":
    bleCommunication()