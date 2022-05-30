#-*-coding:utf-8-*-
import sys
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from bluepy import btle
from bluepy.btle import AssignedNumbers
from IMU1_12data import MyDelegate 
import database
from time import time, sleep
from playsound import playsound
reload(sys)
sys.setdefaultencoding('utf-8')

form_class = uic.loadUiType("userui.ui")[0]

a=1
counttry =0 
 



class UI(QtGui.QMainWindow, form_class):
    
    def __init__(self, parent=None):
        #super().__init__()
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        timer = QTimer(self)
        timer.timeout.connect(self.nowtime)
        timer.start(1000)

        self.button()
        self.nowtime()
        self.th = Thread1()
        self.th2 = Thread2()
        self.th3 = Thread3()
        self.th3.start()
        self.th3.count.connect(self.getval)
        self.th3.connecton.connect(self.nowconnect)
        global nowroutine 
        nowroutine= self.nowroutine_2
    
    #button actions    
    def button(self):
        self.start_1.clicked.connect(self.goto6)
        self.finsave_6.clicked.connect(self.goto2)
        self.seerecord_1.clicked.connect(self.goto3)
        self.calibration_1.clicked.connect(self.goto4)

        self.gotohome_2.clicked.connect(self.gotohome)
        self.gotohome_3.clicked.connect(self.gotohome)
        self.gotohome_4.clicked.connect(self.gotohome)
        self.goto3_5.clicked.connect(self.goto3)
        self.startfinish_2.clicked.connect(self.workoutestimate)
        
        self.giverecord_3.clicked.connect(self.giverecord)
        self.givefeedback_3.clicked.connect(self.givefeedback)
        self.info_3.clicked.connect(self.giveinfo)
        self.pushButton.clicked.connect(self.liveupdate)
        
        self.addroutine_6.clicked.connect(self.addroutine)
        self.deleteroutine_6.clicked.connect(self.deleteroutine)
        self.nowroutine_6.activated[str].connect(self.changeroutinepage)
        self.saveroutinedb_6.clicked.connect(self.saveroutine)
        

        
        
    #silsigan pose-check
    def goto2(self):
        self.stackedWidget.setCurrentWidget(self.page_2)
        self.nowroutine_2.setText(self.nowroutine_6.currentText()) 
        
    # record
    def goto3(self):
        mydb = database.db()
        
        current_day = QDate.currentDate()
        self.stackedWidget.setCurrentWidget(self.page_3)
        for i in range(1,8,1):
            nowday = "day"+str(i)+"_3"
            getattr(self, nowday).setText(current_day.addDays(i-7).toString('MM.dd'))

        for i in range(7):
            nowday = current_day.addDays(-i).toString('yyyy-MM-dd')
            row = mydb.returnDayworkoutRows(nowday)
            count = len(row)

            for x in range(count):
                name, time = row[x] 
                workrecord = "day"+str(7-i)+str(x+1)+"_3"
                getattr(self, workrecord).setText(name+time)
  
    #calibration
    def goto4(self):
        self.stackedWidget.setCurrentWidget(self.page_4) 
        
    def goto6(self):
        # self.th3.start()
        # self.th3.count.connect(self.getval)
        mydb = database.db()

        self.stackedWidget.setCurrentWidget(self.page_6)
        mydb.createWorkoutData()

        row = mydb.returnRoutineRows(1)
        currentroutine = "routine_1"
        for j in range(len(row)):
            getattr(self, currentroutine).setItem(j, 0, QTableWidgetItem(row[j][0]))
            getattr(self, currentroutine).setItem(j, 1, QTableWidgetItem(str(row[j][1])))
            getattr(self, currentroutine).setItem(j, 2, QTableWidgetItem(str(row[j][2])))
            getattr(self, currentroutine).setItem(j, 3, QTableWidgetItem(str(row[j][3])))

    # three button
    def gotohome(self):
        self.stackedWidget.setCurrentWidget(self.page)
        
    def nowtime(self):
        current_day = QDate.currentDate()
        current_time = QTime.currentTime()
        day = current_day.toString('yyyy.MM.dd')
        time = current_time.toString('hh:mm:ss')
        
        self.time_1.setText(day +" " +time) 
        self.time_2.setText(day +" "+ time) 
        self.time_3.setText(day +" " +time) 
        self.time_4.setText(day +" "+ time) 
        self.time_5.setText(day +" "+ time) 
        self.time_6.setText(day +" "+ time) 
        
    # undong tonggue
    def giverecord(self):
        self.stackedWidget.setCurrentWidget(self.page_5) 
        print(" giverecord.")
        
    # feedback
    def givefeedback(self):     
        print("feedback.")       
    
    # workout info
    def giveinfo(self):
        print("giveinfo")
        

    def changeroutinepage(self):
        mydb = database.db()
        for i in range(1,7,1):
            if self.nowroutine_6.currentText() == "routine " +str(i) :
                currentroutinepage = "routinepage_"+str(i)
                currentroutine = "routine_"+str(i)  
                self.stackedWidget_2.setCurrentWidget(getattr(self, currentroutinepage))
                row = mydb.returnRoutineRows(i)
                for j in range(len(row)):
                    getattr(self, currentroutine).setItem(j, 0, QTableWidgetItem(row[j][0]))
                    getattr(self, currentroutine).setItem(j, 1, QTableWidgetItem(str(row[j][1])))
                    getattr(self, currentroutine).setItem(j, 2, QTableWidgetItem(str(row[j][2])))
                    getattr(self, currentroutine).setItem(j, 3, QTableWidgetItem(str(row[j][3]))) 

    def addroutine(self):
        for i in range(1,7,1):
            if self.nowroutine_6.currentText() == "routine " +str(i) :
                currentroutine = "routine_"+str(i)
                for j in range(5):
                    if getattr(self, currentroutine).item(j,0) == None:
                        break
        getattr(self, currentroutine).setItem(j, 0, QTableWidgetItem(self.cb1_6.currentText()))
        getattr(self, currentroutine).setItem(j, 1, QTableWidgetItem(self.cb2_6.currentText()))
        getattr(self, currentroutine).setItem(j, 2, QTableWidgetItem(self.cb3_6.currentText()))
        getattr(self, currentroutine).setItem(j, 3, QTableWidgetItem(self.cb4_6.currentText()))        
        
    def deleteroutine(self):
        for i in range(1,7,1):
            if self.nowroutine_6.currentText() == "routine "+str(i):
                currentroutine = "routine_"+str(i)
                for j in range(4,-1,-1):
                    if getattr(self, currentroutine).item(j,0) != None:
                        break
        getattr(self, currentroutine).setItem(j, 0, None)
        getattr(self, currentroutine).setItem(j, 1, None)
        getattr(self, currentroutine).setItem(j, 2, None)
        getattr(self, currentroutine).setItem(j, 3, None)
         
    
    def liveupdate(self):
        self.th.start()
        self.th.change_value2.connect(self.label_83.setText)
        self.th.change_value1.connect(self.label_87.setText)

    def saveroutine(self):
        mydb = database.db()
        row = []
        for i in range(1,7,1):
            if self.nowroutine_6.currentText() == "routine "+str(i):
                currentroutine = "routine_"+str(i)
        for i in range(5):
            if getattr(self, currentroutine).item(i,0) == None:
                break 
            row.append([])
            row[i].append(currentroutine)
            row[i].append(getattr(self, currentroutine).item(i, 0).text())
            row[i].append(getattr(self, currentroutine).item(i, 1).text())
            row[i].append(getattr(self, currentroutine).item(i, 2).text())
            row[i].append(getattr(self, currentroutine).item(i, 3).text())

        for i in range(1,7,1):
            if row[0][0] == "routine_"+str(i):
                mydb.deleteRoutine(i)

        mydb.GuiInsertWorkout(row)

    def workoutestimate(self):
        global a
        a = a+1
        if a%2 == 0:
            self.th2.start() 
        self.th2.exername.connect(self.label_7.setText)
        self.th2.exerset.connect(self.leftset_2.setText)
        self.th2.exercount.connect(self.lefttry_2.setText)
        self.th2.resttime.connect(self.resttime_2.setText)

    def getval(self):
        global counttry
        counttry = counttry + 1 
    
    def nowconnect(self):
        QMessageBox.about(self,'Ble Notice','Success Connect ')
        playsound('./sound/eng.wav')
        
        
class Thread1(QThread): 
    
    change_value1 = pyqtSignal(str)
    change_value2 = pyqtSignal(str)
   
    def __init__(self): 
        QThread.__init__(self) 
        #self.cond = QWaitCondition()
        #self.mutex = QMutex()
        
        
    def run(self): 
        self.change_value2.emit("1start.") 
        for i in range(20): 
            self.change_value1.emit(str(i)) 
            sleep(2) 
        self.change_value2.emit("arrive.")

class Thread2(QThread):
    
    exername = pyqtSignal(str)
    exerset = pyqtSignal(str)
    exercount = pyqtSignal(str)
    resttime = pyqtSignal(str)
    def __init__(self): 
       QThread.__init__(self)       

    def run(self):
        global a
        global counttry
        global nowroutine
        goal = 0
        goal2 = 0
        totaltry = 0
        record = []
        print(nowroutine)
        mydb = database.db()
        for i in range(1,7,1):
            if nowroutine.text() == "routine " +str(i) :
                row = mydb.returnRoutineRows(i)
                for j in range(len(row)):
                    starttime = time()
                    name, goalset, count, rest = row[j]
                    print(name, goalset, count, rest)
                    print("start")
                    self.exername.emit(name)
                    for k in range(goalset):
                        self.exerset.emit(str(goalset))
                        self.resttime.emit(str(rest))
                        goal = count
                        goal2 = count
                        counttry = 0
                        while True:
                            self.exercount.emit(str(goal2))
                            goal2 = goal - counttry
                            if goal2 == 0:
                                self.exercount.emit(str(goal2))
                                print("finish 1set")
                                #saverecord
                                #row.append([])
                                totaltry = totaltry + counttry
                                break
                            elif a%2 == 1:
                                print("stop")
                                #saverecord
                                totaltry = totaltry + counttry
                                break

                        goalset = goalset-1
                        if k < range(goalset):
                            for l in range(rest):
                                self.resttime.emit(str(rest-l))
                                if a%2 == 1:
                                    print("stop")
                                    break
                                sleep(1)

                        if a%2 ==1:
                            self.exercount.emit("")
                            self.resttime.emit("")
                            self.exerset.emit("")
                            self.exername.emit("")
                            break
                    #saverecord
                    endtime = time()
                    print('time elapsed:', int(endtime - starttime))
                    record.append([])
                    record[j].append(name)
                    record[j].append(int(endtime - starttime))
                    record[j].append(totaltry)
                    print(record[j])
                    totaltry = 0
                # save workout data to DB
                mydb.saveDayworkoutData(record)
        a=a+1


        
    
    def stop(self):
        self.quit()
        self.wait(5000) #5000ms = 5s

class Thread3(QThread): 
    
    count = pyqtSignal()
    connecton = pyqtSignal()

    def __init__(self): 
        QThread.__init__(self) 
        #self.cond = QWaitCondition()
        #self.mutex = QMutex()
        
        
    def run(self): 

        print("Connecting...")
        dev = btle.Peripheral("56:ec:8a:8c:21:5d")

    
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
        object1 = MyDelegate(x_ACC.getHandle() , y_ACC.getHandle(), z_ACC.getHandle(),x_GYRO.getHandle(),y_GYRO.getHandle(),z_GYRO.getHandle(),x_MAG.getHandle(),y_MAG.getHandle(),z_MAG.getHandle(),Roll.getHandle(),Pitch.getHandle(),Yaw.getHandle() )
        dev.setDelegate(object1)
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
        before_val = 0
        self.connecton.emit()
        while True:
            if dev.waitForNotifications(0.5):
                #print(object1.countReturn())
                if (before_val != object1.countReturn()):
                    self.count.emit()
                    print("change signal\n\n\n")
                before_val =object1.countReturn()
                # handleNotification() was called
                continue
        

if __name__ == '__main__':        
    app = QtGui.QApplication(sys.argv)
    mainWindow = UI()
    mainWindow.show()
    sys.exit(app.exec_())
