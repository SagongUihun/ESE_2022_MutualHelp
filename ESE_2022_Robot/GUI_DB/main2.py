#-*-coding:utf-8-*-
import sys
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from bluepy import btle
from bluepy.btle import AssignedNumbers
from IMU1_multi_data import MyDelegate 
import database
from time import time, sleep
from playsound import playsound

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas 
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

reload(sys)
sys.setdefaultencoding('utf-8')

form_class = uic.loadUiType("userui.ui")[0]

a=1
counttry1 = 0
counttry2 = 0
counttry3 = 0 
hand_r = 0
hand_p = 0
hand_y = 0

nowrunname = ""
nowpage = ""

figure = None



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
        #self.th4 = Thread4()
        self.th.start()
        self.th3.start()
        self.th3.count1.connect(self.getval1)
        self.th3.count2.connect(self.getval2)
        self.th3.count3.connect(self.getval3)
        self.th3.connecton.connect(self.nowconnect)
        self.th.pose.connect(self.drawgraph)
        global nowroutine 
        nowroutine= self.nowroutine_2
        
        self.fig = plt.Figure()
        # global figure
        # figure = self.fig
        self.canvas = FigureCanvas(self.fig)
        self.forgraph.addWidget(self.canvas)
        self.triger = True

        #self.th4.start()

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
        self.selectworkout.activated[str].connect(self.updaterecord)
        self.saveroutinedb_6.clicked.connect(self.saveroutine)
        

        
        
    #silsigan pose-check
    def goto2(self):
        global nowpage
        nowpage = "self.page_2"
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
            row = mydb.returnDayworkoutRows()
            count = len(row)
            j = 0
            for x in range(count):
                day, name, time = row[x]
                if day == nowday:
                    workrecord = "day"+str(7-i)+str(j+1)+"_3"
                    j = j + 1
                    getattr(self, workrecord).setText(name+" "+str(int(time))+"회")
  
    #calibration
    def goto4(self):
        self.stackedWidget.setCurrentWidget(self.page_4)
        # self.fig = plt.Figure()
        # self.canvas = FigureCanvas(self.fig)

        # self.forgraph.addWidget(self.canvas)
        # u = np.array([-8, -8, 0])   # vector u
        # v = np.array([5, 6, 2])

        # ax = self.fig.add_subplot(111, projection='3d')

        # start = [0,0,0]
        # ax.quiver(start[0],start[1],start[2],u[0],u[1],u[2],color='red')
        # ax.quiver(start[0],start[1],start[2],v[0],v[1],v[2])
        # ax.quiver(v[0],v[1],v[2],u[0],u[1],u[2],color="green")
        # ax.set_xlim([-8,8])
        # ax.set_ylim([-8,8])
        # ax.set_zlim([-8,8])
        # self.canvas.draw()


        
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

    def updaterecord(self):
        mydb = database.db()
        row = mydb.returnNameWorkoutRows()
        for x in range(len(row)):
            if row[x][0] == self.selectworkout.currentText():
                for i in range(12):
                    target = "detail_"+str(i+1)
                    getattr(self, target).setText(str(row[x][i+1])) 
        
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

    def getval1(self):
        global counttry1
        counttry1 = counttry1 + 1 
    
    def getval2(self):
        global counttry2
        counttry2 = counttry2 + 1 

    def getval3(self):
        global counttry3
        counttry3 = counttry3 + 1 
    
    def nowconnect(self):
        QMessageBox.about(self,'Ble Notice','Success Connect ')
        playsound('./sound/eng.wav')
    
    def drawgraph(self):
        global hand_r
        global hand_p
        global hand_y
        #print(hand_r, hand_p, hand_y)
        hr = np.deg2rad(hand_r)
        hp = np.deg2rad(hand_p)
        hy = np.deg2rad(hand_y)
        if self.stackedWidget.currentWidget() == self.page_2:
            x = np.array([np.cos(hp),0 ,-np.sin(hp)])
            y = np.array([np.sin(hp)*np.sin(hr),np.cos(hr),np.cos(hp)*np.sin(hr)])
            z = np.array([np.sin(hp)*np.cos(hr),-np.sin(hr),np.cos(hp)*np.cos(hr)])
            
            # x = np.array([np.cos(hp),np.sin(hp) ,0])
            # y = np.array([-np.sin(hp)*np.cos(hr), np.cos(hp)*np.cos(hr), np.sin(hr)])
            # z = np.array([np.sin(hp)*np.sin(hr), -np.cos(hp)*np.sin(hr), np.cos(hr)])
            
            
            v = np.array([5, 6, 2])
            
           
            if(self.triger):
                self.ax = self.fig.add_subplot(111, projection='3d')
                self.triger = False
            #print( hand_p, hand_r, hand_y, hr, hp)
            start = [0,0,0]
            
            self.ax.quiver(start[0],start[1],start[2],x[0],x[1],x[2],color='red')
            self.ax.quiver(start[0],start[1],start[2],y[0],y[1],y[2],color='orange')
            self.ax.quiver(start[0],start[1],start[2],z[0],z[1],z[2],color='yellow')
            self.ax.quiver(start[0],start[1],-1,0,0,1,color = 'black')
            
            self.ax.set_xlim([-1,1])
            self.ax.set_ylim([-1,1])
            self.ax.set_zlim([-1,1])
            self.canvas.draw()
            self.ax.axes.clear()
            print("update")



        
        
class Thread1(QThread): 
    
    pose = pyqtSignal()
    def __init__(self): 
        QThread.__init__(self) 
        #self.cond = QWaitCondition()
        #self.mutex = QMutex()
        
        
    def run(self): 
        while True: 
            self.pose.emit()
            sleep(0.4) 
        

class Thread2(QThread):
    
    exername = pyqtSignal(str)
    exerset = pyqtSignal(str)
    exercount = pyqtSignal(str)
    resttime = pyqtSignal(str)
    def __init__(self): 
       QThread.__init__(self)       

    def run(self):
        global a
        global counttry1
        global counttry2
        global counttry3

        global nowroutine
        global nowrunname
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
                    print(name)
                    nowrunname = name
                    for k in range(goalset):
                        self.exerset.emit(str(goalset))
                        self.resttime.emit(str(rest))
                        goal = count
                        goal2 = count
                        counttry1 = 0
                        counttry2 = 0
                        counttry3 = 0
                        if (name =="바벨 컬"):
                            while True:
                                #print(counttry1,counttry2,counttry3)
                                self.exercount.emit(str(goal2))
                                goal2 = goal - counttry1
                                if goal2 == 0:
                                    self.exercount.emit(str(goal2))
                                    print("finish 1set")
                                    totaltry = totaltry + counttry1
                                    break
                                elif a%2 == 1:
                                    print("stop")
                                    #saverecord
                                    totaltry = totaltry + counttry1
                                    break
                                sleep(0.01)
                    
                        if (name =="벤치프레스"):
                            while True:
                                print("벤치프레스")
                                self.exercount.emit(str(goal2))
                                goal2 = goal - counttry2
                                if goal2 == 0:
                                    self.exercount.emit(str(goal2))
                                    print("finish 1set")
                                    #saverecord
                                    #row.append([])
                                    totaltry = totaltry + counttry2
                                    break
                                elif a%2 == 1:
                                    print("stop")
                                    #saverecord
                                    totaltry = totaltry + counttry2
                                    break

                        if (name =="숄더프레스"):
                            while True:
                                self.exercount.emit(str(goal2))
                                goal2 = goal - counttry3
                                if goal2 == 0:
                                    self.exercount.emit(str(goal2))
                                    print("finish 1set")
                                    #saverecord
                                    #row.append([])
                                    totaltry = totaltry + counttry3
                                    break
                                elif a%2 == 1:
                                    print("stop")
                                    #saverecord
                                    totaltry = totaltry + counttry3
                                    break

                        goalset = goalset-1
                        self.exerset.emit(str(goalset))
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
                    nowrunname = ""
                    if j == len(row)-1:
                        a=a+1
                    if a%2 ==1:
                            self.exercount.emit("")
                            self.resttime.emit("")
                            self.exerset.emit("")
                            self.exername.emit("")
                            break
                # save workout data to DB
                mydb.saveDayworkoutData(record)
        a=a+1


        
    
    def stop(self):
        self.quit()
        self.wait(5000) #5000ms = 5s

class Thread3(QThread): 

   
    
    count1 = pyqtSignal()
    count2 = pyqtSignal()
    count3 = pyqtSignal()
    connecton = pyqtSignal()

    def __init__(self): 
        QThread.__init__(self) 
        #self.cond = QWaitCondition()
        #self.mutex = QMutex()
        
        
    def run(self): 
        global hand_r
        global hand_p
        global hand_y
        global nowrunname
        print("Connecting...")
        #56:ec:8a:8c:21:5d
        dev = btle.Peripheral("df:e6:f4:32:69:6d")

 
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
        object1 = MyDelegate(IMU1ACC.getHandle() , IMU1Gyro.getHandle(),IMU1Pose.getHandle(),IMU2ACC.getHandle(),IMU2Gyro.getHandle(),IMU2Pose.getHandle(),0 )
        dev.setDelegate(object1)
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
        before_val1 = 0
        before_val2 = 0
        before_val3 = 0
        beforepose = []
        self.connecton.emit()
        while True:
            if dev.waitForNotifications(1):
                #print(object1.countReturn())
                if nowrunname == "바벨 컬":
                    if (before_val1 != object1.count1Return()):
                        self.count1.emit()
                        print("change signal\n\n\n")
                        before_val1 =object1.count1Return()

                if nowrunname == "벤치프레스":    
                    if (before_val2 != object1.count2Return()):
                        self.count2.emit()
                        print("change signal\n\n\n")
                        before_val2 =object1.count2Return()

                if nowrunname == "숄더프레스":
                    if (before_val3 != object1.count3Return()):
                        self.count3.emit()
                        print("change signal\n\n\n")
                        before_val3 =object1.count3Return()    
               
                # before_val1 =object1.count1Return()
                # before_val2 =object1.count2Return()
                # before_val3 =object1.count3Return()
                # handleNotification() was called
                temp =  object1.relativePose()
                # temp =  object1.ArduinoPose()
                hand_r = temp[0]
                hand_p = temp[1]
                hand_y = temp[2]
                continue
        
# class Thread4(QThread): 
    
#     global hand_r
#     global hand_p
#     global hand_y
#     global nowpage
#     global figure

#     def __init__(self): 
#         QThread.__init__(self) 
#         #self.cond = QWaitCondition()
#         #self.mutex = QMutex()
        
#     def run(self): 
        
#         #print(hand_r, hand_p, hand_y)
#         while True:
#             hr = np.deg2rad(hand_r)
#             hp = np.deg2rad(hand_p)
#             hy = np.deg2rad(hand_y)
#             if nowpage == "self.page_2":
#                 x = np.array([np.cos(hp),0 ,-np.sin(hp)])
#                 y = np.array([np.sin(hp)*np.sin(hr),np.cos(hr),np.cos(hp)*np.sin(hr)])
#                 z = np.array([np.sin(hp)*np.cos(hr),-np.sin(hr),np.cos(hp)*np.cos(hr)])
                
#                 # x = np.array([np.cos(hp),np.sin(hp) ,0])
#                 # y = np.array([-np.sin(hp)*np.cos(hr), np.cos(hp)*np.cos(hr), np.sin(hr)])
#                 # z = np.array([np.sin(hp)*np.sin(hr), -np.cos(hp)*np.sin(hr), np.cos(hr)])
                
                
#                 v = np.array([5, 6, 2])
                
            
#                 if(self.triger):
#                     self.ax = figure.add_subplot(111, projection='3d')
#                     self.triger = False
#                 #print( hand_p, hand_r, hand_y, hr, hp)
#                 start = [0,0,0]
                
#                 self.ax.quiver(start[0],start[1],start[2],x[0],x[1],x[2],color='red')
#                 self.ax.quiver(start[0],start[1],start[2],y[0],y[1],y[2],color='orange')
#                 self.ax.quiver(start[0],start[1],start[2],z[0],z[1],z[2],color='yellow')
#                 self.ax.quiver(start[0],start[1],-1,0,0,1,color = 'black')
                
#                 self.ax.set_xlim([-1,1])
#                 self.ax.set_ylim([-1,1])
#                 self.ax.set_zlim([-1,1])
#                 self.canvas.draw()
#                 self.ax.axes.clear()
#                 print("update") 
#                 sleep(0.4)

if __name__ == '__main__':        
    app = QtGui.QApplication(sys.argv)
    mainWindow = UI()
    mainWindow.show()
    #mainWindow.showFullScreen()
    sys.exit(app.exec_())

