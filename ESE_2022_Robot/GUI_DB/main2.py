#-*-coding:utf-8-*-
import sys
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from bluepy import btle
from bluepy.btle import AssignedNumbers
from IMU1_multi_data import MyDelegate 
from logicTest import Counter
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
L_hand_rpy = [0,0,0]
R_hand_rpy = [0,0,0]
L_data = [] #[[imu1][imu2][fsr]]
R_data = [] 

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
        #self.th = Thread1()
        self.th2 = Thread2()
        self.th3 = Thread3()
        self.th4 = Thread4()
        self.th5 = Thread5()
        #self.th.start()
        self.th3.start()
        #self.th5.start()
        self.th4.count1.connect(self.getval1)
        self.th4.count2.connect(self.getval2)
        self.th4.count3.connect(self.getval3)
        self.th3.connecton.connect(self.nowconnect_L)
        self.th3.connecton.connect(self.th4.start)
        self.th5.connecton.connect(self.nowconnect_R)
        self.th3.pose.connect(self.drawgraph)
        global nowroutine 
        nowroutine= self.nowroutine_2
        
        self.fig = plt.Figure()
        self.fig_r = plt.Figure()
        # global figure
        # figure = self.fig
        self.canvas = FigureCanvas(self.fig)
        self.canvas_r = FigureCanvas(self.fig_r)
        self.forgraph.addWidget(self.canvas)
        self.forgraph_2.addWidget(self.canvas_r)
        self.triger = True
        self.triger_r = True

        #self.th4.start()

    #button actions    
    def button(self):
        self.start_1.clicked.connect(self.goto6)
        self.finsave_6.clicked.connect(self.goto2)
        self.seerecord_1.clicked.connect(self.goto3)
        #self.calibration_1.clicked.connect(self.goto4)

        self.gotohome_2.clicked.connect(self.gotohome)
        self.gotohome_3.clicked.connect(self.gotohome)
        self.gotohome_4.clicked.connect(self.gotohome)
        self.gotohome_5.clicked.connect(self.gotohome)
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
        self.exitbutton.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.calendar.clicked.connect(self.updatecalrecord)
        

        
        
    #silsigan pose-check
    def goto2(self):
        global nowpage
        nowpage = "self.page_2"
        self.stackedWidget.setCurrentWidget(self.page_2)
        self.nowroutine_2.setText(self.nowroutine_6.currentText())
        # #QSound.play('./sound/eng.wav')
        # QSound('./sound/eng.wav').play()
        # print("why no sound")
        
    # record
    def goto3(self):
        mydb = database.db()
        current_day = QDate.currentDate()
        self.stackedWidget.setCurrentWidget(self.page_4)
        self.todayday.setText(current_day.toString('yyyy-MM-dd'+"의 운동 기록"))
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
        
    def goto6(self):
        # self.th3.start()
        # self.th3.count.connect(self.getval)
        mydb = database.db()

        self.stackedWidget.setCurrentWidget(self.page_6)
        mydb.createWorkoutData()
        mydb.createSensorTable()

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
    
    def nowconnect_L(self):
        QMessageBox.about(self,'Ble Notice','Left arm Connect Success')
        playsound('./sound/eng.wav')

    def nowconnect_R(self):
        QMessageBox.about(self,'Ble Notice','Right arm Connect Success ')
        playsound('./sound/eng.wav')

    def updatecalrecord(self):
        mydb = database.db()
        for i in range(7):
            workrecord = "rec_"+str(i)
            getattr(self, workrecord).setText("")

        current_day = self.calendar.selectedDate()
        self.todayday.setText(current_day.toString('yyyy-MM-dd'+'의 운동 기록'))
        nowday = current_day.toString('yyyy-MM-dd')
        print(nowday)
        row = mydb.returnDayworkoutRows()
        count = len(row)
        j = 0
        for x in range(count):
            day, name, time = row[x]
            if day == nowday:
                workrecord = "rec_"+str(j)
                j = j + 1
                getattr(self, workrecord).setText(name+" "+str(int(time))+"회")
        
        # for i in range(7):
        #     nowday = current_day.addDays(-i).toString('yyyy-MM-dd')
        #     row = mydb.returnDayworkoutRows()
        #     count = len(row)
        #     j = 0
        #     for x in range(count):
        #         day, name, time = row[x]
        #         if day == nowday:
        #             workrecord = "day"+str(7-i)+str(j+1)+"_3"
        #             j = j + 1
        #             getattr(self, workrecord).setText(name+" "+str(int(time))+"회")
    
    def drawgraph(self):
        global L_hand_rpy
        global R_hand_rpy
        hr = np.deg2rad(L_hand_rpy[0])
        hp = np.deg2rad(L_hand_rpy[1])
        hy = np.deg2rad(L_hand_rpy[2])

        rhr = np.deg2rad(R_hand_rpy[0])
        rhp = np.deg2rad(R_hand_rpy[1])
        rhy = np.deg2rad(R_hand_rpy[2])
        
        if self.stackedWidget.currentWidget() == self.page_2:
            # L_x = np.array([np.cos(hp),np.sin(hp)*np.sin(hr) ,np.sin(hp)*np.cos(hr)])
            # L_y = np.array([0,np.cos(hr),-np.sin(hr)])
            # L_z = np.array([-np.sin(hp),np.cos(hp)*np.sin(hr),np.cos(hp)*np.cos(hr)])

            # R_x = np.array([np.cos(rhp),0 ,-np.sin(rhp)])
            # R_y = np.array([np.sin(rhp)*np.sin(rhr),np.cos(rhr),np.cos(rhp)*np.sin(rhr)])
            # R_z = np.array([np.sin(rhp)*np.cos(rhr),-np.sin(rhr),np.cos(rhp)*np.cos(rhr)])

            y1_L = np.cos(30*np.pi/180)
            z1_L = np.sin(30*np.pi/180)
            y2_L = np.cos(70*np.pi/180)
            z2_L = np.sin(70*np.pi/180)
            y3_L = np.cos(90*np.pi/180)
            z3_L = np.sin(90*np.pi/180)
            y4_L = -np.cos(70*np.pi/180)
            z4_L = np.sin(70*np.pi/180)
            y5_L = -np.cos(50*np.pi/180)
            z5_L = np.sin(50*np.pi/180)
            
            # L_1 = np.array([x1_L*np.cos(hp) -z1_L*np.sin(hp) , x1_L*np.sin(hp)*np.sin(hr) + z1_L*np.cos(hp)*np.sin(hr) , x1_L*np.sin(hp)*np.cos(hr) + z1_L*np.cos(hp)*np.cos(hr)])
            # L_2 = np.array([x2_L*np.cos(hp) -z2_L*np.sin(hp) , x2_L*np.sin(hp)*np.sin(hr) + z2_L*np.cos(hp)*np.sin(hr) , x2_L*np.sin(hp)*np.cos(hr) + z2_L*np.cos(hp)*np.cos(hr)])
            # L_3 = np.array([x3_L*np.cos(hp) -z3_L*np.sin(hp) , x3_L*np.sin(hp)*np.sin(hr) + z3_L*np.cos(hp)*np.sin(hr) , x3_L*np.sin(hp)*np.cos(hr) + z3_L*np.cos(hp)*np.cos(hr)])
            # L_4 = np.array([x4_L*np.cos(hp) -z4_L*np.sin(hp) , x4_L*np.sin(hp)*np.sin(hr) + z4_L*np.cos(hp)*np.sin(hr) , x4_L*np.sin(hp)*np.cos(hr) + z4_L*np.cos(hp)*np.cos(hr)])
            # L_5 = np.array([x5_L*np.cos(hp) -z5_L*np.sin(hp) , x5_L*np.sin(hp)*np.sin(hr) + z5_L*np.cos(hp)*np.sin(hr) , x5_L*np.sin(hp)*np.cos(hr) + z5_L*np.cos(hp)*np.cos(hr)])
            L_1 = np.array([-z1_L*np.sin(hp) , y1_L*np.cos(hr) + z1_L*np.cos(hp)*np.sin(hr) , -y1_L*np.sin(hr) + z1_L*np.cos(hp)*np.cos(hr)])
            L_2 = np.array([-z2_L*np.sin(hp) , y2_L*np.cos(hr) + z2_L*np.cos(hp)*np.sin(hr) , -y2_L*np.sin(hr) + z2_L*np.cos(hp)*np.cos(hr)])
            L_3 = np.array([-z3_L*np.sin(hp) , y3_L*np.cos(hr) + z3_L*np.cos(hp)*np.sin(hr) , -y3_L*np.sin(hr) + z3_L*np.cos(hp)*np.cos(hr)])
            L_4 = np.array([-z4_L*np.sin(hp) , y4_L*np.cos(hr) + z4_L*np.cos(hp)*np.sin(hr) , -y4_L*np.sin(hr) + z4_L*np.cos(hp)*np.cos(hr)])
            L_5 = np.array([-z5_L*np.sin(hp) , y5_L*np.cos(hr) + z5_L*np.cos(hp)*np.sin(hr) , -y5_L*np.sin(hr) + z5_L*np.cos(hp)*np.cos(hr)])

            y1_R = np.cos(30*np.pi/180)
            z1_R = np.sin(30*np.pi/180)
            y2_R = np.cos(70*np.pi/180)
            z2_R = np.sin(70*np.pi/180)
            y3_R = np.cos(90*np.pi/180)
            z3_R = np.sin(90*np.pi/180)
            y4_R = -np.cos(70*np.pi/180)
            z4_R = np.sin(70*np.pi/180)
            y5_R = -np.cos(50*np.pi/180)
            z5_R = np.sin(50*np.pi/180)

            R_1 = np.array([-z1_R*np.sin(rhp) , y1_R*np.cos(rhr) + z1_R*np.cos(rhp)*np.sin(rhr) , -y1_R*np.sin(rhr) + z1_R*np.cos(rhp)*np.cos(rhr)])
            R_2 = np.array([-z2_R*np.sin(rhp) , y2_R*np.cos(rhr) + z2_R*np.cos(rhp)*np.sin(rhr) , -y2_R*np.sin(rhr) + z2_R*np.cos(rhp)*np.cos(rhr)])
            R_3 = np.array([-z3_R*np.sin(rhp) , y3_R*np.cos(rhr) + z3_R*np.cos(rhp)*np.sin(rhr) , -y3_R*np.sin(rhr) + z3_R*np.cos(rhp)*np.cos(rhr)])
            R_4 = np.array([-z4_R*np.sin(rhp) , y4_R*np.cos(rhr) + z4_R*np.cos(rhp)*np.sin(rhr) , -y4_R*np.sin(rhr) + z4_R*np.cos(rhp)*np.cos(rhr)])
            R_5 = np.array([-z5_R*np.sin(rhp) , y5_R*np.cos(rhr) + z5_R*np.cos(rhp)*np.sin(rhr) , -y5_R*np.sin(rhr) + z5_R*np.cos(rhp)*np.cos(rhr)])
           
            
            v = np.array([5, 6, 2])


            if(self.triger):
                self.ax = self.fig.add_subplot(111, projection='3d')
                self.triger = False
            if(self.triger_r):
                self.axr = self.fig_r.add_subplot(111, projection='3d')
                self.triger_r = False        
            #print( hand_p, hand_r, hand_y, hr, hp)
            start = [0,0,0]

            # self.axr.quiver(start[0],start[1],start[2],R_x[0],R_x[1],R_x[2],color='red')
            # self.axr.quiver(start[0],start[1],start[2],R_y[0],R_y[1],R_y[2],color='orange')
            # self.axr.quiver(start[0],start[1],start[2],R_z[0],R_z[1],R_z[2],color='magenta')
            # self.axr.quiver(start[0],start[1],-1,0,0,1,color = 'black')

            self.axr.quiver(start[0],start[1],start[2],R_1[0],R_1[1],R_1[2],color='red')
            self.axr.quiver(start[0],start[1],start[2],R_2[0],R_2[1],R_2[2],color='orange')
            self.axr.quiver(start[0],start[1],start[2],R_3[0],R_3[1],R_3[2],color='yellow')
            self.axr.quiver(start[0],start[1],start[2],R_4[0],R_4[1],R_4[2],color='green')
            self.axr.quiver(start[0],start[1],start[2],R_5[0],R_5[1],R_5[2],color='blue')
            self.axr.quiver(start[0],start[1],-1,0,0,1,color = 'black')

            self.axr.set_xlim([-1,1])
            self.axr.set_ylim([-1,1])
            self.axr.set_zlim([-1,1])
            self.canvas_r.draw()
            self.axr.axes.clear()

            # self.ax.quiver(start[0],start[1],start[2],L_x[0],L_x[1],L_x[2],color='red')
            # self.ax.quiver(start[0],start[1],start[2],L_y[0],L_y[1],L_y[2],color='magenta')
            # self.ax.quiver(start[0],start[1],start[2],L_z[0],L_z[1],L_z[2],color='magenta')
            # self.ax.quiver(start[0],start[1],-1,0,0,1,color = 'black')

            self.ax.quiver(start[0],start[1],start[2],L_1[0],L_1[1],L_1[2],color='red')
            self.ax.quiver(start[0],start[1],start[2],L_2[0],L_2[1],L_2[2],color='orange')
            self.ax.quiver(start[0],start[1],start[2],L_3[0],L_3[1],L_3[2],color='yellow')
            self.ax.quiver(start[0],start[1],start[2],L_4[0],L_4[1],L_4[2],color='green')
            self.ax.quiver(start[0],start[1],start[2],L_5[0],L_5[1],L_5[2],color='blue')
            self.ax.quiver(start[0],start[1],-1,0,0,1,color = 'black')

            self.ax.set_xlim([-1,1])
            self.ax.set_ylim([-1,1])
            self.ax.set_zlim([-1,1])
            self.canvas.draw()
            self.ax.axes.clear()
           
            # print("update")



        
        
class Thread1(QThread): 
    
    pose = pyqtSignal()
    def __init__(self): 
        QThread.__init__(self) 
        #self.cond = QWaitCondition()
        #self.mutex = QMutex()
        
        
    def run(self): 
        while True: 
            self.pose.emit()
            sleep(0.6) 
        

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
        global L_hand_rpy
        global R_hand_rpy

        global nowroutine
        global nowrunname
        goal = 0
        goal2 = 0
        totaltry = 0
        record = []
        savetime = 0
        savetime_before = 0
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
                                savetime = int(time()%3)
                                if savetime != savetime_before:
                                    mydb.insertRPY(name, L_hand_rpy, R_hand_rpy)
                                savetime_before = int(time()%3)
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
    pose = pyqtSignal()

    def __init__(self): 
        QThread.__init__(self) 
        #self.cond = QWaitCondition()
        #self.mutex = QMutex()
        
        
    def run(self): 
        global L_hand_rpy  
        global nowrunname , L_data 
        
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

        FSR = HRService.getCharacteristics("6e400008-b5a3-f393-e0a9-e50e24dcca9e")[0] #Notice! Check is characteristic found before usage in production code!

        # Assign delegate to target characteristic
        object1 = MyDelegate(IMU1ACC.getHandle() , IMU1Gyro.getHandle(),IMU1Pose.getHandle(),IMU2ACC.getHandle(),IMU2Gyro.getHandle(),IMU2Pose.getHandle(),FSR.getHandle() )
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
        desc_FSR = FSR.getDescriptors(AssignedNumbers.client_characteristic_configuration)

        
        #desc_z_acc = z_ACC.getDescriptors(AssignedNumbers.client_characteristic_configuration)
       
        # print("Writing \"notification\" flag to descriptor with handle: ", desc[0].handle)
        dev.writeCharacteristic(desc_IMU1ACC[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_IMU1Gyro[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_IMU1Pose[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!

        dev.writeCharacteristic(desc_IMU2ACC[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_IMU2Gyro[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_IMU2Pose[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_FSR[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!


        #dev.writeCharacteristic(desc_z_acc[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
       
        print("Waiting for notifications...")
        self.connecton.emit()
        before_time = time()

        while True:
            if dev.waitForNotifications(1):

                L_data = object1.absolute_data()

                L_hand_rpy =  object1.relativePose()
                
                
                if(time() - before_time > 0.6):
                    self.pose.emit()
                    before_time = time()

        
class Thread4(QThread): 
    
    count1 = pyqtSignal()
    count2 = pyqtSignal()
    count3 = pyqtSignal()
    global L_data
    global R_data
    

    def __init__(self):  
        QThread.__init__(self) 
        #self.cond = QWaitCondition()
        #self.mutex = QMutex()
        
        
    def run(self): 
        L_counter  = Counter()
        R_counter  = Counter()
        before_val1 = 0
        before_val2 = 0
        before_val3 = 0
        while True: 
            if(L_data[2][0] >30 and R_data[2][0]>30):
                if nowrunname == "바벨 컬":
                    temp = L_counter.KcCurl(L_data[0][3])
                    temp2 = R_counter.KcCurl(R_data[0][3])
                    print(temp,temp2)
                    if (before_val1 != max(temp,temp2)):
                        self.count1.emit()
                        print("change signal\n\n\n")
                        before_val1 =max(temp,temp2)

                elif nowrunname == "벤치프레스":   
                    temp = L_counter.dumbelCurl(L_data[1][4]) 
                    if (before_val2 != temp):
                        self.count2.emit()
                        print("change signal\n\n\n")
                        before_val2 =temp

                elif nowrunname == "숄더프레스":
                    temp = L_counter.shoulderPress(L_data[1][3])
                    temp2 = R_counter.shoulderPress(R_data[1][3])
                    if (before_val3 != max(temp,temp2)):
                        self.count3.emit()
                        print("change signal\n\n\n")
                        before_val3 =max(temp,temp2) 



class Thread5(QThread): 

   
    
    count1 = pyqtSignal()
    count2 = pyqtSignal()
    count3 = pyqtSignal()
    connecton = pyqtSignal()

    def __init__(self): 
        QThread.__init__(self) 
        #self.cond = QWaitCondition()
        #self.mutex = QMutex()
        
        
    def run(self): 
        global R_hand_rpy
        global nowrunname , R_data 
        
        print("Connecting...")
        #
        dev = btle.Peripheral("56:ec:8a:8c:21:5d")

 
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

        FSR = HRService.getCharacteristics("6e400008-b5a3-f393-e0a9-e50e24dcca9e")[0] #Notice! Check is characteristic found before usage in production code!

        # Assign delegate to target characteristic
        object1 = MyDelegate(IMU1ACC.getHandle() , IMU1Gyro.getHandle(),IMU1Pose.getHandle(),IMU2ACC.getHandle(),IMU2Gyro.getHandle(),IMU2Pose.getHandle(),FSR.getHandle() )
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
        desc_FSR = FSR.getDescriptors(AssignedNumbers.client_characteristic_configuration)

        
        #desc_z_acc = z_ACC.getDescriptors(AssignedNumbers.client_characteristic_configuration)
       
        # print("Writing \"notification\" flag to descriptor with handle: ", desc[0].handle)
        dev.writeCharacteristic(desc_IMU1ACC[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_IMU1Gyro[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_IMU1Pose[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!

        dev.writeCharacteristic(desc_IMU2ACC[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_IMU2Gyro[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_IMU2Pose[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
        dev.writeCharacteristic(desc_FSR[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!


        #dev.writeCharacteristic(desc_z_acc[0].handle, b"\x01\x00")# Notice! Do not use [0] in production. Check is descriptor found first!
       
        print("Waiting for notifications...")
        before_val1 = 0
        before_val2 = 0
        before_val3 = 0
        beforepose = []
        self.connecton.emit()
          

        while True:
            if dev.waitForNotifications(0.5):

                R_data = object1.absolute_data()
                R_hand_rpy =  object1.relativePose()

                continue

if __name__ == '__main__':        
    app = QtGui.QApplication(sys.argv)
    mainWindow = UI()
    #mainWindow.show()
    mainWindow.showFullScreen()
    sys.exit(app.exec_())

