#-*-coding:utf-8-*-
import sys, os
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from bluepy import btle
from bluepy.btle import AssignedNumbers
from IMU1_multi_data import MyDelegate 
from logicTest import Counter
import database 
from time import time, sleep


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
        #os.system("mpg123 ./sound/start.wav")
        self.button()
        self.nowtime()
        self.th = Thread1()
        self.th2 = Thread2()
        self.th3 = Thread3()
        self.th4 = Thread4()
        self.th5 = Thread5()
        self.th.start()
        #self.th3.start()
        self.th5.start()
        self.th4.count1.connect(self.getval1)
        self.th4.count2.connect(self.getval2)
        self.th4.count3.connect(self.getval3)
        self.th3.connecton.connect(self.nowconnect_L)
        self.th3.connecton.connect(self.th4.start)
        self.th5.connecton.connect(self.nowconnect_R)
        self.th5.connecton.connect(self.th4.start)
        #self.th3.pose.connect(self.drawgraph)
        self.th5.pose.connect(self.drawgraph)
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
        #self.info_3.clicked.connect(self.giveinfo)
        #self.pushButton.clicked.connect(self.liveupdate)
        
        self.addroutine_6.clicked.connect(self.addroutine)
        self.deleteroutine_6.clicked.connect(self.deleteroutine)
        self.nowroutine_6.activated[str].connect(self.changeroutinepage)
        self.selectworkout.activated[str].connect(self.updaterecord)
        #self.saveroutinedb_6.clicked.connect(self.saveroutine)
        self.exitbutton.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.calendar.clicked.connect(self.updatecalrecord)
        self.calendar_2.clicked.connect(self.updatecalrecord_2)

        
        
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
        self.todayday.setText(current_day.toString('yyyy-MM-dd'))
        # for i in range(1,8,1):
        #     nowday = "day"+str(i)+"_3"
        #     getattr(self, nowday).setText(current_day.addDays(i-7).toString('MM.dd'))

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
        #             getattr(self, workrecord).setText(name+" "+str(int(time))+"???")
  
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
        for i in range(12):
            target = "detail_"+str(i+1)
            getattr(self, target).setText("")
        mydb = database.db()
        row = mydb.returnNameWorkoutRows()
        for x in range(len(row)):
            if row[x][0] == self.selectworkout.currentText():
                for i in range(12):
                    target = "detail_"+str(i+1)
                    if i<4: 
                        getattr(self, target).setText(str(round(float(row[x][i+1])/60,2))) 
                    else:
                        getattr(self, target).setText(str(round(float(row[x][i+1]),2))) 
        
    # feedback
    def givefeedback(self):     
        self.stackedWidget.setCurrentWidget(self.page_3) 
        self.stackedWidget_3.setCurrentWidget(self.page_9)     
    
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
        #os.system("mpg123 ./sound/"+str(counttry1)+".wav")
    
    def getval2(self):
        global counttry2
        counttry2 = counttry2 + 1 
        #os.system("mpg123 ./sound/"+str(counttry2)+".wav")

    def getval3(self):
        global counttry3
        counttry3 = counttry3 + 1 
        #os.system("mpg123 ./sound/"+str(counttry3)+".wav")
    
    def nowconnect_L(self):
        QMessageBox.about(self,'Ble Notice','Left arm Connect Success')
        

    def nowconnect_R(self):
        QMessageBox.about(self,'Ble Notice','Right arm Connect Success ')

    def updatecalrecord(self):
        mydb = database.db()
        self.rec_0.setText("No Record")
        for i in range(1,7):
            workrecord = "rec_"+str(i)
            getattr(self, workrecord).setText("")

        current_day = self.calendar.selectedDate()
        self.todayday.setText(current_day.toString('yyyy-MM-dd'))
        nowday = current_day.toString('yyyy-MM-dd')
        print(nowday)
        row = mydb.returnDayworkoutRows()
        count = len(row)
        j = 0
        for x in range(count):
            day, name, trysum, time, kcalsum = row[x]
            if day == nowday:
                workrecord = "rec_"+str(j)
                j = j + 1
                getattr(self, workrecord).setText(name+" "+str(int(trysum))+"??? "+str(int(time/60)+1)+"??? "+ str(round((float(kcalsum)),3)) + "kcal")
        
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
        #             getattr(self, workrecord).setText(name+" "+str(int(time))+"???")
    def updatecalrecord_2(self):
        mydb = database.db()
        row = mydb.returnHandData()
        count = len(row)
        self.stackedWidget_3.setCurrentWidget(self.page_9)
        self.label_9.setText("")

        current_day = self.calendar_2.selectedDate()
        self.label_3.setText(current_day.toString('yyyy-MM-dd'))
        nowday = current_day.toString('yyyy-MM-dd')
        # print(nowday)
        
        for x in range(count):
            day, name, RLavg, PLavg, YLavg, RRavg, PRavg, YRavg = row[x]
            if day == str(nowday) and name == self.cb1_7.currentText():
                self.label_9.setText(str(round(PLavg,2)+round(PRavg,2)/2))
                if(round(PLavg,2)+round(PRavg,2)<5 and round(PLavg,2)+round(PRavg,2)>-5):
                    self.stackedWidget_3.setCurrentWidget(self.page_7)
                elif(round(PLavg,2)+round(PRavg,2)==0):
                    self.stackedWidget_3.setCurrentWidget(self.page_9)
                else:
                    self.stackedWidget_3.setCurrentWidget(self.page_8)
        


    def drawgraph(self):
        global L_hand_rpy
        global R_hand_rpy
        # hr = np.deg2rad(L_hand_rpy[0])
        # hp = np.deg2rad(L_hand_rpy[1])
        # hy = np.deg2rad(L_hand_rpy[2])

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

            y1 = np.cos(20*np.pi/180)
            z1 = np.sin(20*np.pi/180)
            y2 = np.cos(70*np.pi/180)
            z2 = np.sin(70*np.pi/180)
            y3 = np.cos(90*np.pi/180)
            z3 = np.sin(90*np.pi/180)
            y4 = -np.cos(70*np.pi/180)
            z4 = np.sin(70*np.pi/180)
            y5 = -np.cos(50*np.pi/180)
            z5 = np.sin(50*np.pi/180)
        
            # L_1 = np.array([-z1*np.sin(hp) , y1*np.cos(hr) + z1*np.cos(hp)*np.sin(hr) , -y1*np.sin(hr) + z1*np.cos(hp)*np.cos(hr)])
            # L_2 = np.array([-z2*np.sin(hp) , y2*np.cos(hr) + z2*np.cos(hp)*np.sin(hr) , -y2*np.sin(hr) + z2*np.cos(hp)*np.cos(hr)])
            # L_3 = np.array([-z3*np.sin(hp) , y3*np.cos(hr) + z3*np.cos(hp)*np.sin(hr) , -y3*np.sin(hr) + z3*np.cos(hp)*np.cos(hr)])
            # L_4 = np.array([-z4*np.sin(hp) , y4*np.cos(hr) + z4*np.cos(hp)*np.sin(hr) , -y4*np.sin(hr) + z4*np.cos(hp)*np.cos(hr)])
            # L_5 = np.array([-z5*np.sin(hp) , y5*np.cos(hr) + z5*np.cos(hp)*np.sin(hr) , -y5*np.sin(hr) + z5*np.cos(hp)*np.cos(hr)])

            R_1 = np.array([-z1*np.sin(rhp) , y1*np.cos(rhr) + z1*np.cos(rhp)*np.sin(rhr) , -y1*np.sin(rhr) + z1*np.cos(rhp)*np.cos(rhr)])
            R_2 = np.array([-z2*np.sin(rhp) , y2*np.cos(rhr) + z2*np.cos(rhp)*np.sin(rhr) , -y2*np.sin(rhr) + z2*np.cos(rhp)*np.cos(rhr)])
            R_3 = np.array([-z3*np.sin(rhp) , y3*np.cos(rhr) + z3*np.cos(rhp)*np.sin(rhr) , -y3*np.sin(rhr) + z3*np.cos(rhp)*np.cos(rhr)])
            R_4 = np.array([-z4*np.sin(rhp) , y4*np.cos(rhr) + z4*np.cos(rhp)*np.sin(rhr) , -y4*np.sin(rhr) + z4*np.cos(rhp)*np.cos(rhr)])
            R_5 = np.array([-z5*np.sin(rhp) , y5*np.cos(rhr) + z5*np.cos(rhp)*np.sin(rhr) , -y5*np.sin(rhr) + z5*np.cos(rhp)*np.cos(rhr)])
           
            
            v = np.array([5, 6, 2])


            if(self.triger):
                self.ax = self.fig.add_subplot(111, projection='3d')
                self.triger = False
                # self.canvas.draw()
                # axb = self.canvas.copy_from_bbox(self.ax.bbox)

            if(self.triger_r):
                self.axr = self.fig_r.add_subplot(111, projection='3d')
                self.triger_r = False
                # self.canvas_r.draw()        
                # axrb = self.canvas.copy_from_bbox(self.axr.bbox)
            #print( hand_p, hand_r, hand_y, hr, hp)
            start = [0,0,0]

            # self.axr.quiver(start[0],start[1],start[2],R_x[0],R_x[1],R_x[2],color='red')
            # self.axr.quiver(start[0],start[1],start[2],R_y[0],R_y[1],R_y[2],color='orange')
            # self.axr.quiver(start[0],start[1],start[2],R_z[0],R_z[1],R_z[2],color='magenta')
            # self.axr.quiver(start[0],start[1],-1,0,0,1,color = 'black')

            self.axr.quiver(start[0],start[1],start[2],R_1[0]/2,R_1[1]/2,R_1[2]/2,color='red')
            self.axr.quiver(start[0],start[1],start[2],R_2[0]*0.9,R_2[1]*0.9,R_2[2]*0.9,color='orange')
            self.axr.quiver(start[0],start[1],start[2],R_3[0]*1.2,R_3[1]*1.2,R_3[2]*1.2,color='yellow')
            self.axr.quiver(start[0],start[1],start[2],R_4[0]*0.9,R_4[1]*0.9,R_4[2]*0.9,color='green')
            self.axr.quiver(start[0],start[1],start[2],R_5[0]*0.7,R_5[1]*0.7,R_5[2]*0.7,color='blue')
            self.axr.quiver(start[0],start[1],-1,0,0,1,color = 'black')

            self.axr.set_xlim([-1,1])
            self.axr.set_ylim([-1,1])
            self.axr.set_zlim([-1,1])
            self.canvas_r.draw()
            # self.canvas_r.blit(self.axr.bbox)
            self.axr.axes.clear()
            # self.canvas_r.flush_events()

            # self.ax.quiver(start[0],start[1],start[2],L_x[0],L_x[1],L_x[2],color='red')
            # self.ax.quiver(start[0],start[1],start[2],L_y[0],L_y[1],L_y[2],color='magenta')
            # self.ax.quiver(start[0],start[1],start[2],L_z[0],L_z[1],L_z[2],color='magenta')
            # self.ax.quiver(start[0],start[1],-1,0,0,1,color = 'black')

            # self.ax.quiver(start[0],start[1],start[2],L_1[0],L_1[1],L_1[2],color='red')
            # self.ax.quiver(start[0],start[1],start[2],L_2[0],L_2[1],L_2[2],color='orange')
            # self.ax.quiver(start[0],start[1],start[2],L_3[0],L_3[1],L_3[2],color='yellow')
            # self.ax.quiver(start[0],start[1],start[2],L_4[0],L_4[1],L_4[2],color='green')
            # self.ax.quiver(start[0],start[1],start[2],L_5[0],L_5[1],L_5[2],color='blue')
            # self.ax.quiver(start[0],start[1],-1,0,0,1,color = 'black')

            # self.ax.set_xlim([-1,1])
            # self.ax.set_ylim([-1,1])
            # self.ax.set_zlim([-1,1])
            # self.canvas.draw()
            # self.canvas.blit(self.ax.bbox)
            # self.ax.axes.clear()
            # self.canvas.flush_events()
           
            # print("update")



        
        
class Thread1(QThread): 
    
    pose = pyqtSignal()
    def __init__(self): 
        QThread.__init__(self) 
        #self.cond = QWaitCondition()
        #self.mutex = QMutex()
        
        
    def run(self): 
        # while True: 
        #     self.pose.emit()
        #     sleep(0.6) 
        print("hello")

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
                    sleep(0.5)
                    for k in range(goalset):
                        self.exerset.emit(str(goalset))
                        self.resttime.emit(str(rest))
                        goal = count
                        goal2 = count
                        goal3 = goal2
                        counttry1 = 0
                        counttry1_buf = 0
                        counttry2 = 0
                        counttry2_buf = 0
                        counttry3 = 0
                        counttry3_buf = 0
                        if (nowrunname =="?????? ???" or nowrunname == "?????????" or nowrunname =="????????? ????????? ?????????"):
                            while True:
                                #print(counttry1,counttry2,counttry3)
                                self.exercount.emit(str(goal2))
                                goal2 = goal - counttry1
                                if goal3 != goal2:
                                    os.system("mpg123 ./sound/"+str(counttry1)+".wav")
                                    goal3 = goal2
                                #### Virtual Trainer saying ###
                                if counttry1_buf != counttry1:
                                    t_after_count = time()
                                t_now = time()
                                if counttry1 != 0 and t_now - t_after_count > 10:
                                    print("10 seconds last")
                                    os.system("mpg123 ./sound/dodo.wav")
                                    t_after_count = time()
                                ###############################    
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
                                counttry1_buf = counttry1
                                sleep(0.01)
                    
                        if (nowrunname == "?????????" or nowrunname == "??????"):
                            while True:
                                # print("???????????????")
                                self.exercount.emit(str(goal2))
                                goal2 = goal - counttry2
                                if goal3 != goal2:
                                    os.system("mpg123 ./sound/"+str(counttry2)+".wav")
                                    goal3 = goal2

                                #### Virtual Trainer saying ###
                                if counttry2_buf != counttry2:
                                    t_after_count = time()
                                t_now = time()
                                if counttry2 != 0 and t_now - t_after_count > 10:
                                    print("10 seconds last")
                                    os.system("mpg123 ./sound/dodo.wav")
                                    t_after_count = time()

                                if goal2 == 0:
                                    self.exercount.emit(str(goal2))
                                    print("finish 1set")
                                    #saverecord
                                    totaltry = totaltry + counttry2
                                    break
                                elif a%2 == 1:
                                    print("stop")
                                    #saverecord
                                    totaltry = totaltry + counttry2
                                    break
                                savetime = int(time()%3)
                                if savetime != savetime_before:
                                    mydb.insertRPY(name, L_hand_rpy, R_hand_rpy)
                                savetime_before = int(time()%3)
                                counttry2_buf = counttry2
                                sleep(0.01)

                        if (name =="???????????????" or nowrunname == "???????????????" or nowrunname == "???????????????" or nowrunname == "????????????" or nowrunname == "???????????????"):
                            while True:
                                self.exercount.emit(str(goal2))
                                goal2 = goal - counttry3
                                if goal3 != goal2:
                                    os.system("mpg123 ./sound/"+str(counttry3)+".wav")
                                    goal3 = goal2

                                #### Virtual Trainer saying ###
                                if counttry3_buf != counttry3:
                                    t_after_count = time()
                                t_now = time()
                                if counttry3 != 0 and t_now - t_after_count > 10:
                                    print("10 seconds last")
                                    os.system("mpg123 ./sound/dodo.wav")
                                    t_after_count = time()

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
                                savetime = int(time()%3)
                                if savetime != savetime_before:
                                    mydb.insertRPY(name, L_hand_rpy, R_hand_rpy)
                                savetime_before = int(time()%3)
                                counttry3_buf = counttry3
                                sleep(0.01)

                        goalset = goalset-1
                        self.exerset.emit(str(goalset))
                        if k < range(goalset):
                            os.system("mpg123 ./sound/finset.wav")
                            for l in range(rest):
                                self.resttime.emit(str(rest-l))
                                if rest-l == 10:
                                    os.system("mpg123 ./sound/rest10.wav")
                                # if rest-l == 2:
                                    # os.system("mpg123 ./sound/restover.wav")
                                if a%2 == 1:
                                    print("stop")
                                    break
                                sleep(1)
                            os.system("mpg123 ./sound/restover.wav")
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
        #df:e6:f4:32:69:6d
        #7a:97:26:89:44:21
        try:
            dev = btle.Peripheral("7a:97:26:89:44:21")
        except:
            print("reconnect")
            self.run()
            sleep(1)
 
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
        a = time()
        while True:
            try:
                if dev.waitForNotifications(1):

                    L_data = object1.absolute_data()

                    L_hand_rpy =  object1.relativePose()
                    
                    if(time() - before_time > 0.6):
                        self.pose.emit()
                        before_time = time()
                
                    sleep(0.01)
            except:
                print("disconnect")
                break
        self.run()

class Thread4(QThread): 
    
    count1 = pyqtSignal()
    count2 = pyqtSignal()
    count3 = pyqtSignal()
    global L_data
    global R_data
    global nowrunname

    def __init__(self):  
        QThread.__init__(self) 
        #self.cond = QWaitCondition()
        #self.mutex = QMutex()
        
        
    def run(self): 
        L_counter  = Counter()
        R_counter  = Counter()
        before_val1 = 0
        before_val12 = 0
        before_val2 = 0
        before_val22 = 0
        before_val3 = 0
        before_val32 = 0
        
        sleep(1)
        while True: 
            # print(R_data)
            sleep(0.01)
            if(R_data[2][0] >3):# and R_data[2][0]>30):
                #print(R_data)
                #print(nowrunname)
                if nowrunname == None or nowrunname == "":
                    pass
                
                elif nowrunname == "?????? ???" or nowrunname =="?????????" or nowrunname == "????????? ????????? ?????????":
                    print("countinf")
                    temp = 0#L_counter.KcCurl(L_data[0][3])
                    temp2 = R_counter.KcCurl(R_data[0][4])
                    #print(temp,temp2)
                    if (before_val1 != max(temp,temp2)):
                        self.count1.emit()
                        print("change signal\n\n\n")
                        before_val1 =max(temp,temp2)

                elif nowrunname == "?????????" or nowrunname ==  "??????":   
                    temp =0# L_counter.pushUp(L_data[2][0]) 
                    temp2 = R_counter.pushUp(R_data[2][0]) 
                    if (before_val2 != max(temp,temp2)):
                        self.count2.emit()
                        print("change signal\n\n\n")
                        before_val2 =max(temp,temp2)

                elif nowrunname == "???????????????" or nowrunname == "???????????????" or nowrunname == "???????????????" or nowrunname == "????????????" or nowrunname == "???????????????":
                    temp =0# L_counter.shoulderPress(L_data[1][3])
                    temp2 = R_counter.shoulderPress(R_data[0][0])
                    if (before_val3 != max(temp,temp2)):
                        self.count3.emit()
                        print("change signal\n\n\n")
                        before_val3 =max(temp,temp2) 


class Thread5(QThread): 

    from time import time, sleep
    
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
        global R_hand_rpy
        global nowrunname , R_data 
        
        print("Connecting...")
        #
        try:
            dev = btle.Peripheral("7a:97:26:89:44:21")# right
            #  dev = btle.Peripheral("df:e6:f4:32:69:6d")
            # dev = btle.Peripheral("56:ec:8a:8c:21:5d") #left
        except:
            print("reconnect")
            sleep(1)
            self.run()
        # dev = btle.Peripheral("56:ec:8a:8c:21:5d")
        #dev = btle.Peripheral("df:e6:f4:32:69:6d")

 
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
        os.system("mpg123 ./sound/blueconnect.wav")
        sleep(5)
        before_val1 = 0
        before_val2 = 0
        before_val3 = 0
        beforepose = []
        self.connecton.emit()
        #os.system("mpg123 ./sound/connectbt.wav")
        a= time()
        before_time = time()
        while True:
            try:
                if dev.waitForNotifications(1):

                    R_data = object1.absolute_data()
                    R_hand_rpy = object1.relativePose()
                    if(time() - before_time > 0.2):
                        self.pose.emit()
                        before_time = time()
                    sleep(0.01)
                    # print(time()-a)
                    # a= time()
                    continue
            
            except:
                print("sensor disconnect")
                os.system("mpg123 ./sound/bluedisconnect.wav")
                break
        sleep(1)
        self.run()
            
if __name__ == '__main__':        
    app = QtGui.QApplication(sys.argv)
    mainWindow = UI()
    #mainWindow.show()
    mainWindow.showFullScreen()
    sys.exit(app.exec_())

