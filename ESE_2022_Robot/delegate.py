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